from typing import List, Optional

from grai_source_mssql import base
from grai_source_mssql.loader import MsSQLConnector
from pydantic import SecretStr

from grai_actions.config import config


def get_nodes_and_edges(client):
    conn = MsSQLConnector(
        namespace=config.grai_namespace,
    )

    # Already adapted to client
    nodes, edges = base.get_nodes_and_edges(conn, client.id)
    return nodes, edges
