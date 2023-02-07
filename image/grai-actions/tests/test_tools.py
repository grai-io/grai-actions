import unittest

import validators
from grai_actions import tools
from grai_graph.utils import mock_v1_edge, mock_v1_node
from grai_schemas.base import GraiMetadata
from grai_schemas.v1 import EdgeV1, NodeV1
from grai_schemas.v1.metadata.edges import (
    ColumnToColumnMetadata,
    EdgeTypeLabels,
    GenericEdgeMetadataV1,
)
from grai_schemas.v1.metadata.nodes import (
    ColumnMetadata,
    GenericNodeMetadataV1,
    NodeTypeLabels,
)


def mock_node(name: str, namespace: str = "default"):
    node_dict = {
        "type": "Node",
        "version": "v1",
        "spec": {
            "id": None,
            "name": name,
            "namespace": namespace,
            "data_source": "test_source",
            "display_name": name,
            "is_active": True,
            "metadata": {"grai": ColumnMetadata(node_type=NodeTypeLabels.column.value)},
        },
    }
    node = NodeV1(**node_dict)
    return node


def mock_edge(source_node, destination_node):
    edge_dict = {
        "type": "Edge",
        "version": "v1",
        "spec": {
            "id": None,
            "name": f"{source_node.namespace}.{source_node.name} -> {destination_node.namespace}.{destination_node.name}",
            "namespace": source_node.namespace,
            "data_source": "test_source",
            "source": {"name": source_node.name, "namespace": source_node.namespace},
            "destination": {
                "name": destination_node.name,
                "namespace": destination_node.namespace,
            },
            "is_active": True,
            "metadata": {"grai": ColumnToColumnMetadata(edge_type=EdgeTypeLabels.column_to_column.value)},
        },
    }

    edge = EdgeV1(**edge_dict)
    return edge


def build_mock_type_test_result(a, b, *args):
    args = [a, b, *args]
    nodes = [mock_node(arg) for arg in args]

    nodes[0].spec.metadata.grai.node_attributes.data_type = "int"
    nodes[-1].spec.metadata.grai.node_attributes.data_type = "float"
    return tools.TypeTestResult(nodes[0], nodes)


def test_mock_node_extra_metadata():
    node_dict = {
        "type": "Node",
        "version": "v1",
        "spec": {
            "id": None,
            "name": "tom",
            "namespace": "bombadil",
            "data_source": "test_source",
            "display_name": "Tommy B",
            "is_active": True,
            "metadata": {
                "grai": ColumnMetadata(node_type=NodeTypeLabels.column.value),
                "extra": {},
            },
        },
    }
    try:
        node = NodeV1(**node_dict)
    except Exception as e:
        assert False, "failed to create node and metadata with non-grai metadata fields"


class TestTypeTestResult(unittest.TestCase):
    test_obj = build_mock_type_test_result("a", "b")

    @classmethod
    def test_make_row_is_str(cls):
        row_str = cls.test_obj.make_row()
        assert isinstance(row_str, str)

    @classmethod
    def test_make_row_has_correct_number_of_columns(cls):
        row_str = cls.test_obj.make_row()
        assert row_str.count("|") == 4

    @classmethod
    def test_make_message_is_str(cls):
        message = cls.test_obj.message()
        assert isinstance(message, str)

    @classmethod
    def test_make_message_doesnt_contain_column_breaks(cls):
        message = cls.test_obj.message()
        assert "|" not in message

    @classmethod
    def test_error_metadata_has_all_keys(cls):
        meta = cls.test_obj.error_metadata()
        for key in ["source", "destination", "type", "message"]:
            assert key in meta, f"Missing {key} in metadata result"

    @classmethod
    def test_error_metadata_keys_are_strings(cls):
        meta = cls.test_obj.error_metadata()
        for key in ["source", "destination", "type", "message"]:
            assert isinstance(meta[key], str)

    @classmethod
    def test_error_metadata_type(cls):
        meta = cls.test_obj.error_metadata()
        assert meta["type"] == "Data Type"


def build_mock_nullable_test_result(a, b, *args):
    args = [a, b, *args]
    nodes = [mock_node(arg) for arg in args]

    nodes[0].spec.metadata.grai.node_attributes.is_nullable = True
    nodes[-1].spec.metadata.grai.node_attributes.is_nullable = False
    return tools.NullableTestResult(nodes[0], nodes)


class TestNullableTestResult(unittest.TestCase):
    test_obj = build_mock_nullable_test_result("a", "b")

    @classmethod
    def test_make_row_is_str(cls):
        row_str = cls.test_obj.make_row()
        assert isinstance(row_str, str)

    @classmethod
    def test_make_row_has_correct_number_of_columns(cls):
        row_str = cls.test_obj.make_row()
        assert row_str.count("|") == 4

    @classmethod
    def test_make_message_is_str(cls):
        message = cls.test_obj.message()
        assert isinstance(message, str)

    @classmethod
    def test_make_message_doesnt_contain_column_breaks(cls):
        message = cls.test_obj.message()
        assert "|" not in message

    @classmethod
    def test_error_metadata_has_all_keys(cls):
        meta = cls.test_obj.error_metadata()
        for key in ["source", "destination", "type", "message"]:
            assert key in meta, f"Missing {key} in metadata result"

    @classmethod
    def test_error_metadata_keys_are_strings(cls):
        meta = cls.test_obj.error_metadata()
        for key in ["source", "destination", "type", "message"]:
            assert isinstance(meta[key], str)

    @classmethod
    def test_error_metadata_type(cls):
        meta = cls.test_obj.error_metadata()
        assert meta["type"] == "Nullable"


def build_mock_unique_test_result(a, b, *args):
    args = [a, b, *args]
    nodes = [mock_node(arg) for arg in args]

    nodes[0].spec.metadata.grai.node_attributes.is_unique = True
    nodes[-1].spec.metadata.grai.node_attributes.is_unique = False
    return tools.UniqueTestResult(nodes[0], nodes)


class TestUniqueTestResult(unittest.TestCase):
    test_obj = build_mock_unique_test_result("a", "b")

    @classmethod
    def test_make_row_is_str(cls):
        row_str = cls.test_obj.make_row()
        assert isinstance(row_str, str)

    @classmethod
    def test_make_row_has_correct_number_of_columns(cls):
        row_str = cls.test_obj.make_row()
        assert row_str.count("|") == 4

    @classmethod
    def test_make_message_is_str(cls):
        message = cls.test_obj.message()
        assert isinstance(message, str)

    @classmethod
    def test_make_message_doesnt_contain_column_breaks(cls):
        message = cls.test_obj.message()
        assert "|" not in message

    @classmethod
    def test_error_metadata_has_all_keys(cls):
        meta = cls.test_obj.error_metadata()
        for key in ["source", "destination", "type", "message"]:
            assert key in meta, f"Missing {key} in metadata result"

    @classmethod
    def test_error_metadata_keys_are_strings(cls):
        meta = cls.test_obj.error_metadata()
        for key in ["source", "destination", "type", "message"]:
            assert isinstance(meta[key], str)

    @classmethod
    def test_error_metadata_type(cls):
        meta = cls.test_obj.error_metadata()
        assert meta["type"] == "Uniqueness"


def get_test_summary():
    source_node = mock_node("a")
    results = [
        build_mock_type_test_result("a", "b", "c"),
        build_mock_unique_test_result("a", "c", "d", "e"),
        build_mock_nullable_test_result(
            "a",
            "f",
        ),
    ]
    return tools.TestSummary(source_node, results)


class TestTestSummary(unittest.TestCase):
    summary = get_test_summary()

    @classmethod
    def expected_graph_status_path(cls):
        result = {
            cls.id("a"): {cls.id("b"): True, cls.id("c"): True, cls.id("f"): False},
            cls.id("b"): {
                cls.id("c"): False,
            },
            cls.id("c"): {cls.id("d"): True},
            cls.id("d"): {cls.id("e"): False},
        }
        return result

    @classmethod
    def id(cls, val):
        return ("default", val)

    @classmethod
    def test_graph_status_data_type(cls):
        summary_result = cls.summary.graph_status_path()
        assert isinstance(summary_result, dict), f"Root object not dict, got {type(summary_result)}"
        assert all(
            isinstance(value, dict) for value in summary_result.values()
        ), f"Child object not dict, got {set(type(val) for val in summary_result.values())}"
        assert all(
            isinstance(key, tuple) for key in summary_result.keys()
        ), f"Child key not tuple, got {set(type(val) for val in summary_result.keys())}"
        assert all(
            all(isinstance(key, tuple) for key in values.keys()) for values in summary_result.values()
        ), f"key in child not tuple, got {set(type(v) for val in summary_result.values() for v in val.keys())}"
        assert all(
            all(isinstance(val, bool) for val in values.values()) for values in summary_result.values()
        ), f"value in child not bool, got {set(type(v) for val in summary_result.values() for v in val.values())}"

    @classmethod
    def test_graph_status_root_keys(cls):
        result = cls.expected_graph_status_path()
        summary_result = cls.summary.graph_status_path()
        assert (
            result.keys() == summary_result.keys()
        ), f"Unexpected parent keys. Expected: {list(result.keys())}. Got {list(summary_result.keys())}"

    @classmethod
    def test_graph_status_child_keys(cls):
        result = cls.expected_graph_status_path()
        summary_result = cls.summary.graph_status_path()

        for key in result.keys():
            assert (
                result[key].keys() == summary_result[key].keys()
            ), f"Unexpected child keys in {key}. Expected: {list(result[key].keys())}. Got {list(summary_result[key].keys())}"

    @classmethod
    def test_graph_status_child_values(cls):
        result = cls.expected_graph_status_path()
        summary_result = cls.summary.graph_status_path()

        for key, values in result.items():
            for sub_key, value in values.items():
                assert (
                    value == summary_result[key][sub_key]
                ), f"Incorrect value for graph_status[{key}][{sub_key}], expected {value} got {summary_result[key][sub_key]}"

    @classmethod
    def test_build_mermaid(cls):
        message = cls.summary.mermaid_graph()
        assert isinstance(message, str)

    @classmethod
    def test_build_table(cls):
        message = cls.summary.build_table()
        assert isinstance(message, str)

    @classmethod
    def test_test_summary(cls):
        message = cls.summary.test_summary()
        assert isinstance(message, str)

    @classmethod
    def test_build_link(cls):
        message = cls.summary.build_link()
        assert isinstance(message[1], str)

    @classmethod
    def test_link_is_valid(cls):
        message = cls.summary.build_link()
        assert validators.url(message[0]), f"{message[0]} is not a valid url"

    @classmethod
    def test_message(cls):
        message = cls.summary.message()
        assert isinstance(message, str)
