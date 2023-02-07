from typing import Optional

from grai_source_mssql import base
from grai_source_mssql.loader import MsSQLConnector
from pydantic import BaseSettings, validator

from grai_actions.config import config


class Args(BaseSettings):
    grai_mssql_host: str
    grai_mssql_port: Optional[str] = None
    grai_mssql_database: str
    grai_mssql_user: str
    grai_mssql_password: str
    grai_mssql_encrypt: Optional[bool] = None
    grai_mssql_trusted_connection: Optional[bool] = None
    grai_mssql_protocol: str
    grai_mssql_server: Optional[str] = None

    @validator("grai_mssql_encrypt", pre=True)
    def verify_encrypt(cls, value):
        print(f"encrypt:pre: {value}")

        if value == "true":
            return True
        elif value == "false":
            return False

        return None

    @validator("grai_mssql_trusted_connection", pre=True)
    def verify_trusted_connection(cls, value):
        print(f"trusted_connection:pre: {value}")
        if value == "true":
            return True
        elif value == "false":
            return False

        return None

    @validator("grai_mssql_server", pre=True)
    def verify_server(cls, value):
        return None if value == "" else value


args = Args()


def get_nodes_and_edges(client):
    print(f"server: {args.grai_mssql_server}")
    print(f"encrypt: {args.grai_mssql_encrypt}")
    print(f"trusted_connection: {args.grai_mssql_trusted_connection}")

    conn = MsSQLConnector(
        user=args.grai_mssql_user,
        password=args.grai_mssql_password,
        database=args.grai_mssql_database,
        server=args.grai_mssql_server,
        host=args.grai_mssql_host,
        port=args.grai_mssql_port,
        encrypt=args.grai_mssql_encrypt,
        namespace=config.grai_namespace,
        additional_connection_strings=["TrustServerCertificate=yes"] if args.grai_mssql_trusted_connection else None,
    )

    # Already adapted to client
    nodes, edges = base.get_nodes_and_edges(conn, client.id)
    return nodes, edges
