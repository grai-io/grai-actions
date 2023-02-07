from grai_client.update import update

from grai_actions.config import SupportedActions, config
from grai_actions.git_messages import post_comment
from grai_actions.integrations import get_nodes_and_edges
from grai_actions.tools import TestResultCache
from grai_actions.utilities import get_client


def run_update_server(client):
    nodes, edges = get_nodes_and_edges(client)
    update(client, nodes)
    update(client, edges)


def run_tests(client):
    results = TestResultCache(client)
    summary = results.consolidated_summary()
    has_errors = len(summary.test_results) > 0
    for message in results.messages():
        post_comment(message)
        errors = True

    if has_errors:
        post_comment(summary.message())
        raise Exception("Test failures detected")


def main():
    client = get_client()

    match config.grai_action:
        case SupportedActions.TESTS.value:
            run_tests(client)
        case SupportedActions.UPDATE.value:
            run_update_server(client)
        case _:
            message = f"Unrecognized action {config.grai_action}. Supported options include {SupportedActions}"
            raise NotImplementedError(message)


if __name__ == "__main__":
    main()
