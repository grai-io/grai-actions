from typing import Optional

from grai_source_snowflake import base
from grai_source_snowflake.loader import SnowflakeConnector

from grai_actions.config import config, ActionBaseSettings


class Args(ActionBaseSettings):
    grai_snowflake_account: str
    grai_db_user: str
    grai_db_password: str
    grai_snowflake_warehouse: str
    grai_snowflake_role: Optional[str] = None
    grai_snowflake_database: Optional[str] = None
    grai_snowflake_schema: Optional[str] = None


args = Args()


def get_nodes_and_edges(client):
    conn = SnowflakeConnector(
        account=args.grai_snowflake_account,
        user=args.grai_db_user,
        password=args.grai_db_password,
        warehouse=args.grai_snowflake_warehouse,
        role=args.grai_snowflake_role,
        database=args.grai_snowflake_database,
        schema=args.grai_snowflake_schema,
        namespace=config.grai_namespace,
    )

    # Already adapted to client
    nodes, edges = base.get_nodes_and_edges(conn, client.id)
    return nodes, edges
