import os
from dataclasses import dataclass


def validate_item(item, item_name, item_label=None, env_var_label=None):
    if item_label is None:
        item_label = item_name
    if env_var_label is None:
        env_var_label = f"GRAI_{item_name.upper()}"
    message = f"No {item_name} provided, please provide an `{item_label}` value in your workflow or create a `{env_var_label}` secret."
    assert item is not None and item != "", message


@dataclass
class Config:
    github_token = os.environ["GITHUB_TOKEN"]
    owner = os.environ["GITHUB_REPOSITORY_OWNER"]
    repo = os.environ["GITHUB_REPOSITORY"].split("/")[-1]
    namespace = os.environ["GRAI_NAMESPACE"]
    host = os.environ["GRAI_HOST"]
    port = os.environ["GRAI_PORT"]
    git_event = os.environ["GITHUB_EVENT_NAME"]
    api_key = os.environ["GRAI_API_KEY"]
    issue_number = os.environ["PR_NUMBER"]
    workspace = os.environ["GRAI_WORKSPACE"]
    grai_frontend_host = os.environ["GRAI_FRONTEND_HOST"]

    def __post_init__(self):
        self.workspace = None if self.workspace == "" else self.workspace
        self.port = "443" if self.port == "" else self.port

        validate_item(self.api_key, "api-key")
        validate_item(self.github_token, "github-token")
        assert (
            self.api_key is not None and self.api_key != ""
        ), "No api key provided, please provide an `api-key` value in your workflow or create a `GRAI_API_KEY` secret"


config = Config()
