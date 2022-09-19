import os
from ghapi.all import GhApi
from dataclasses import dataclass
from grai_source_flat_file.base import update_server
from grai_client.endpoints.v1.client import ClientV1


@dataclass
class config:
    github_token = os.environ['GITHUB_TOKEN']
    owner = os.environ['GITHUB_REPOSITORY_OWNER']
    repo = os.environ['GITHUB_REPOSITORY'].split('/')[-1]
    file = os.environ['TRACKED_FILE']
    namespace = os.environ['GRAI_NAMESPACE']
    host = os.environ['GRAI_HOST']
    port = os.environ['GRAI_PORT']
    git_event = os.environ['GITHUB_EVENT_NAME']
    grai_auth_token = os.environ['GRAI_AUTH_TOKEN']
    issue_number = os.environ['PR_NUMBER']#os.environ['GITHUB_REF'].split('/')[2]


def collapsable(content, label):
    result = f"""<details><summary>{label}</summary>
<p>

{content}

</p>
</details>"""
    return result


def heading(string, level):
    return f'<h{level}> {string} </h{level}>'


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


def build_message(node_name, node_tuple, affected_nodes):
    return f"""
{mermaid_graph(node_tuple)}

{build_node_test_summary(node_name, affected_nodes)}
    
    """


def post_comment(message):
    api = GhApi(owner=config.owner, repo=config.repo, token=config.github_token)
    api.issues.create_comment(config.issue_number, body=message)


def file_deleted():
    pass
    #  TODO


def on_merge(client):
    update_server(client, config.file, config.namespace)


def build_graph():
    from grai_graph import graph
    from grai_source_flat_file.loader import get_nodes_and_edges
    from grai_source_flat_file.adapters import adapt_to_client
    
    G = graph.Graph()
    nodes, edges = get_nodes_and_edges(config.file, config.namespace)
    nodes = adapt_to_client(nodes)
    G.add_nodes(nodes)
    #G.add_edges(edges)
    return G

def on_pull_request(client):
    from grai_graph import analysis
    from grai_source_flat_file.loader import get_nodes_and_edges
    from grai_source_flat_file.adapters import adapt_to_client
    
    G = client.build_graph()
    analysis = analysis.GraphAnalyzer(G)
    
    nodes, edges = get_nodes_and_edges(config.file, config.namespace)
    nodes = adapt_to_client(nodes)
    for node in nodes:
        new_type = node.spec.metadata['data_type']
        original_node = G.get_node(name=node.spec.name, namespace=node.spec.namespace)
        affected_nodes = analysis.test_type_change(namespace=node.spec.namespace, name=node.spec.name, new_type=new_type)
        node_name = node.spec.name
        # TODO: this is technically wrong
        node_tuple = [(node_name, n.spec.name, n.spec.metadata['data_type'] == new_type) for n in affected_nodes]
        affected_nodes = [(n.spec.name, n.spec.metadata['data_type']) for n in affected_nodes]
        if affected_nodes:
            message = build_message(node_name, node_tuple, affected_nodes)
            post_comment(message)
        else:
            post_comment(f"no affected nodes for {node_name} ")
    


def main():
    if not os.path.exists(config.file):
        raise f"{config.file} does not exist"
    client = ClientV1(config.host, config.port)
    
    client.set_authentication_headers(token=config.grai_auth_token)
    authentication_status = client.check_authentication()
    if authentication_status.status_code != 200:
        raise Exception(f"Authentication to {config.host} failed")
    
    # client.set_authentication_headers(username='null@grai.io', password='super_secret')
    if config.git_event == 'merge':
        return on_merge(client)
    elif config.git_event == 'pull_request':
        return on_pull_request(client)

if __name__ == "__main__":
    main()
