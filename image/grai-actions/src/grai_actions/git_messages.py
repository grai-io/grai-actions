from functools import wraps
from typing import Callable, List, Optional

from ghapi.all import GhApi

from grai_actions.config import config


def collapsable(content, label):
    result = f"""<details><summary>{label}</summary>
<p>

{content}

</p>
</details>"""
    return result


def heading(string, level):
    return f"<h{level}> {string} </h{level}>"


DEFAULT_MESSAGE = """
No Grai data lineage issues detected.
"""


def github_try_catch(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            message = (
                f"There was an issue communicating with the GitHub API. This is most likely an issue with your",
                "github-token permissions. You can find more information about resolving permission errors here:",
                "https://docs.grai.io/tooling/github-actions",
            )
            raise Exception(message) from e

    return inner


class ProtectedGitHubApiEndpoint:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def __getattr__(self, k):
        base_attr = getattr(self.endpoint, k)
        return github_try_catch(base_attr) if isinstance(base_attr, Callable) else base_attr


class BotApi:
    def __init__(self):
        self.api = GhApi(
            owner=config.github_repository_owner,
            repo=config.repo_name,
            token=config.github_token.get_secret_value(),
        )
        self.test_signal_text = "<!-- grai marker text for test comments-->"
        self.protected_issues = ProtectedGitHubApiEndpoint(self.api.issues)

    @staticmethod
    def add_comment_identifier(message, identifier):
        return f"{identifier}{message}"

    def get_marked_comment(self, identifier) -> Optional[dict]:
        current_comments = self.protected_issues.list_comments(config.pr_number)
        # user_comments = (comment for comment in current_comments if comment["user"]["id"] == self.bot_user_id)
        for comment in current_comments:
            if identifier in comment["body"]:
                return comment
        return None

    def create_or_update_comment(self, message: Optional[str]):
        marked_message = self.add_comment_identifier(
            DEFAULT_MESSAGE if message is None else message, self.test_signal_text
        )
        marked_comment = self.get_marked_comment(self.test_signal_text)

        if marked_comment is None:
            self.protected_issues.create_comment(config.pr_number, body=marked_message)
        else:
            if message is None:
                self.protected_issues.delete_comment(marked_comment["id"])
            else:
                self.protected_issues.update_comment(marked_comment["id"], body=marked_message)


def create_or_update_comment(message):
    bot = BotApi()
    bot.create_or_update_comment(message)
