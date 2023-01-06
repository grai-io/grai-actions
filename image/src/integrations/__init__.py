import os


match os.environ['GRAI_ACCESS_MODE']:
    case ['dbt']:
        from dbt import get_nodes_and_edges
        import dbt as integration
    case ['flat_file']:
        from flat_file import get_nodes_and_edges
        import flat_file as integration
