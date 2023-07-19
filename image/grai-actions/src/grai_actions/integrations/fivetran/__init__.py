from typing import Optional

from grai_source_fivetran.base import FivetranIntegration
from pydantic import Json, SecretStr

from grai_actions.config import ActionBaseSettings, config


class Args(ActionBaseSettings):
    grai_fivetran_namespace_map: Optional[Json] = None
    grai_fivetran_api_key: SecretStr
    grai_fivetran_api_secret: SecretStr
    grai_fivetran_endpoint: Optional[str] = None


def get_integration(client, args=None):
    if args is None:
        args = Args()

    integration = FivetranIntegration.from_client(
        client=client,
        source=config.grai_source_name,
        namespaces=args.grai_fivetran_namespace_map,
        default_namespace=config.grai_namespace,
        api_key=args.grai_fivetran_api_key.get_secret_value(),
        api_secret=args.grai_fivetran_api_secret.get_secret_value(),
        endpoint=args.grai_fivetran_endpoint,
    )
    return integration
