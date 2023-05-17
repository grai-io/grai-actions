from grai_source_bigquery import base
from grai_source_bigquery.loader import BigqueryConnector
from pydantic import BaseSettings

from grai_actions.config import config


def get_nodes_and_edges(client):
    conn = BigqueryConnector(
        namespace=config.grai_namespace,
    )

    # Already adapted to client
    nodes, edges = base.get_nodes_and_edges(conn, client.id)
    return nodes, edges
