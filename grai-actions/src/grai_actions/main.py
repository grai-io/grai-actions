from grai_client.endpoints.v1.client import ClientV1
from grai_client.update import update

from grai_actions.config import SUPPORTED_ACTIONS, config
from grai_actions.git_messages import post_comment
from grai_actions.integrations import get_nodes_and_edges
from grai_actions.tools import TestResultCache


def run_update_server(client):
    nodes, edges = get_nodes_and_edges(client)
    update(client, nodes)
    update(client, edges)


def run_tests(client):
    results = TestResultCache(client)

    errors = False
    for message in results.messages():
        post_comment(message)
        errors = True

    if errors:
        raise Exception("Test failures detected")


def main():
    conn_kwargs = {}
    if config.workspace is not None:
        conn_kwargs["workspace"] = config.workspace

    client = ClientV1(config.host, config.port, **conn_kwargs)
    client.set_authentication_headers(api_key=config.api_key)

    authentication_status = client.check_authentication()
    if authentication_status.status_code != 200:
        raise Exception(f"Authentication to {config.host} failed")

    match config.grai_action:
        case "tests":
            run_tests(client)
        case "update":
            run_update_server(client)
        case _:
            # try importing access_mode?
            message = f"Unrecognized action {config.grai_action}. Supported options include {SUPPORTED_ACTIONS}"
            raise NotImplementedError(message)


if __name__ == "__main__":
    main()
