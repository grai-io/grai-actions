import os
from dataclasses import dataclass

from grai_source_dbt import base
from grai_source_dbt.adapters import adapt_to_client


@dataclass
class Args:
    manifest_file: str = os.environ["GRAI_DBT_MANIFEST_FILE"]
    namespace: str = os.environ.get("GRAI_NAMESPACE", "default")


args = Args()
assert os.path.exists(args.manifest_file), f"{args.manifest_file} does not exist"


def get_nodes_and_edges(client):
    nodes, edges = base.get_nodes_and_edges(
        args.manifest_file, args.namespace, client.id
    )
    nodes = adapt_to_client(nodes)
    edges = adapt_to_client(edges)
    return nodes, edges
