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


def mermaid_graph(node_tuples):
    def new_edge(a, b, status):
        return f'{a}-->|"{"✅" if status else "❌"}"| {b};'

    message = f"""```mermaid
graph TD;
    {''.join((new_edge(*tup) for tup in node_tuples))}
```
    """
    return message


def build_table(affected_nodes):
    def make_row(name, dtype):
        row = f"""| {name} | data type | expected {dtype} |
"""
        return row

    rows = "".join([make_row(name, dtype) for name, dtype in affected_nodes])
    message = f"""| Dependency | Test | Message |
| --- | --- | --- |
{rows}
    """
    return message


def build_node_test_summary(name, affected_nodes):
    label = heading(name, 2)
    section = f"""
{heading('Failing Tests', 4)}

{build_table(affected_nodes)}
    """
    return collapsable(section, label)


def build_link(node_name, affected_nodes):
    def node_to_error(name, dtype):
        return {
            "source": node_name,
            "destination": name,
            "type": "data type",
            "message": f"""expected {dtype}""",
        }

    errorList = []

    for name, dtype in affected_nodes:
        errorList.append(node_to_error(name, dtype))

    errors = urllib.parse.quote_plus(json.dumps(errorList))

    return f"""<a href="{config.grai_frontend_host}/workspaces/{config.workspace}/graph?limitGraph=true&errors={errors}" target="_blank">Show Plot</a>"""


def build_message(node_name, node_tuple, affected_nodes):
    return f"""
{mermaid_graph(node_tuple)}

{build_node_test_summary(node_name, affected_nodes)}

{config.grai_frontend_host and build_link(node_name, affected_nodes)}
    """


def post_comment(message):
    api = GhApi(owner=config.owner, repo=config.repo, token=config.github_token)
    api.issues.create_comment(config.issue_number, body=message)
