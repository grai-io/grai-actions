from typing import Optional

from grai_source_redshift import base
from grai_source_redshift.loader import RedshiftConnector
from pydantic import SecretStr

from grai_actions.config import config


class Args(config.ActionBaseSettings):
    grai_db_user: str
    grai_db_password: Optional[SecretStr]
    grai_redshift_database: str
    grai_redshift_host: str
    grai_redshift_port: Optional[int] = None


args = Args()


def get_nodes_and_edges(client):
    conn = RedshiftConnector(
        namespace=config.grai_namespace,
        user=args.grai_db_user,
        password=args.grai_db_password,
        database=args.grai_redshift_database,
        host=args.grai_redshift_host,
        port=args.grai_redshift_port,
    )

    # Already adapted to client
    nodes, edges = base.get_nodes_and_edges(conn, client.id)
    return nodes, edges
