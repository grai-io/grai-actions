import yaml
import os
from tomark import Tomark
import markdown


SHARED_FIELDS = {'action', 'github-token', 'namespace', 'workspace', 'api-key', 'grai-app-url',
                 'client-host', 'client-port', 'grai-user', 'grai-password'}

SHARED_EXAMPLE_DEFAULTS = {
    'namespace': 'my_apps_grai_namespace',
    'api-key': 'my_grai_api_key',
    'action': 'tests',
}


class BuildDocResults:
    def __init__(self, doc_settings, ignored_fields=None):
        self.doc_settings = doc_settings
        self.folder = self.doc_settings['folder']
        self.ignored_fields = ignored_fields if ignored_fields is not None else SHARED_FIELDS

        file = os.path.join(self.folder, "action.yaml")
        self.data = yaml.safe_load(open(file))

        self.table_data = self.build_table_data()
        self.action_example = self.build_action_example()

    @staticmethod
    def build_record(field_name, field_vals):
        record = {
            'Field': field_name,
            'Required': 'yes' if field_vals.get('required', False) else 'no',
            'Default': field_vals.get('default', ''),
            'Description': field_vals.get('description', '')
        }
        return {k: v if v is not None else '' for k, v in record.items()}

    def build_table_data(self):
        inputs = self.data['inputs']

        table_data = []
        for key, vals in inputs.items():
            if key in self.ignored_fields:
                continue
            record = self.build_record(key, vals)
            table_data.append(record)
        return table_data

    def build_action_example(self):
        with_args = {key: example for key, vals in self.data['inputs'].items()
                     if (example := vals.get('example', None)) is not None}
        with_args = {**SHARED_EXAMPLE_DEFAULTS, **with_args}
        steps = [
            {"name": "Checkout", "uses": "actions/checkout@v3"},
            {"name": "Run Grai Action", "uses": f"grai-io/grai-actions/{self.folder}@master", "with": with_args},
        ]
        base = {
            "on": ["pull_request"],
            "name": self.doc_settings.get('name', self.doc_settings['folder']),
            "jobs": {
                f"test_{self.doc_settings['folder']}": {
                    "runs-on": "ubuntu-latest",
                    "steps": steps
                }
            },
        }
        return base

    def table_description(self):
        return Tomark.table(self.table_data)


with open("./docs/documented.yaml") as f:
    documented = yaml.safe_load(f)['ready']

SENTINEL_STRING = "<!-- Fields Sentinel Section -->"
EXAMPLE_SENTINEL_STRING = "<!-- Example Sentinel Section -->"


for documentation in documented:
    docs = BuildDocResults(documentation)
    file_string = open(os.path.join(docs.folder, "README.md")).read()
    if SENTINEL_STRING not in file_string:
        raise Exception(f"Sentinel string not found in {docs.folder}")

    result = [obj.strip() for obj in file_string.split(SENTINEL_STRING)]
    result[1] = docs.table_description()
    result = f"\n\n{SENTINEL_STRING}\n\n".join(result)

    result = [obj.strip() for obj in file_string.split(EXAMPLE_SENTINEL_STRING)]
    yaml_output = yaml.dump(docs.action_example, sort_keys=False)
    result[1] = f"```yaml copy\n{yaml_output}\n```"
    result = f"\n\n{EXAMPLE_SENTINEL_STRING}\n\n".join(result)

    if result != file_string:
        with open(os.path.join(docs.folder, "README.md"), "w") as f:
            f.write(result)


