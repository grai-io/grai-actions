import json
import urllib.parse
from abc import ABC, abstractmethod
from itertools import chain, pairwise
from typing import Dict, List, Tuple

from grai_client.endpoints.v1.client import ClientV1
from grai_graph.analysis import GraphAnalyzer
from grai_schemas.v1 import NodeV1
from grai_schemas.v1.metadata import GraiEdgeMetadataV1 as EdgeMetadata
from grai_schemas.v1.metadata import GraiNodeMetadataV1 as NodeMetadata

from grai_actions import integrations
from grai_actions.config import config
from grai_actions.git_messages import collapsable, heading
from grai_actions.integrations import get_nodes_and_edges

#
# def get_nodes_and_edges(*args, **kwargs):
#     nodes, edges = integrations.get_nodes_and_edges(*args, **kwargs)
#     for node in nodes:
#         item = (
#             node.spec.metadata
#             if isinstance(node.spec.metadata, dict)
#             else node.spec.metadata.dict()
#         )
#         node.spec.metadata = NodeMetadata(**item)
#
#     for edge in edges:
#         item = (
#             edge.spec.metadata
#             if isinstance(edge.spec.metadata, dict)
#             else edge.spec.metadata.dict()
#         )
#         edge.spec.metadata = EdgeMetadata(**item)
#     return nodes, edges


SEPARATOR_CHAR = "/"


def build_node_name(node: NodeV1):
    return f"{node.spec.namespace}{SEPARATOR_CHAR}{node.spec.name}"


class TestResult(ABC):
    """Assumed to be a failing test result"""

    type: str

    def __init__(self, node, test_path):
        self.node: NodeV1 = node
        self.failing_node: NodeV1 = test_path[-1]
        self.test_path = test_path
        self.node_name = build_node_name(self.node)
        self.failing_node_name = build_node_name(self.failing_node)

    @abstractmethod
    def message(self) -> str:
        return ""

    def make_row(self) -> str:
        row = f"| {self.node_name} | {self.type} | {self.message()} |"
        return row

    def error_metadata(self) -> Dict:
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
        self.expected_value = self.failing_node.spec.metadata.grai.node_attributes.data_type
        self.provided_value = self.node.spec.metadata.grai.node_attributes.data_type

    def message(self) -> str:
        return f"Node `{self.failing_node_name}` expected to be {self.expected_value} not {self.provided_value}"


class UniqueTestResult(TestResult):
    type = "Uniqueness"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expected_value = self.failing_node.spec.metadata.grai.node_attributes.is_unique
        self.provided_value = self.node.spec.metadata.grai.node_attributes.is_unique

    def message(self) -> str:
        to_be_or_not_to_be = "not " if self.expected_value else ""
        return f"Node `{self.failing_node_name}` expected {to_be_or_not_to_be}to be unique"


class NullableTestResult(TestResult):
    type = "Nullable"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expected_value = self.failing_node.spec.metadata.grai.node_attributes.is_nullable
        self.provided_value = self.node.spec.metadata.grai.node_attributes.is_nullable

    def message(self) -> str:
        to_be_or_not_to_be = "not " if self.expected_value else ""
        return f"Node `{self.failing_node_name}` expected {to_be_or_not_to_be}to be nullable"


class TestSummary:
    def __init__(self, source_node, test_results):
        self.source_node: NodeV1 = source_node
        self.test_results: List[TestResult] = test_results

    def graph_status_path(self) -> Dict[Tuple[str, str], Dict[Tuple[str, str], bool]]:
        edge_status = {}
        for test in self.test_results:
            path_edges = list(pairwise(test.test_path))
            if len(path_edges) < 1:
                raise Exception("Test paths must have more than two nodes")

            for a, b in path_edges:
                a_id = (a.spec.namespace, a.spec.name)
                b_id = (b.spec.namespace, b.spec.name)
                edge_status.setdefault(a_id, {})
                edge_status[a_id].setdefault(b_id, True)
            edge_status[a_id][b_id] = False

        return edge_status

    def mermaid_graph(self) -> str:
        def new_edge(a, b, status):
            a, b = [f"{namespace}{SEPARATOR_CHAR}{name}" for namespace, name in [a, b]]
            return f'\t{a}-->|"{"✅" if status else "❌"}"| {b};'

        graph_status = self.graph_status_path()
        edges = "\n".join(new_edge(a, b, status) for a, values in graph_status.items() for b, status in values.items())
        message = f"```mermaid\ngraph TD;\n{edges}\n```"
        return message

    def build_table(self) -> str:
        rows = "\n".join([test.make_row() for test in self.test_results])
        message = f"| Dependency | Test | Message |\n| --- | --- | --- |\n{rows}"
        return message

    def test_summary(self) -> str:
        label = heading(build_node_name(self.source_node), 2)
        section = f"{heading('Failing Tests', 4)}\n\n{self.build_table()}\n"
        return collapsable(section, label)

    def build_link(self):
        errors = [error.error_metadata() for error in self.test_results]
        errors = urllib.parse.quote_plus(json.dumps(errors))
        link = f"{config.grai_frontend_url}/workspaces/{config.grai_workspace}/graph?limitGraph=true&errors={errors}"
        return link, f"""<a href="{link}" target="_blank">Show Plot</a>"""

    def message(self) -> str:
        message = f"\n{self.mermaid_graph()}\n\n{self.test_summary()}\n"
        if config.grai_frontend_url:
            message = f"{message}\n{self.build_link()[1]}"

        return message


class TestResultCache:
    def __init__(self, client: ClientV1):
        self.client = client
        self.new_nodes, self.new_edges = get_nodes_and_edges(client)

        self.graph = self.client.build_graph()
        self.analysis = GraphAnalyzer(graph=self.graph)

    @property
    def new_columns(self):
        for node in self.new_nodes:
            node_type = node.spec.metadata.grai.node_type
            if node_type != "Column":
                continue
            yield node

    def type_tests(self):
        errors = False

        result_map = {}
        for node in self.new_columns:
            try:
                original_node = self.graph.get_node(name=node.spec.name, namespace=node.spec.namespace)
            except:
                # This is a new node
                continue

            result = node.spec.metadata.grai.node_attributes.data_type
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
                original_node = self.graph.get_node(name=node.spec.name, namespace=node.spec.namespace)
            except:
                # This is a new node
                continue

            result = node.spec.metadata.grai.node_attributes.is_unique
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
                original_node = self.graph.get_node(name=node.spec.name, namespace=node.spec.namespace)
            except:
                # This is a new node
                continue

            result = node.spec.metadata.grai.node_attributes.is_nullable
            affected_nodes = self.analysis.test_nullable_violations(
                namespace=node.spec.namespace, name=node.spec.name, is_nullable=result
            )
            result_map[node] = [NullableTestResult(node, path) for path in affected_nodes]
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
