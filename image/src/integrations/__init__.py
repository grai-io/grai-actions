import os

access_mode = os.environ['GRAI_ACCESS_MODE'].strip()

match access_mode:
    case 'dbt':
        from .dbt import get_nodes_and_edges
        import dbt as integration
    case 'flat-file':
        from .flat_file import get_nodes_and_edges
        import flat_file as integration
    case _:
        # try importing access_mode?
        pass
