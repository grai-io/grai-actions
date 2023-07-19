import pytest

from grai_actions.config import Config


@pytest.fixture
def local_config():
    config = Config(
        github_token="temp",
        github_repository_owner="temp",
        github_repository="temp",
        github_event_name="temp",
        github_ref="temp",
        grai_source_name="a_cool_place",
        grai_password="super_secret",
        grai_user="null@grai.io",
        grai_url="http://localhost:8000",
        grai_frontend_url="http://localhost:3000",
        grai_action="update",
        grai_access_mode="postgres",
        grai_api_key=None,
    )
    return config
