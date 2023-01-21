from enum import Enum
from typing import Literal, Optional, Union

from pydantic import AnyUrl, BaseSettings, SecretStr, validator


class ConcatenateableSecretStr(SecretStr):
    """Required for GHapi to work correctly"""

    def __radd__(self, value):
        return str(self) + value


class ActionBaseSettings(BaseSettings):
    class Config:
        """Extra configuration options"""

        anystr_strip_whitespace = True  # remove trailing whitespace
        use_enum_values = True  # Populates model with the value property of enums
        validate_assignment = True  # Perform validation on assignment to attributes


class CaseInsensitiveEnum(Enum):
    @classmethod
    def __missing__(cls, value):
        value = value.lower()
        for member in cls:
            if member.value == value:
                return member
        return None


class SupportedActions(CaseInsensitiveEnum):
    TESTS = "tests"
    UPDATE = "update"


class AccessModes(CaseInsensitiveEnum):
    DBT = "dbt"
    FLAT_FILE = "flat_file"
    TEST_MODE = "test_mode"


class Config(ActionBaseSettings):
    # --- Github configuration values --- #
    github_token: str
    github_repository_owner: str
    github_repository: str
    github_event_name: str
    github_ref: str
    pr_number: str

    # --- Grai configuration values --- #
    grai_api_key: str
    grai_namespace: str = "default"
    grai_workspace: Optional[str] = None
    grai_host: str = "api.grai.io"
    grai_port: str = "443"
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


config = Config()
