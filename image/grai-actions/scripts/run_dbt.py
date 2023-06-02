import os

env_vars = [
    "GRAI_ACCESS_MODE = dbt",
    "GITHUB_REPOSITORY_OWNER = Grai",
    "GITHUB_REPOSITORY = grai-actions",
    "GITHUB_EVENT_NAME = pull_request",
    "GITHUB_TOKEN = abc",
    "GITHUB_REF = 'abc/123/itseasy",
    "GRAI_API_KEY = vEew4z8d.a8oczWuXBvDgvJRHGZ0pFl9JGZvOZjxj",
    "GRAI_DBT_MANIFEST_FILE = /Users/ian/repos/grai/grai-actions/image/grai-actions/tests/manifest.json",
    "GRAI_ACTION = update",
    "GRAI_WORKSPACE = default",  # e92d10a1-72b7-45ed-bc88-642465426f04",
    "GRAI_URL = http://localhost:8000",
]

for env_var in env_vars:
    key, value = [val.strip() for val in env_var.split("=")]
    os.environ.setdefault(key, value)


def run_test():
    from grai_actions.config import config
    from grai_actions.tools import TestResultCache
    from grai_actions.utilities import get_client

    client = get_client()
    results = TestResultCache(client)

    for result in results.messages():
        print(result)


def run_update():
    from grai_actions.main import run_update_server
    from grai_actions.utilities import get_client

    client = get_client()

    run_update_server(client)


run_update()
run_test()
