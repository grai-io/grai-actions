from typing import List, Optional

from grai_source_mssql.base import MsSQLIntegration
from pydantic import SecretStr

from grai_actions.config import ActionBaseSettings, config


def get_integration(client, args=None):
    integration = MsSQLIntegration.from_client(
        client=client,
        source=config.grai_source_name,
        namespace=config.grai_namespace,
    )
    return integration
