from grai_source_flat_file import base
from grai_source_flat_file.adapters import adapt_to_client
from pydantic import BaseSettings, FilePath

from grai_actions.config import ActionBaseSettings, config


class Args(ActionBaseSettings):
    grai_flat_file_file: FilePath


def get_nodes_and_edges(client, args=None):
    if args is None:
        args = Args()
    nodes, edges = base.get_nodes_and_edges(str(args.grai_flat_file_file), config.grai_namespace, client.id)
    return nodes, edges
