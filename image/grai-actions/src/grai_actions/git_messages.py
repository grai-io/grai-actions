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


def create_or_edit_comment(pr_number, message):
    pass


def post_comment(message):
    api = GhApi(
        owner=config.github_repository_owner,
        repo=config.repo_name,
        token=config.github_token.get_secret_value(),
    )
    api.issues.create_comment(config.pr_number, body=message)