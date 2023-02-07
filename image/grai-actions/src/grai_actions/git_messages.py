from typing import List, Optional

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


class BotApi:
    def __init__(self):
        self.api = GhApi(
            owner=config.github_repository_owner,
            repo=config.repo_name,
            token=config.github_token.get_secret_value(),
        )
        self.bot_user = self.api.users.get_authenticated()
        self.bot_user_id = self.bot_user["id"]
        self.test_signal_text = '<!-- grai marker text for test comments-->'

    @staticmethod
    def add_comment_identifier(message, identifier):
        return f"{identifier}{message}"

    def get_marked_comment(self, identifier) -> Optional[dict]:
        current_comments = self.api.issues.list_comments(config.pr_number)
        user_comments = (comment for comment in current_comments if comment["user"]["id"] == self.bot_user_id)
        for comment in user_comments:
            if identifier in comment["body"]:
                return comment
        return None

    def create_or_edit_comment(self, message):
        message = self.add_comment_identifier(message, self.test_signal_text)
        marked_comment = self.get_marked_comment(self.test_signal_text)
        if marked_comment is None:
            self.api.issues.create_comment(config.pr_number, body=message)
        else:
            self.api.issues.update_comment(marked_comment["id"], body=message)


def post_comment(message):
    bot = BotApi()
    bot.create_or_edit_comment(message)
