import json
import urllib.parse
from abc import ABC, abstractmethod
from itertools import chain, pairwise
from typing import Dict, Iterable, List, Tuple

from grai_client.endpoints.v1.client import ClientV1
from grai_graph.analysis import GraphAnalyzer, Graph
from grai_schemas.v1 import NodeV1, EdgeV1
from grai_schemas.v1.metadata import GraiEdgeMetadataV1 as EdgeMetadata
from grai_schemas.v1.metadata import GraiNodeMetadataV1 as NodeMetadata

from grai_actions import integrations
from grai_actions.config import config
from grai_actions.git_messages import collapsable, heading
from grai_actions.integrations import get_nodes_and_edges

SEPARATOR_CHAR = "/"


def build_node_name(node: NodeV1) -> str:
    return f"{node.spec.namespace}{SEPARATOR_CHAR}{node.spec.name}"


class TestResult(ABC):
    """Assumed to be a failing test result"""

    type: str

    def __init__(self, node: NodeV1, test_path: List[NodeV1]):
        self.node = node
        self.failing_node = test_path[-1]
        self.test_path = test_path
        self.node_name = build_node_name(self.node)
        self.failing_node_name = build_node_name(self.failing_node)

    @abstractmethod
    def message(self) -> str:
        return ""

    def make_row(self) -> str:
        row = f"| {self.node_name} | {self.failing_node_name} | {self.type} | {self.message()} |"
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
    def __init__(self, test_results):
        self.test_results: List[TestResult] = test_results

    def graph_status_path(self) -> Dict[Tuple[str, str], Dict[Tuple[str, str], bool]]:
        edge_status: Dict[Tuple[str, str], Dict[Tuple[str, str], bool]] = {}
        for test in self.test_results:
            path_edges = list(pairwise(test.test_path))
            if len(path_edges) < 1:
                raise Exception("Test paths must have more than two nodes")

            for a, b in path_edges:
                for node in [a, b]:
                    assert node.spec.namespace is not None
                    assert node.spec.name is not None
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
        message = f"| Changed Node | Failing Dependency | Test | Message |\n| --- | --- | --- | --- |\n{rows}"
        return message

    def test_summary(self) -> str:
        label = heading("Test Results", 2)
        section = f"\n{self.build_table()}\n"
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


class SingleSourceTestSummary(TestSummary):
    def __init__(self, source_node, test_results, *args, **kwargs):
        self.source_node = source_node
        super().__init__(test_results, *args, **kwargs)

    def test_summary(self) -> str:
        label = heading(build_node_name(self.source_node), 2)
        section = f"{heading('Failing Tests', 4)}\n\n{self.build_table()}\n"
        return collapsable(section, label)


class TestResultCacheBase:
    def __init__(self, new_nodes: List[NodeV1], new_edges: List[EdgeV1], graph):
        self.new_nodes, self.new_edges = new_nodes, new_edges
        self.graph = graph
        self.analysis = GraphAnalyzer(graph=self.graph)

    @property
    def new_columns(self):
        for node in self.new_nodes:
            node_type = node.spec.metadata.grai.node_type
            if node_type != "Column":
                continue
            yield node

    def type_tests(self) -> Dict[NodeV1, List[TypeTestResult]]:
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
            result_map[node] = [TypeTestResult(node, path) for path in affected_nodes]
        return result_map

    def unique_tests(self) -> Dict[NodeV1, List[UniqueTestResult]]:
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

    def null_tests(self) -> Dict[NodeV1, List[NullableTestResult]]:
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

    def test_results(self) -> Dict[NodeV1, List[TestResult]]:
        tests = chain(
            self.unique_tests().items(),
            self.null_tests().items(),
            self.type_tests().items(),
        )

        results: Dict[NodeV1, List[TestResult]] = {}
        for key, values in tests:
            results.setdefault(key, [])
            results[key].extend(values)

        return results

    def messages(self) -> Iterable[str]:
        test_results = self.test_results()
        for node, tests in test_results.items():
            yield SingleSourceTestSummary(node, tests).message()

    def consolidated_summary(self) -> TestSummary:
        test_failures = list(chain.from_iterable(self.test_results().values()))
        summary = TestSummary(test_failures)
        return summary


class TestResultCache(TestResultCacheBase):
    def __init__(self, client: ClientV1):
        self.client = client
        new_nodes, new_edges = get_nodes_and_edges(client)

        try:
            graph = self.client.build_graph()
        except Exception as e:
            raise Exception(
                f"Failed to load data from the provided client running on host={client.host} and port={client.port}"
            ) from e
        super().__init__(new_nodes, new_edges, graph)
