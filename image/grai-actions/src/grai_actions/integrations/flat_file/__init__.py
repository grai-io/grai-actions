from grai_source_flat_file import base
from grai_source_flat_file.adapters import adapt_to_client
from pydantic import BaseSettings, FilePath

from grai_actions.config import ActionBaseSettings, config


class Args(ActionBaseSettings):
    grai_flat_file_file: FilePath


def get_integration(client, args=None):
    if args is None:
        args = Args()

    integration = base.FlatFileIntegration(
        client=client,
        source_name=config.source_name,
        file_name=str(args.grai_flat_file_file),
        namespace=config.grai_namespace,
    )
    return integration
