from grai_source_redshift import base
from grai_source_redshift.loader import RedshiftConnector
from pydantic import BaseSettings

from grai_actions.config import config


def get_nodes_and_edges(client):
    conn = RedshiftConnector(
        namespace=config.grai_namespace,
    )

    # Already adapted to client
    nodes, edges = base.get_nodes_and_edges(conn, client.id)
    return nodes, edges
