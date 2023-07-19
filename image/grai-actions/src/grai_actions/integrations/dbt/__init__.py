from grai_source_dbt.base import DbtIntegration
from pydantic import BaseSettings, FilePath

from grai_actions.config import ActionBaseSettings, config


class Args(ActionBaseSettings):
    grai_dbt_manifest_file: FilePath


def get_integration(client, args=None):
    if args is None:
        args = Args()

    integration = DbtIntegration.from_client(
        client=client,
        source=config.grai_source_name,
        manifest_file=str(args.grai_dbt_manifest_file),
        namespace=config.grai_namespace,
    )
    return integration
