from grai_actions.config import AccessModes, config

match config.grai_access_mode:
    case AccessModes.DBT.value:
        from .dbt import get_nodes_and_edges
    case AccessModes.FLAT_FILE.value:
        from .flat_file import get_nodes_and_edges
    case AccessModes.POSTGRES.value:
        from .postgres import get_nodes_and_edges
    case AccessModes.MYSQL.value:
        from .mysql import get_nodes_and_edges
    case AccessModes.SNOWFLAKE.value:
        from .snowflake import get_nodes_and_edges
    case AccessModes.MSSQL.value:
        from .mssql import get_nodes_and_edges
    case AccessModes.BIGQUERY.value:
        from .bigquery import get_nodes_and_edges
    case AccessModes.REDSHIFT.value:
        from .redshift import get_nodes_and_edges
    case AccessModes.FIVETRAN.value:
        from .fivetran import get_nodes_and_edges
    case AccessModes.TEST_MODE.value:

        def get_nodes_and_edges(*args, **kwargs):
            return [], []

    case _:
        # try importing access_mode?
        message = f"Unrecognized access mode {config.grai_access_mode}. This is a defensive error indicating the `GRAI_ACCESS_MODE` environment variable has been incorrectly set by an action or overridden by the user."
        raise NotImplementedError(message)
