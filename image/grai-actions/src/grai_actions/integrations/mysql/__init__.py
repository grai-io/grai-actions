from typing import Optional

from grai_source_mysql.base import MySQLIntegration

from grai_actions.config import ActionBaseSettings, config


class Args(ActionBaseSettings):
    grai_db_host: str
    grai_db_port: Optional[str] = None
    grai_db_database_name: str
    grai_db_user: str
    grai_db_password: str


def get_integration(client, args=None):
    if args is None:
        args = Args()

    integration = MySQLIntegration.from_client(
        client=client,
        source=config.grai_source_name,
        namespace=config.grai_namespace,
        host=args.grai_db_host,
        port=args.grai_db_port,
        dbname=args.grai_db_database_name,
        user=args.grai_db_user,
        password=args.grai_db_password,
    )

    return integration
