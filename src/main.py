import os
from ghapi.all import GhApi
from dataclasses import dataclass
from grai_source_flat_file.base import update_server
from grai_client.endpoints.v1.client import ClientV1


@dataclass
class config:
    token = os.environ['GITHUB_TOKEN']
    owner = os.environ['GITHUB_REPOSITORY_OWNER']
    repo = os.environ['GITHUB_REPOSITORY'].split('/')[-1]
    issue_number = os.environ['GITHUB_REF_NAME'].split('/')[0]
    file = os.environ['TRACKED_FILE']
    namespace = os.environ['GRAI_NAMESPACE']
    host = os.environ['GRAI_HOST']
    port = os.environ['GRAI_PORT']


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
        raise f"{config.file} does not exist"
    
    client = ClientV1(config.host, config.port)
    client.set_authentication_headers(username='null@grai.io', password='super_secret')
    update_server(client, config.file, config.namespace)


if __name__ == "__main__":
    main()
