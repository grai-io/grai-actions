from grai_actions.utilities import get_client


def test_get_client(local_config):
    client = get_client(local_config)


def test_run_update(local_config):
    from grai_actions.integrations.postgres import Args, get_nodes_and_edges

    args = Args(
        grai_db_host='localhost',
        grai_db_port='5433',
        grai_db_database_name='db',
        grai_db_user='grai',
        grai_db_password='grai'
    )
    client = get_client(local_config)

    nodes, edges = get_nodes_and_edges(client, args)

