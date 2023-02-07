from grai_actions.config import config
from grai_source_mssql import base
from grai_source_mssql.loader import MsSQLConnector
from pydantic import BaseSettings


class Args(BaseSettings):
    grai_mssql_host: str
    grai_mssql_port: str
    grai_mssql_database_name: str
    grai_mssql_user: str
    grai_mssql_password: str
    grai_mssql_encrypt: bool
    grai_mssql_trusted_connection: bool
    grai_mssql_protocol: str
    grai_mssql_server: str


args = Args()


def get_nodes_and_edges(client):
    conn = MsSQLConnector(
        user=args.grai_mssql_user,
        password=args.grai_mssql_password,
        database=args.grai_mssql_database_name,
        server=args.grai_mssql_server,
        host=args.grai_mssql_host,
        port=args.grai_mssql_port,
        encrypt=args.grai_mssql_encrypt,
        namespace=config.namespace,
        additional_connection_strings=["TrustServerCertificate=yes"]
        if args.grai_mssql_trusted_connection
        else None,
    )

    # Already adapted to client
    nodes, edges = base.get_nodes_and_edges(conn, client.id)
    return nodes, edges
