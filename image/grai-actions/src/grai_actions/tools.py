import json
import urllib.parse
from abc import ABC, abstractmethod
from itertools import chain, pairwise
from typing import Dict, Iterable, List, Tuple

from grai_client.endpoints.v1.client import ClientV1
from grai_client.integrations.base import GraiIntegrationImplementation
from grai_client.update import compute_graph_changes
from grai_graph.analysis import GraphAnalyzer
from grai_graph.graph import Graph
from grai_schemas.v1 import EdgeV1, NodeV1

from grai_actions.config import config
from grai_actions.git_messages import collapsable, heading

SEPARATOR_CHAR = "/"


def build_node_name(node: NodeV1) -> str:
    return f"{node.spec.namespace}{SEPARATOR_CHAR}{node.spec.name}"


class TestResult(ABC):
    """Assumed to be a failing test result"""

    type: str

    def __init__(self, node: NodeV1, test_path: List[NodeV1], test_pass: bool = False):
        self.node = node
        self.failing_node = test_path[-1]
        self.test_path = test_path
        self.node_name = build_node_name(self.node)
        self.failing_node_name = build_node_name(self.failing_node)
        self.test_pass = test_pass

    @abstractmethod
    def message(self) -> str:
        return ""

    def make_row(self) -> str:
        row = f"| {self.node.spec.namespace} | {self.node.spec.name} | {self.failing_node_name} | {self.type} | {self.message()} |"
        return row

    def error_metadata(self) -> Dict:
        return {
            "source": self.node.spec.name,
            "destination": self.failing_node.spec.name,
            "type": self.type,
            "message": self.message(),
        }


class DeletedTestResult(TestResult):
    type = "Deleted"

    def message(self) -> str:
        return (
            f"Node `{self.failing_node.spec.name}` was deleted. It had {len(self.test_path)} downstream dependencies "
            f"ending in {self.test_path[-1].spec.name}"
        )


class TypeTestResult(TestResult):
    type = "Data Type"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expected_value = self.failing_node.spec.metadata.grai.node_attributes.data_type
        self.provided_value = self.node.spec.metadata.grai.node_attributes.data_type

    def message(self) -> str:
        return f"Node `{self.failing_node.spec.name}` expected `{self.node.spec.name}` to be of type {self.expected_value} not {self.provided_value}"


class UniqueTestResult(TestResult):
    type = "Uniqueness"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expected_value = self.failing_node.spec.metadata.grai.node_attributes.is_unique
        self.provided_value = self.node.spec.metadata.grai.node_attributes.is_unique

    def message(self) -> str:
        to_be_or_not_to_be = "to be" if self.expected_value else "**not** to be"
        return f"Node `{self.failing_node.spec.name}` expected `{self.node.spec.name}` {to_be_or_not_to_be} unique"


class NullableTestResult(TestResult):
    type = "Nullable"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expected_value = self.failing_node.spec.metadata.grai.node_attributes.is_nullable
        self.provided_value = self.node.spec.metadata.grai.node_attributes.is_nullable

    def message(self) -> str:
        to_be_or_not_to_be = "to be" if self.expected_value else "**not** to be"
        return f"Node `{self.failing_node.spec.name}` expected `{self.node.spec.name}` {to_be_or_not_to_be} nullable"


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
        message = f"| Namespace | Changed Node | Failing Dependency | Test | Message |\n| --- | --- | --- | --- | --- |\n{rows}"
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
    def __init__(self, new_nodes: List[NodeV1], new_edges: List[EdgeV1], graph: Graph):
        self.new_nodes, self.new_edges = new_nodes, new_edges
        _, _, self.deleted_nodes = compute_graph_changes(new_nodes, graph.manifest.nodes)

        self.graph = graph
        self.analysis = GraphAnalyzer(graph=self.graph)

    @property
    def new_columns(self):
        for node in self.new_nodes:
            node_type = node.spec.metadata.grai.node_type
            if node_type != "Column":
                continue
            yield node

    def data_type_tests(self) -> Dict[NodeV1, List[TypeTestResult]]:
        errors = False

        result_map = {}
        for node in self.new_columns:
            try:
                original_node = self.graph.get_node(name=node.spec.name, namespace=node.spec.namespace)
            except:
                # This is a new node
                continue

            result = node.spec.metadata.grai.node_attributes.data_type
            affected_nodes = self.analysis.test_data_type_change(
                namespace=node.spec.namespace, name=node.spec.name, new_type=result
            )
            test_results = [TypeTestResult(node, path, test_pass) for (path, test_pass) in affected_nodes]
            if test_results:
                result_map[node] = test_results
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
            test_results = [UniqueTestResult(node, path, test_pass) for (path, test_pass) in affected_nodes]
            if test_results:
                result_map[node] = test_results

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
            test_results = [NullableTestResult(node, path, test_pass) for (path, test_pass) in affected_nodes]
            if test_results:
                result_map[node] = test_results
        return result_map

    def deleted_tests(self) -> Dict[NodeV1, List[DeletedTestResult]]:
        errors = False
        result_map = {}
        for node in self.deleted_nodes:
            downstream = self.analysis.test_delete_node(node.spec.namespace, node.spec.name)
            failed = len(downstream) > 0
            result_map[node] = [DeletedTestResult(node, downstream, failed)]
        return result_map

    def test_results(self) -> Dict[NodeV1, List[TestResult]]:
        tests = chain(
            self.unique_tests().items(),
            self.null_tests().items(),
            self.deleted_tests().items(),
            # self.data_type_tests().items(),
        )

        results: Dict[NodeV1, List[TestResult]] = {}
        for key, values in tests:
            results.setdefault(key, [])
            results[key].extend(values)

        return results

    def test_failures(self) -> Dict[NodeV1, List[TestResult]]:
        return {k: [test for test in v if not test.test_pass] for k, v in self.test_results().items()}

    def messages(self) -> Iterable[str]:
        for node, tests in self.test_failures().items():
            yield SingleSourceTestSummary(node, tests).message()

    def consolidated_summary(self) -> TestSummary:
        test_failures = list(chain.from_iterable(self.test_failures().values()))
        summary = TestSummary(test_failures)
        return summary


class TestResultCache(TestResultCacheBase):
    def __init__(self, client: ClientV1, integration: GraiIntegrationImplementation):
        self.client = client
        new_nodes, new_edges = integration.get_nodes_and_edges()

        try:
            graph = self.client.build_graph()
        except Exception as e:
            raise Exception(
                f"Failed to load data from the provided client running on host={client.host} and port={client.port}"
            ) from e
        super().__init__(new_nodes, new_edges, graph)
