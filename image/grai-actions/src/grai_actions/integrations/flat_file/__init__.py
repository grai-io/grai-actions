from grai_source_flat_file.base import FlatFileIntegration
from pydantic import BaseSettings, FilePath

from grai_actions.config import ActionBaseSettings, config


class Args(ActionBaseSettings):
    grai_flat_file_file: FilePath


def get_integration(client, args=None):
    if args is None:
        args = Args()

    integration = FlatFileIntegration.from_client(
        client=client,
        source=config.grai_source_name,
        file_name=str(args.grai_flat_file_file),
        namespace=config.grai_namespace,
    )
    return integration
