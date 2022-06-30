import os
from ghapi.all import GhApi

token = os.environ['INPUT_REPO-TOKEN']
owner = os.environ['GITHUB_REPOSITORY_OWNER']
repo = os.environ['GITHUB_REPOSITORY'].split('/')[-1]
issue_number = os.environ['GITHUB_REF_NAME'].split('/')[0]

message = """
<details>
    <summary>Clickable comment</summary>
    
    ## Test Heading
    1. A thing
    2. B thing
</details>
"""

api = GhApi(owner=owner, repo=repo, token=token)
api.issues.create_comment(issue_number=issue_number, 
                          body=message)

