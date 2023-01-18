import json
import urllib.parse
from abc import ABC, abstractmethod
from itertools import chain, pairwise
from typing import Dict, List

from grai_client.endpoints.v1.client import ClientV1
from grai_client.schemas.node import NodeV1
from grai_graph.analysis import GraphAnalyzer
from grai_schemas.models import GraiEdgeMetadata, GraiNodeMetadata

from grai_actions import get_nodes_and_edges as integration_nodes_and_edges

from .config import config
from .git_messages import collapsable, heading


def get_nodes_and_edges(*args, **kwargs):
    nodes, edges = integration_nodes_and_edges(*args, **kwargs)
    for node in nodes:
        node.spec.metadata = GraiNodeMetadata(**node.spec.metadata.dict())

    for edge in edges:
        edge.spec.metadata = GraiEdgeMetadata(**edge.spec.metadata.dict())
    return nodes, edges


class TestResult(ABC):
    type: str

    def __init__(self, node, test_path):
        self.node: NodeV1 = node
        self.failing_node: NodeV1 = test_path[-1]
        self.test_path = test_path

    @abstractmethod
    def message(self):
        pass

    def make_row(self):
        row = f"| {self.node.spec.name} | {self.type} | {self.message()} |\n"
        return row

    def error_metadata(self):
        return {
            "source": self.node.spec.name,
            "destination": self.failing_node.spec.name,
            "type": self.type,
            "message": self.message(),
        }


class TypeTestResult(TestResult):
    type = "Data Type"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expected_value = (
            self.failing_node.spec.metadata.grai.node_attributes.data_type
        )
        self.provided_value = self.node.spec.metadata.grai.node_attributes.data_type

    def message(self):
        return f"Node {self.failing_node} expected to be {self.expected_value}"


class UniqueTestResult(TestResult):
    type = "Uniqueness"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expected_value = (
            self.failing_node.spec.metadata.grai.node_attributes.is_unique
        )
        self.provided_value = self.node.spec.metadata.grai.node_attributes.is_unique

    def message(self):
        to_be_or_not_to_be = "not " if self.expected_value else ""
        return f"Node {self.failing_node} was expected {to_be_or_not_to_be}to be unique"


class NullableTestResult(TestResult):
    type = "Nullable"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expected_value = (
            self.failing_node.spec.metadata.grai.node_attributes.is_nullable
        )
        self.provided_value = self.node.spec.metadata.grai.node_attributes.is_nullable

    def message(self):
        to_be_or_not_to_be = "not " if self.expected_value else ""
        return (
            f"Node {self.failing_node} was expected {to_be_or_not_to_be}to be nullable"
        )


class TestSummary:
    def __init__(self, source_node, test_results):
        self.source_node: NodeV1 = source_node
        self.test_results: List[TestResult] = test_results

    def graph_status_path(self):
        edge_status = {}
        for test in self.test_results:
            for a, b in pairwise(test.test_path):
                a_id = (a.spec.namespace, a.spec.name)
                b_id = (b.spec.namespace, b.spec.name)
                edge_status.setdefault(a_id, {b_id: True})
            edge_status[a_id][b_id] = False

        return edge_status

    def mermaid_graph(self):
        def new_edge(a, b, status):
            return f'{a}-->|"{"✅" if status else "❌"}"| {b};'

        graph_status = self.graph_status_path()
        edges = "".join(
            new_edge(a, b, status)
            for a, values in graph_status.items()
            for b, status in values.items()
        )
        message = f"```mermaid\ngraph TD;\n{edges}\n```"

    def build_table(self):
        rows = [test.make_row() for test in self.test_results]
        message = f"| Dependency | Test | Message |\n| --- | --- | --- |\n{rows}"
        return message

    def test_summary(self):
        label = heading(self.source_node.spec.name, 2)
        section = f"{heading('Failing Tests', 4)}\n\n{self.build_table()}\n"
        return collapsable(section, label)

    def build_link(self):
        errors = (error.error_metadata() for error in self.test_results)
        errors = urllib.parse.quote_plus(json.dumps(errors))
        return f"""<a href="{config.grai_frontend_host}/workspaces/{config.workspace}/graph?limitGraph=true&errors={errors}" target="_blank">Show Plot</a>"""

    def message(self):
        message = f"\n{self.mermaid_graph()}\n\n{self.test_summary()}\n"
        if config.grai_frontend_host:
            message = f"{message}\n{self.build_link()}"

        return message


class TestResultCache:
    def __init__(self, client: ClientV1):
        self.client = client
        self.graph = self.client.build_graph()
        self.analysis = GraphAnalyzer(graph=self.graph)
        self.new_nodes, self.new_edges = get_nodes_and_edges(client)

    @property
    def new_columns(self):
        for node in self.new_nodes:
            node_type = node.spec.metadata["grai"]["node_type"]
            if node_type != "Column":
                continue
            yield node

    def type_tests(self):
        errors = False

        result_map = {}
        for node in self.new_columns:
            try:
                original_node = self.graph.get_node(
                    name=node.spec.name, namespace=node.spec.namespace
                )
            except:
                # This is a new node
                continue

            result = node.spec.metadata["grai"]["node_attributes"].get(
                "data_type", None
            )
            affected_nodes = self.analysis.test_type_change(
                namespace=node.spec.namespace, name=node.spec.name, new_type=result
            )
            result_map[node] = [TypeTestResult(node, [path]) for path in affected_nodes]
        return result_map

    def unique_tests(self):
        errors = False
        result_map = {}
        for node in self.new_columns:
            try:
                original_node = self.graph.get_node(
                    name=node.spec.name, namespace=node.spec.namespace
                )
            except:
                # This is a new node
                continue

            result = node.spec.metadata["grai"]["node_attributes"].get(
                "is_unique", None
            )
            affected_nodes = self.analysis.test_unique_violations(
                namespace=node.spec.namespace,
                name=node.spec.name,
                expects_unique=result,
            )
            result_map[node] = [UniqueTestResult(node, path) for path in affected_nodes]
        return result_map

    def null_tests(self):
        errors = False
        result_map = {}
        for node in self.new_columns:
            try:
                original_node = self.graph.get_node(
                    name=node.spec.name, namespace=node.spec.namespace
                )
            except:
                # This is a new node
                continue

            result = node.spec.metadata["grai"]["node_attributes"].get(
                "is_unique", None
            )
            affected_nodes = self.analysis.test_nullable_violations(
                namespace=node.spec.namespace, name=node.spec.name, is_nullable=result
            )
            result_map[node] = [
                NullableTestResult(node, path) for path in affected_nodes
            ]
        return result_map

    def test_results(self):
        tests = chain(
            self.unique_tests().items(),
            self.null_tests().items(),
            self.type_tests().items(),
        )

        results: Dict[str, List[TestResult]] = {}
        for key, values in tests:
            results.setdefault(key, [])
            results[key].extend(values)

        return results

    def messages(self):
        test_results = self.test_results()
        for node, tests in test_results.items():
            yield TestSummary(node, tests).message()
