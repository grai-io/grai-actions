from typing import Optional

from grai_source_fivetran import base
from grai_source_fivetran.loader import FivetranConnector
from pydantic import Json, SecretStr

from grai_actions.config import config, ActionBaseSettings


class Args(ActionBaseSettings):
    grai_fivetran_namespace_map: Optional[Json] = None
    grai_fivetran_api_key: SecretStr
    grai_fivetran_api_secret: SecretStr
    grai_fivetran_endpoint: Optional[str] = None


args = Args()


def get_nodes_and_edges(client):
    conn = FivetranConnector(
        endpoint=args.grai_fivetran_endpoint,
        api_key=args.grai_fivetran_api_key.get_secret_value(),
        api_secret=args.grai_fivetran_api_secret.get_secret_value(),
        namespaces=args.grai_fivetran_namespace_map,
        default_namespace=config.grai_namespace,
    )

    # Already adapted to client
    nodes, edges = base.get_nodes_and_edges(conn, client.id)
    return nodes, edges
