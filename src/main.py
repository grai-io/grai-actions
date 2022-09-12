import os
from ghapi.all import GhApi
from dataclasses import dataclass


@dataclass
class config:
    token = os.environ['GITHUB_TOKEN']
    owner = os.environ['GITHUB_REPOSITORY_OWNER']
    repo = os.environ['GITHUB_REPOSITORY'].split('/')[-1]
    issue_number = os.environ['GITHUB_REF_NAME'].split('/')[0]
    file = os.environ['TRACKED_FILE']


def build_message():
    message = """
    <details>
        <summary>Clickable comment</summary>
        
        ## Test Heading
        1. A thing
        2. B thing
    </details>
    """
    return message


def post_comment(message):
    api = GhApi(owner=config.owner, repo=config.repo, token=config.token)
    api.issues.create_comment(issue_number=config.issue_number, 
                            body=message)

def file_deleted():
    pass

def main():
    message = build_message()
    if not os.path.exists(config.file):
        


if __name__ == "__main__":
    main()
