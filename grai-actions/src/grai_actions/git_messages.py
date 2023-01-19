import json
import urllib
from urllib import parse

from ghapi.all import GhApi

from .config import config


def collapsable(content, label):
    result = f"""<details><summary>{label}</summary>
<p>

{content}

</p>
</details>"""
    return result


def heading(string, level):
    return f"<h{level}> {string} </h{level}>"


def post_comment(message):
    api = GhApi(owner=config.owner, repo=config.repo, token=config.github_token)
    api.issues.create_comment(config.issue_number, body=message)
