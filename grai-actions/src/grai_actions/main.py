from grai_client.endpoints.v1.client import ClientV1

from grai_actions.integrations import get_nodes_and_edges

from .config import config
from .git_messages import post_comment
from .tools import TestResultCache


def file_deleted():
    pass
    #  TODO


def on_merge(client):
    nodes, edges = get_nodes_and_edges(client)


def on_pull_request(client):
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

    if config.git_event == "merge":
        return on_merge(client)
    elif config.git_event == "pull_request":
        return on_pull_request(client)


if __name__ == "__main__":
    main()
