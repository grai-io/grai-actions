from grai_actions.config import AccessModes, config
from grai_actions.utilities import DevMockIntegration

match config.grai_access_mode:
    case AccessModes.DBT.value:
        from .dbt import get_integration
    case AccessModes.FLAT_FILE.value:
        from .flat_file import get_integration
    case AccessModes.POSTGRES.value:
        from .postgres import get_integration
    case AccessModes.MYSQL.value:
        from .mysql import get_integration
    case AccessModes.SNOWFLAKE.value:
        from .snowflake import get_integration
    case AccessModes.MSSQL.value:
        from .mssql import get_integration
    case AccessModes.BIGQUERY.value:
        from .bigquery import get_integration
    case AccessModes.REDSHIFT.value:
        from .redshift import get_integration
    case AccessModes.FIVETRAN.value:
        from .fivetran import get_integration
    case AccessModes.TEST_MODE.value:
        def get_integration(*args, **kwargs):
            return DevMockIntegration()

    case _:
        # try importing access_mode?
        message = f"Unrecognized access mode {config.grai_access_mode}. This is a defensive error indicating the `GRAI_ACCESS_MODE` environment variable has been incorrectly set by an action or overridden by the user."
        raise NotImplementedError(message)
