from typing import Optional

from grai_source_mysql import base
from grai_source_mysql.loader import MySQLConnector

from grai_actions.config import ActionBaseSettings, config


class Args(ActionBaseSettings):
    grai_db_host: str
    grai_db_port: Optional[str] = None
    grai_db_database_name: str
    grai_db_user: str
    grai_db_password: str



def get_nodes_and_edges(client, args=None):
    if args is None:
        args = Args()
    conn = MySQLConnector(
        dbname=args.grai_db_database_name,
        user=args.grai_db_user,
        password=args.grai_db_password,
        host=args.grai_db_host,
        port=args.grai_db_port,
        namespace=config.grai_namespace,
    )

    # Already adapted to client
    nodes, edges = base.get_nodes_and_edges(conn, client.id)
    return nodes, edges
