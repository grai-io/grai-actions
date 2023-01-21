from grai_client.update import update

from grai_actions.config import SupportedActions, config
from grai_actions.git_messages import post_comment
from grai_actions.tools import TestResultCache, get_nodes_and_edges
from grai_actions.utilities import get_client


def run_update_server(client):
    nodes, edges = get_nodes_and_edges(client)
    update(client, nodes)
    update(client, edges)


def run_tests(client, config):
    results = TestResultCache(client)

    errors = False
    for message in results.messages():
        post_comment(message)
        errors = True

    if errors:
        raise Exception("Test failures detected")


def main():
    client = get_client()

    match config.grai_action:
        case SupportedActions.TESTS.value:
            run_tests(client, config)
        case SupportedActions.UPDATE.value:
            run_update_server(client, config)
        case _:
            message = f"Unrecognized action {config.grai_action}. Supported options include {SupportedActions}"
            raise NotImplementedError(message)


if __name__ == "__main__":
    main()
