from grai_source_dbt import base
from pydantic import BaseSettings, FilePath

from grai_actions.config import ActionBaseSettings, config


class Args(ActionBaseSettings):
    grai_dbt_manifest_file: FilePath



def get_nodes_and_edges(client, args=None):
    if args is None:
        args = Args()
    # Already adapted to client
    nodes, edges = base.get_nodes_and_edges(str(args.grai_dbt_manifest_file), config.grai_namespace, client.id)
    return nodes, edges
