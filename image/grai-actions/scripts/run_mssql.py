import os

env_vars = [
    "GRAI_ACCESS_MODE = mssql",
    "GITHUB_REPOSITORY_OWNER = Grai",
    "GITHUB_REPOSITORY = grai-actions",
    "GITHUB_EVENT_NAME = pull_request",
    "GITHUB_TOKEN = abc",
    "GITHUB_REF = 'abc/123/itseasy",
    "GRAI_API_KEY = EctPQthl.gCEe0Baizw2etVqYkNc2l3sUNBTGCFKK",
    "GRAI_MSSQL_HOST = localhost",
    "GRAI_MSSQL_USER = sa",
    "GRAI_MSSQL_PASSWORD = GraiGraiGr4i",
    "GRAI_MSSQL_ENCRYPT = false",
    "GRAI_ACTION = tests",
    "GRAI_WORKSPACE = a9db1460-dc0f-46e3-a142-3bd8a51335fa",
    "GRAI_HOST = api.grai.io",
    "GRAI_PORT = 443",
]

for env_var in env_vars:
    key, value = [val.strip() for val in env_var.split("=")]
    os.environ.setdefault(key, value)


def run_test():
    from grai_actions.config import config
    from grai_actions.tools import TestResultCache
    from grai_actions.utilities import get_client

    # breakpoint()
    client = get_client()
    results = TestResultCache(client)
    breakpoint()



def run_update():
    from grai_actions.main import run_update_server
    from grai_actions.utilities import get_client

    client = get_client()

    run_update_server(client)


#run_update()
run_test()
