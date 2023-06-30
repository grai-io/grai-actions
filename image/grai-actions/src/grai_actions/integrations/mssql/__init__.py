from typing import List, Optional

from grai_source_mssql import base
from grai_source_mssql.loader import MsSQLConnector
from pydantic import SecretStr

from grai_actions.config import ActionBaseSettings, config


def get_integration(client, args=None):
    conn = MsSQLConnector(
        namespace=config.grai_namespace,
    )
    integration = base.MsSQLIntegration(
        client=client,
        source_name=config.source_name,
        namespace=config.grai_namespace,
    )
    return integration
