from typing import Optional

from grai_source_redshift import base
from grai_source_redshift.loader import RedshiftConnector
from pydantic import SecretStr

from grai_actions.config import ActionBaseSettings, config


class Args(ActionBaseSettings):
    grai_db_host: str
    grai_db_port: Optional[str] = None
    grai_db_database_name: str
    grai_db_user: str
    grai_db_password: SecretStr


args = Args()


def get_nodes_and_edges(client):
    conn = RedshiftConnector(
        namespace=config.grai_namespace,
        user=args.grai_db_user,
        password=args.grai_db_password.get_secret_value(),
        database=args.grai_db_database_name,
        host=args.grai_db_host,
        port=args.grai_db_port,
    )

    # Already adapted to client
    nodes, edges = base.get_nodes_and_edges(conn, client.id)
    return nodes, edges
