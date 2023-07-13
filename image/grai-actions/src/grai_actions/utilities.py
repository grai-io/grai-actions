import time
from typing import Optional

from grai_client.endpoints.v1.client import ClientV1
from grai_client.endpoints.v1.utils import MockClientV1
from grai_client.integrations.base import GraiIntegrationImplementation

from grai_actions.config import Config, DeveloperActions, config

DevMockClient = MockClientV1


class DevMockIntegration(GraiIntegrationImplementation):
    def __init__(self):
        self.client = DevMockClient()
        self.data_source = "dev_mock"

    def nodes(self):
        return []

    def edges(self):
        return []


def get_client(client_config: Optional[Config] = None) -> ClientV1:
    if client_config is None:
        client_config = config

    if client_config.grai_action == DeveloperActions.DEV_TESTS.value:
        return DevMockClient()

    if client_config.grai_api_key is None:
        if client_config.grai_user is None or client_config.grai_password is None:
            raise ValueError("Must provide either an API key or username and password")

    conn_kwargs = {
        "api_key": client_config.grai_api_key,
        "username": client_config.grai_user,
        "password": client_config.grai_password,
    }
    if client_config.grai_workspace is not None:
        conn_kwargs["workspace"] = client_config.grai_workspace

    for i in range(2):
        try:
            client = ClientV1(url=client_config.grai_url, **conn_kwargs)
            return client
        except:
            time.sleep(3)

        client = ClientV1(url=client_config.grai_url, **conn_kwargs)
        return client
