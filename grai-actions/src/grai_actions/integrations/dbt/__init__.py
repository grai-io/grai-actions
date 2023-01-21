from grai_source_dbt import base
from pydantic import BaseSettings, FilePath

from grai_actions.config import config


class Args(BaseSettings):
    grai_dbt_manifest_file: FilePath


args = Args()


def get_nodes_and_edges(client):
    # Already adapted to client
    nodes, edges = base.get_nodes_and_edges(
        args.grai_dbt_manifest_file.name, config.grai_namespace, client.id
    )
    return nodes, edges
