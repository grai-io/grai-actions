from grai_source_bigquery.base import BigQueryIntegration

from grai_actions.config import ActionBaseSettings, config


class Args(ActionBaseSettings):
    grai_bigquery_project: str
    grai_bigquery_dataset: str
    grai_bigquery_credentials: str


def get_integration(client, args=None):
    if args is None:
        args = Args()

    integration = BigQueryIntegration.from_client(
        client=client,
        source=config.source_name,
        namespace=config.grai_namespace,
        project=args.grai_bigquery_project,
        dataset=args.grai_bigquery_dataset,
        credentials=args.grai_bigquery_credentials,
    )

    return integration
