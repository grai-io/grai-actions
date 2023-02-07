from typing import Optional

from grai_actions.config import Config, config
from grai_client.endpoints.v1.client import ClientV1


def get_client(client_config: Optional[Config] = None) -> ClientV1:
    if client_config is None:
        client_config = config

    conn_kwargs = {}
    if client_config.grai_workspace is not None:
        conn_kwargs["workspace"] = client_config.grai_workspace

    client = ClientV1(client_config.grai_host, client_config.grai_port, **conn_kwargs)
    client.set_authentication_headers(
        api_key=client_config.grai_api_key.get_secret_value()
    )

    authentication_status = client.check_authentication()
    if authentication_status.status_code != 200:
        raise Exception(f"Authentication to {client_config.grai_host} failed")

    return client
