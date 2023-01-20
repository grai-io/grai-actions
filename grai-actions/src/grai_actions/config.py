from enum import Enum
from typing import Optional

from pydantic import AnyUrl, BaseSettings, SecretStr, validator


class SupportedActions(Enum):
    TESTS = "tests"
    UPDATE = "update"


class AccessModes(Enum):
    DBT = "dbt"
    FLAT_FILE = "flat_file"
    TEST_MODE = "test_mode"


DEFAULT_ACCESS_MODE = AccessModes.TEST_MODE.value


class AccessMode(BaseSettings):
    grai_access_mode: AccessModes = DEFAULT_ACCESS_MODE

    class Config:
        use_enum_values = True  # Populates model with the value property of enums


class Config(BaseSettings):
    """Config values are pulled from their corresponding case-insensitive environment variables"""

    # --- Github configs --- #
    github_token: SecretStr
    github_repository_owner: str
    github_repository: str
    github_event_name: str
    pr_number: str

    # ---- Grai configs --- #
    grai_api_key: SecretStr
    grai_namespace: str = "default"
    grai_workspace: Optional[str] = None
    grai_host: str = "api.grai.io"
    grai_port: str = "443"
    grai_frontend_url: Optional[AnyUrl] = None
    grai_action: SupportedActions = SupportedActions.TESTS
    grai_access_mode: AccessModes = DEFAULT_ACCESS_MODE

    @property
    def repo_name(self):
        return self.github_repository.split("/")[-1]

    @validator("grai_frontend_url")
    def validate_grai_frontend_url(cls, value, values):
        if value is None:
            if values["grai_host"] == "api.grai.io":
                return "https://app.grai.io"
            return value
        else:
            return value.rstrip("/")

    class Config:
        """Extra configuration options"""

        anystr_strip_whitespace = True  # remove trailing whitespace
        use_enum_values = True  # Populates model with the value property of enums
        validate_assignment = True  # Perform validation on assignment to attributes


access_mode = AccessMode()
if access_mode.grai_access_mode == AccessModes.TEST_MODE.value:
    default_config = {
        "github_token": "abcde",
        "github_repository_owner": "Grai",
        "github_repository": "grai.io/grai-actions",
        "github_event_name": "pull_request",
        "pr_number": "8675309",
        "grai_api_key": "a-really-secret-key",
    }
    config = Config(**default_config)
else:
    config = Config()
