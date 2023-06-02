from enum import Enum
from typing import Literal, Optional, Union

from pydantic import AnyUrl, BaseSettings, SecretStr, root_validator, validator


class ActionBaseSettings(BaseSettings):
    class Config:
        """Extra configuration options"""

        anystr_strip_whitespace = True  # remove trailing whitespace
        use_enum_values = True  # Populates model with the value property of enums
        validate_assignment = True  # Perform validation on assignment to attributes

    @root_validator(pre=True)
    def parse_empty_values(cls, values):
        """Empty strings should be treated as missing"""
        new_values = values.copy()
        for k, v in values.items():
            if isinstance(v, SecretStr):
                v = v.get_secret_value()
            if v == "":
                new_values.pop(k)
        return new_values


class DeveloperActions(Enum):
    DEV_TESTS = "dev_tests"


class SupportedActions(Enum):
    TESTS = "tests"
    UPDATE = "update"


class AccessModes(Enum):
    DBT = "dbt"
    FLAT_FILE = "flat_file"
    POSTGRES = "postgres"
    MYSQL = "mysql"
    MSSQL = "mssql"
    SNOWFLAKE = "snowflake"
    TEST_MODE = "test_mode"
    REDSHIFT = "redshift"
    FIVETRAN = "fivetran"
    BIGQUERY = "bigquery"


class DefaultValues:
    grai_namespace = "default"
    grai_workspace = None
    grai_url = "https://api.grai.io"


class Config(ActionBaseSettings):
    # --- Github configuration values --- #
    github_token: SecretStr
    github_repository_owner: str
    github_repository: str
    github_event_name: str
    github_ref: str

    # --- Grai configuration values --- #
    grai_api_key: Optional[SecretStr] = None
    grai_namespace: str = DefaultValues.grai_namespace
    grai_user: Optional[str] = None
    grai_password: Optional[SecretStr] = None
    grai_workspace: Optional[str] = DefaultValues.grai_workspace
    grai_url: str = DefaultValues.grai_url
    grai_frontend_url: Optional[AnyUrl] = None
    grai_action: Union[SupportedActions, DeveloperActions] = SupportedActions.TESTS
    grai_access_mode: AccessModes

    @property
    def repo_name(self):
        return self.github_repository.split("/")[-1]

    @property
    def pr_number(self):
        return self.github_ref.split("/")[2]

    @validator("grai_frontend_url")
    def validate_grai_frontend_url(cls, value, values):
        if value is None:
            if values["grai_url"] == "https://api.grai.io":
                return "https://app.grai.io"
            return value
        else:
            return value.rstrip("/")


config = Config()
