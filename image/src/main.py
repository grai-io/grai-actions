import json
import os
import urllib.parse
from dataclasses import dataclass

from ghapi.all import GhApi
from grai_client.endpoints.v1.client import ClientV1
from grai_graph import graph
from grai_graph.analysis import GraphAnalyzer
from integrations import get_nodes_and_edges


def validate_item(item, item_name, item_label=None, env_var_label=None):
    if item_label is None:
        item_label = item_name
    if env_var_label is None:
        env_var_label = f"GRAI_{item_name.upper()}"
    message = f"No {item_name} provided, please provide an `{item_label}` value in your workflow or create a `{env_var_label}` secret."
    assert item is not None and item != "", message


@dataclass
class Config:
    github_token = os.environ["GITHUB_TOKEN"]
    owner = os.environ["GITHUB_REPOSITORY_OWNER"]
    repo = os.environ["GITHUB_REPOSITORY"].split("/")[-1]
    namespace = os.environ["GRAI_NAMESPACE"]
    host = os.environ["GRAI_HOST"]
    port = os.environ["GRAI_PORT"]
    git_event = os.environ["GITHUB_EVENT_NAME"]
    api_key = os.environ["GRAI_API_KEY"]
    issue_number = os.environ["PR_NUMBER"]
    workspace = os.environ["GRAI_WORKSPACE"]
    grai_frontend_host = os.environ["GRAI_FRONTEND_HOST"]

    def __post_init__(self):
        self.workspace = None if self.workspace == "" else self.workspace
        self.port = "443" if self.port == "" else self.port

        validate_item(self.api_key, "api-key")
        validate_item(self.github_token, "github-token")
        assert (
            self.api_key is not None and self.api_key != ""
        ), "No api key provided, please provide an `api-key` value in your workflow or create a `GRAI_API_KEY` secret"


config = Config()


def collapsable(content, label):
    result = f"""<details><summary>{label}</summary>
<p>

{content}

</p>
</details>"""
    return result


def heading(string, level):
    return f"<h{level}> {string} </h{level}>"


def mermaid_graph(node_tuples):
    def new_edge(a, b, status):
        return f'{a}-->|"{"✅" if status else "❌"}"| {b};'

    message = f"""```mermaid
graph TD;
    {''.join((new_edge(*tup) for tup in node_tuples))}
```
    """
    return message


def build_table(affected_nodes):
    def make_row(name, dtype):
        row = f"""| {name} | data type | expected {dtype} |
"""
        return row

    rows = "".join([make_row(name, dtype) for name, dtype in affected_nodes])
    message = f"""| Dependency | Test | Message |
| --- | --- | --- |
{rows}
    """
    return message


def build_node_test_summary(name, affected_nodes):
    label = heading(name, 2)
    section = f"""
{heading('Failing Tests', 4)}

{build_table(affected_nodes)}
    """
    return collapsable(section, label)


def build_link(node_name, affected_nodes):
    def node_to_error(name, dtype):
        return {
            "source": node_name,
            "destination": name,
            "type": "data type",
            "message": f"""expected {dtype}""",
        }

    errorList = []

    for name, dtype in affected_nodes:
        errorList.append(node_to_error(name, dtype))

    errors = urllib.parse.quote_plus(json.dumps(errorList))

    return f"""<a href="{config.grai_frontend_host}?limitGraph=true&errors={errors}" target="_blank">Show Plot</a>"""


def build_message(node_name, node_tuple, affected_nodes):
    return f"""
{mermaid_graph(node_tuple)}

{build_node_test_summary(node_name, affected_nodes)}

{config.grai_frontend_host and build_link(node_name, affected_nodes)}
    """


def post_comment(message):
    api = GhApi(owner=config.owner, repo=config.repo, token=config.github_token)
    api.issues.create_comment(config.issue_number, body=message)


def file_deleted():
    pass
    #  TODO


def on_merge(client):
    nodes, edges = get_nodes_and_edges(client)


def build_graph(client):
    G = graph.Graph()
    nodes, edges = get_nodes_and_edges(client)
    if len(nodes) > 0:
        G.add_nodes(nodes)
    if len(edges) > 0:
        G.add_edges(edges)
    return G


def on_pull_request(client):
    G = client.build_graph()
    analysis = GraphAnalyzer(G)

    nodes, edges = get_nodes_and_edges(client)

    errors = False
    for node in nodes:
        new_type = node.spec.metadata.get("data_type", None)
        try:
            original_node = G.get_node(
                name=node.spec.name, namespace=node.spec.namespace
            )
        except:
            # Node doesn't exist
            continue

        affected_nodes = analysis.test_type_change(
            namespace=node.spec.namespace, name=node.spec.name, new_type=new_type
        )
        node_name = node.spec.name
        # TODO: this is technically wrong
        node_tuple = [
            (node_name, n.spec.name, n.spec.metadata["data_type"] == new_type)
            for n in affected_nodes
        ]
        affected_nodes = [
            (n.spec.name, n.spec.metadata["data_type"]) for n in affected_nodes
        ]
        if affected_nodes:
            message = build_message(node_name, node_tuple, affected_nodes)
            post_comment(message)
            errors = True

    if errors:
        raise Exception("Type changes failed")


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
