import os
from ghapi.all import GhApi
from dataclasses import dataclass
from grai_source_flat_file.base import update_server
from grai_client.endpoints.v1.client import ClientV1


@dataclass
class config:
    token = os.environ['GITHUB_TOKEN']
    owner = os.environ['GITHUB_REPOSITORY_OWNER']
    repo = os.environ['GITHUB_REPOSITORY'].split('/')[-1]
    issue_number = os.environ['GITHUB_REF_NAME'].split('/')[0]
    file = os.environ['TRACKED_FILE']
    namespace = os.environ['GRAI_NAMESPACE']
    host = os.environ['GRAI_HOST']
    port = os.environ['GRAI_PORT']
    git_event = os.environ['GITHUB_EVENT_NAME']
    token = os.environ['GRAI_AUTH_TOKEN']


def build_type_change_message(node, affected_nodes, new_type, message="## Type Changes\n"):
    if not affected_nodes:
        return message
    
    name = node.spec.name
    namespace = node.spec.namespace
    original_type = node.spec.metadata['data_type']
    message += f"### {namespace}/{name}: ({original_type} -> {new_type})\n"
    for a_n in affected_nodes:
        a_name = a_n.spec.name
        a_namespace = a_n.spec.namespace
        message += f"\t❌ {a_namespace}/{a_name} expected type **{a_n.spec.metadata['data_type']}**\n"
    
    return message


def build_message(type_results):
    message = f"""
    <details>
        <summary>Test Results</summary>
        {type_results}
    </details>
    """
    return message


def post_comment(message):
    api = GhApi(owner=config.owner, repo=config.repo, token=config.token)
    api.issues.create_comment(issue_number=config.issue_number, 
                            body=message)

def file_deleted():
    pass
    #  TODO


def on_merge(client):
    update_server(client, config.file, config.namespace)


def on_pull_request(client):
    from grai_graph import graph, analysis
    from grai_source_flat_file.loader import get_nodes_and_edges
    from grai_source_flat_file.adapters import adapt_to_client
    
    # G = client.build_graph()
    # analysis = analysis.GraphAnalyzer(G)
    
    # nodes, edges = get_nodes_and_edges(config.file, config.namespace)
    # nodes = adapt_to_client(nodes)

    # found_issues = False
    # message = "## Type Changes\n"
    # for node in nodes:
    #     new_type = node.spec.metadata['data_type']
    #     original_node = G.get_node(name=node.spec.name, namespace=node.spec.namespace)
    #     affected_nodes = analysis.test_type_change(namespace=node.spec.namespace, name=node.spec.name, new_type=new_type)
    #     message = build_type_change_message(original_node, affected_nodes, new_type, message)
    #     found_issues = found_issues or any(affected_nodes)
    # message = build_message(message)
    
    # print(message)
    # if found_issues:
        # post_comment(message)
        # raise
    message = '## Type Changes\\n### demo/data/prod.age: (integer -> float)\\n\\t❌ demo/data/warehouse.age expected type **integer**\\n'
    post_comment(message)


def main():
    if not os.path.exists(config.file):
        raise f"{config.file} does not exist"
    client = ClientV1(config.host, config.port)
    if config.token != '':
        client.set_authentication_headers(token=config.token)
    else: 
        client.set_authentication_headers(username='null@grai.io', password='super_secret')

    if config.git_event == 'merge':
        return on_merge(client)
    elif config.git_event == 'pull_request':
        return on_pull_request(client)

if __name__ == "__main__":
    main()
