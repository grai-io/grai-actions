from typing import Optional

from grai_source_mssql import base
from grai_source_mssql.loader import MsSQLConnector
from pydantic import BaseSettings, validator

from grai_actions.config import config


args = Args()


def get_nodes_and_edges(client):
    conn = MsSQLConnector(

        namespace=config.grai_namespace,
        additional_connection_strings=["TrustServerCertificate=yes"],
    )

    # Already adapted to client
    nodes, edges = base.get_nodes_and_edges(conn, client.id)
    return nodes, edges
