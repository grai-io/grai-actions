import os


def get_pr_number():
    return os.environ["GITHUB_REF"].split("/")[2]


env_vars = [
    "GRAI_ACCESS_MODE = TEST_MODE",
    "GITHUB_REPOSITORY_OWNER = Grai",
    "GITHUB_REPOSITORY = grai-actions",
    "GRAI_NAMESPACE = default",
    "GRAI_HOST = localhost",
    "GRAI_PORT = 8000",
    "GITHUB_EVENT_NAME = pull_request",
    "GRAI_API_KEY = abc",
    f"PR_NUMBER = {get_pr_number()}",
    "GRAI_WORKSPACE = default",
    "GRAI_FRONTEND_HOST = http://localhost:3000",
]

for env_var in env_vars:
    key, value = [val.strip() for val in env_var.split("=")]
    os.environ.setdefault(key, value)


def run_test():
    from test_tools import get_test_summary

    from grai_actions.git_messages import post_comment

    summary = get_test_summary()
    message = summary.message()
    post_comment(message)


run_test()
