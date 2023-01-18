import os

access_mode = os.environ["GRAI_ACCESS_MODE"].strip()

match access_mode:
    case "dbt":
        from .dbt import get_nodes_and_edges
    case "flat-file":
        from .flat_file import get_nodes_and_edges
    case "TEST_MODE":

        def get_nodes_and_edges(*args, **kwargs):
            return [], []

    case _:
        # try importing access_mode?
        message = f"Unrecognized access mode {access_mode}. This is a defensive error indicating the `GRAI_ACCESS_MODE` environment variable has been incorrectly set by an action or overridden by the user."
        raise NotImplementedError(message)
