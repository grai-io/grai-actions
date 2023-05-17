from typing import Optional

from grai_source_fivetran import base
from grai_source_fivetran.loader import FiveTranConnector
from pydantic import BaseSettings, Json

from grai_actions.config import config


class NamespaceValues(BaseSettings):
    grai_fivetran_namespace_map: Optional[Json[str, str]] = None


def get_nodes_and_edges(client):
    conn = FiveTranConnector(
        namespaces=NamespaceValues.namespace_map,
        default_namespace=config.grai_namespace,
    )

    # Already adapted to client
    nodes, edges = base.get_nodes_and_edges(conn, client.id)
    return nodes, edges
