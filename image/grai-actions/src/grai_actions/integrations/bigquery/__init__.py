from typing import Optional

from grai_source_bigquery import base
from grai_source_bigquery.loader import BigQueryIntegration

from grai_actions.config import ActionBaseSettings, config


class Args(ActionBaseSettings):
    grai_bigquery_project: str
    grai_bigquery_dataset: str
    grai_bigquery_credentials: str


def get_integration(client, args=None):
    if args is None:
        args = Args()

    integration = base.BigQueryIntegration(
        client=client,
        source_name=config.source_name,
        namespace=config.grai_namespace,
        project=args.grai_bigquery_project,
        dataset=args.grai_bigquery_dataset,
        credentials=args.grai_bigquery_credentials,
    )

    return integration
