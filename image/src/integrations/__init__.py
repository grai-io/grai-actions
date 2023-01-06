import os

access_mode = os.environ['GRAI_ACCESS_MODE'].strip()

match access_mode:
    case 'dbt':
        from .dbt import get_nodes_and_edges
    case 'flat-file':
        from .flat_file import get_nodes_and_edges
    case _:
        # try importing access_mode?
        pass
