import unittest

from grai_client.schemas.edge import EdgeV1
from grai_client.schemas.node import NodeV1
from grai_graph.utils import mock_v1_edge, mock_v1_node
from grai_schemas.base import Metadata
from grai_schemas.models import (
    ColumnMetadata,
    ColumnToColumnAttributes,
    GraiEdgeMetadata,
    GraiNodeMetadata,
)

from grai_actions import tools


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
            "metadata": {"grai": ColumnMetadata()},
        },
    }
    node = NodeV1(**node_dict)
    node.spec.metadata = Metadata(**node.spec.metadata)
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
            "metadata": {"grai": ColumnToColumnAttributes()},
        },
    }

    edge = EdgeV1(**edge_dict)
    edge.spec.metadata = Metadata(**edge.spec.metadata)
    return edge


def build_mock_type_test_result():
    a = mock_node("a")
    a.spec.metadata.grai.node_attributes.data_type = "int"
    b = mock_node("b")
    b.spec.metadata.grai.node_attributes.data_type = "float"

    return tools.TypeTestResult(a, [a, b])


class TestTypeTestResult(unittest.TestCase):
    test_obj = build_mock_type_test_result()

    @classmethod
    def test_make_row_is_str(cls):
        row_str = cls.test_obj.make_row()
        assert isinstance(row_str, str)

    @classmethod
    def test_make_row_has_correct_number_of_columns(cls):
        row_str = cls.test_obj.make_row()
        assert row_str.count("|") == 4

    @classmethod
    def test_make_row_ends_with_newline(cls):
        row_str = cls.test_obj.make_row()
        assert row_str.endswith("\n")

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


def build_mock_nullable_test_result():
    a = mock_node("a")
    a.spec.metadata.grai.node_attributes.is_nullable = True
    b = mock_node("b")
    b.spec.metadata.grai.node_attributes.is_nullable = False

    return tools.NullableTestResult(a, [a, b])


class TestNullableTestResult(unittest.TestCase):
    test_obj = build_mock_nullable_test_result()

    @classmethod
    def test_make_row_is_str(cls):
        row_str = cls.test_obj.make_row()
        assert isinstance(row_str, str)

    @classmethod
    def test_make_row_has_correct_number_of_columns(cls):
        row_str = cls.test_obj.make_row()
        assert row_str.count("|") == 4

    @classmethod
    def test_make_row_ends_with_newline(cls):
        row_str = cls.test_obj.make_row()
        assert row_str.endswith("\n")

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


def build_mock_unique_test_result():
    a = mock_node("a")
    a.spec.metadata.grai.node_attributes.is_unique = True
    b = mock_node("b")
    b.spec.metadata.grai.node_attributes.is_unique = False

    return tools.UniqueTestResult(a, [a, b])


class TestUniqueTestResult(unittest.TestCase):
    test_obj = build_mock_unique_test_result()

    @classmethod
    def test_make_row_is_str(cls):
        row_str = cls.test_obj.make_row()
        assert isinstance(row_str, str)

    @classmethod
    def test_make_row_has_correct_number_of_columns(cls):
        row_str = cls.test_obj.make_row()
        assert row_str.count("|") == 4

    @classmethod
    def test_make_row_ends_with_newline(cls):
        row_str = cls.test_obj.make_row()
        assert row_str.endswith("\n")

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
