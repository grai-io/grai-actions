import os
from dataclasses import dataclass

from grai_source_flat_file import base
from grai_source_flat_file.adapters import adapt_to_client


@dataclass
class Args:
    file: str = os.environ["GRAI_TRACKED_FILE"]
    namespace: str = os.environ.get("GRAI_NAMESPACE", "default")


args = Args()
assert os.path.exists(args.file), f"{args.file} does not exist"


def get_nodes_and_edges(client):
    nodes, edges = base.get_nodes_and_edges(args.file, args.namespace)
    nodes = adapt_to_client(nodes)
    # edges = adapt_to_client(edges)
    return nodes, []
