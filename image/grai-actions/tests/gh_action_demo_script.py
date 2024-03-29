import os

env_vars = [
    "GRAI_ACCESS_MODE = test_mode",
    "GITHUB_REPOSITORY_OWNER = Grai",
    "GITHUB_REPOSITORY = grai-actions",
    "GITHUB_EVENT_NAME = pull_request",
    "GRAI_SOURCE_NAME = a_cool_source",
    "GRAI_API_KEY = abc",
]

for env_var in env_vars:
    key, value = [val.strip() for val in env_var.split("=")]
    os.environ.setdefault(key, value)


def run_test():
    from test_tools import get_test_summary

    from grai_actions.git_messages import create_or_update_comment

    summary = get_test_summary()
    message = summary.message()
    create_or_update_comment(message)


run_test()
