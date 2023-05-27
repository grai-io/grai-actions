from typing import Optional

from grai_source_bigquery import base
from grai_source_bigquery.loader import BigqueryConnector

from grai_actions.config import config, ActionBaseSettings


class Args(ActionBaseSettings):
    grai_bigquery_project: str
    grai_bigquery_dataset: str
    grai_bigquery_credentials: str


args = Args()


def get_nodes_and_edges(client):
    conn = BigqueryConnector(
        namespace=config.grai_namespace,
        project=args.grai_bigquery_project,
        dataset=args.grai_bigquery_dataset,
        credentials=args.grai_bigquery_credentials,
    )

    # Already adapted to client
    nodes, edges = base.get_nodes_and_edges(conn, client.id)
    return nodes, edges
