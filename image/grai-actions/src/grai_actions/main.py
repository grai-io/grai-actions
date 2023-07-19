import uuid

from grai_schemas.v1 import SourcedEdgeV1, SourcedNodeV1, SourceV1

from grai_actions.config import DeveloperActions, SupportedActions, config
from grai_actions.git_messages import create_or_update_comment
from grai_actions.integrations import get_integration
from grai_actions.tools import TestResultCache
from grai_actions.utilities import get_client


def run_integration_tests(client):
    config.grai_source_name = SourceV1.from_spec({"name": config.grai_source_name, "id": uuid.uuid4()})
    integration = get_integration(client)
    nodes, edges = integration.get_nodes_and_edges()
    assert len(nodes) > 0, "No nodes were found"
    assert len(edges) > 0, "No edges were found"
    assert all(isinstance(node, SourcedNodeV1) for node in nodes), "All nodes must be of type NodeV1"
    assert all(isinstance(edge, SourcedEdgeV1) for edge in edges), "All edges must be of type EdgeV1"


def run_update_server(client):
    integration = get_integration(client)
    integration.update()


def run_tests(client):
    results = TestResultCache(client)
    summary = results.consolidated_summary()
    has_errors = len(summary.test_results) > 0

    if has_errors:
        create_or_update_comment(summary.message())
        raise Exception("Test failures detected")
    else:
        create_or_update_comment(None)


def main():
    client = get_client()

    match config.grai_action:
        case SupportedActions.TESTS.value:
            run_tests(client)
        case SupportedActions.UPDATE.value:
            run_update_server(client)
        case DeveloperActions.DEV_TESTS.value:
            run_integration_tests(client)
        case _:
            message = f"Unrecognized action {config.grai_action}. Supported options include {SupportedActions}"
            raise NotImplementedError(message)


if __name__ == "__main__":
    main()
