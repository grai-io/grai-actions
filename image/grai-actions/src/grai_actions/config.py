from enum import Enum
from typing import Literal, Optional, Union

from pydantic import AnyUrl, BaseSettings, SecretStr, root_validator, validator


class ActionBaseSettings(BaseSettings):
    class Config:
        """Extra configuration options"""

        anystr_strip_whitespace = True  # remove trailing whitespace
        use_enum_values = True  # Populates model with the value property of enums
        validate_assignment = True  # Perform validation on assignment to attributes


class SupportedActions(Enum):
    TESTS = "tests"
    UPDATE = "update"


class AccessModes(Enum):
    DBT = "dbt"
    FLAT_FILE = "flat_file"
    POSTGRES = "postgres"
    MYSQL = "mysql"
    SNOWFLAKE = "snowflake"
    TEST_MODE = "test_mode"


class DefaultValues:
    grai_namespace = "default"
    grai_workspace = None
    grai_host = "api.grai.io"
    grai_port = "443"


class Config(ActionBaseSettings):
    # --- Github configuration values --- #
    github_token: SecretStr
    github_repository_owner: str
    github_repository: str
    github_event_name: str
    github_ref: str

    # --- Grai configuration values --- #
    grai_api_key: SecretStr
    grai_namespace: str = DefaultValues.grai_namespace
    grai_workspace: Optional[str] = DefaultValues.grai_workspace
    grai_host: str = DefaultValues.grai_host
    grai_port: str = DefaultValues.grai_port
    grai_frontend_url: Optional[AnyUrl] = None
    grai_action: SupportedActions = SupportedActions.TESTS
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
            if values["grai_host"] == "api.grai.io":
                return "https://app.grai.io"
            return value
        else:
            return value.rstrip("/")

    @root_validator(pre=True)
    def parse_empty_values(cls, values):
        """Empty strings should be treated as missing"""
        new_values = values.copy()
        for k, v in values.items():
            if v == "":
                new_values.pop(k)
        return new_values


config = Config()
