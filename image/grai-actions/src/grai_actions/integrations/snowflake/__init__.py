from typing import Optional

from grai_source_snowflake.base import SnowflakeIntegration

from grai_actions.config import ActionBaseSettings, config


class Args(ActionBaseSettings):
    grai_snowflake_account: str
    grai_db_user: str
    grai_db_password: str
    grai_snowflake_warehouse: str
    grai_snowflake_role: Optional[str] = None
    grai_snowflake_database: Optional[str] = None
    grai_snowflake_schema: Optional[str] = None


def get_integration(client, args=None):
    if args is None:
        args = Args()

    integration = SnowflakeIntegration.from_client(
        client=client,
        source=config.source_name,
        namespace=config.grai_namespace,
        account=args.grai_snowflake_account,
        user=args.grai_db_user,
        password=args.grai_db_password,
        warehouse=args.grai_snowflake_warehouse,
        role=args.grai_snowflake_role,
        database=args.grai_snowflake_database,
        schema=args.grai_snowflake_schema,
    )
    return integration
