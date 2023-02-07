from grai_actions.config import config
from grai_source_dbt import base
from pydantic import BaseSettings, FilePath


class Args(BaseSettings):
    grai_dbt_manifest_file: FilePath


args = Args()


def get_nodes_and_edges(client):
    # Already adapted to client
    nodes, edges = base.get_nodes_and_edges(
        str(args.grai_dbt_manifest_file), config.grai_namespace, client.id
    )
    return nodes, edges
