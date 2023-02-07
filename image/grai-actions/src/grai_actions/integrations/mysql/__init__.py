from grai_actions.config import config
from grai_source_mysql import base
from grai_source_mysql.loader import MySQLConnector
from pydantic import BaseSettings


class Args(BaseSettings):
    grai_db_host: str
    grai_db_port: str
    grai_db_database_name: str
    grai_db_user: str
    grai_db_password: str


args = Args()


def get_nodes_and_edges(client):
    conn = MySQLConnector(
        dbname=args.grai_db_database_name,
        user=args.grai_db_user,
        password=args.grai_db_password,
        host=args.grai_db_host,
        port=args.grai_db_port,
        namespace=config.namespace,
    )

    # Already adapted to client
    nodes, edges = base.get_nodes_and_edges(conn, client.id)
    return nodes, edges
