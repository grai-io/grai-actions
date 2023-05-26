import yaml
import os
from tomark import Tomark
import markdown


SHARED_FIELDS = {'action', 'github-token', 'namespace', 'workspace', 'api-key', 'grai-frontend-host', 'client-host', 'client-port'}


class BuildTable:
    def __init__(self, action_folder, ignored_fields=None):
        self.folder = action_folder
        self.ignored_fields = ignored_fields if ignored_fields is not None else SHARED_FIELDS
        self.table_data = self.process_action_yaml()


    @staticmethod
    def build_record(field_name, field_vals):
        record = {
            'Field': field_name,
            'Required': 'yes' if field_vals.get('required', False) else 'no',
            'Default': field_vals.get('default', ''),
            'Description': field_vals.get('description', '')
        }
        return record

    def process_action_yaml(self):
        file = os.path.join(self.folder, "action.yaml")
        data = yaml.safe_load(open(file))
        inputs = data['inputs']

        table_data = []
        for key, vals in inputs.items():
            if key in self.ignored_fields:
                continue
            record = self.build_record(key, vals)
            table_data.append(record)
        return table_data

    def table_description(self):
        return Tomark.table(self.table_data)


folders = ["snowflake", "redshift", "bigquery", "postgres", "mysql", "mssql", "fivetran", "flat-file", "dbt"]

SENTINEL_STRING = "<!-- Fields Sentinel Section -->"
join_string = f"""{SENTINEL_STRING}
"""


for folder in folders:
    table = BuildTable(folder)
    file_string = open(os.path.join(folder, "README.md")).read()
    if SENTINEL_STRING not in file_string:
        raise Exception(f"Sentinel string not found in {folder}")
    result = file_string.split(join_string)
    result[1] = table.table_description()
    result = join_string.join(result)
    with open(os.path.join(folder, "README.md"), "w") as f:
        f.write(result)
