from grai_source_flat_file import base
from grai_source_flat_file.adapters import adapt_to_client
from pydantic import BaseSettings, FilePath

from grai_actions.config import config


class Args(BaseSettings):
    grai_tracked_file: FilePath


args = Args()


def get_nodes_and_edges(client):
    nodes, edges = base.get_nodes_and_edges(str(args.grai_tracked_file), config.grai_namespace)
    nodes = adapt_to_client(nodes)
    # edges = adapt_to_client(edges)
    return nodes, []
