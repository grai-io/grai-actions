# from grai_actions.utilities import get_client
# from grai_client.endpoints.v1.client import ClientV1
# from grai_actions.config import Config
import uuid


def is_valid_uuid(string):
    try:
        uuid.UUID(string)
        return True
    except ValueError:
        return False


# def test_build_client():
#     config = Config()
#     config.host = "api.grai.io"
#     client = get_client()
#     assert isinstance(client, ClientV1)


# def test_get_workspace_id():
#     config = Config(grai_workspace='default')
#     config.grai_workspace = 'default'
#     config.grai_api_key = 'm4S9p5qY.gbr9nd6Bs1qP8fUJIRWIaeqTEf7vPsh4'
#     #client = get_client(config)
#
#     #assert is_valid_uuid(client.workspace), "Client did not pull a UUID for the default workspace as expected"
#
