import jsonschema
import json
from logging import getLogger
from pathlib import Path

from .defaults import DEFAULT_APP_DIR
from .parameters import FGParameters
from ._resources import resource_bytes

logger = getLogger('fastgenomics.common')


class FGApp(object):
    # files that are checked for existence that are not otherwise
    # explicitly used by the FGApp
    _mandatory_files = ["LICENSE", "LICENSE-THIRD-PARTY"]

    def __init__(self, app_dir=DEFAULT_APP_DIR):
        if isinstance(app_dir, str):
            app_dir = Path(app_dir)

        self.app_dir = app_dir
        self.manifest = self.get_manifest()
        self.default_parameters = FGParameters(
            self.manifest["application"]["parameters"])
        self.app_type = self.manifest["application"]["type"]
        self.inputs = self.manifest['application']['input']
        self.outputs = self.manifest['application']['output']
        assert self.app_type in ["Calculation", "Visualization"]

        self.check_files()

    def get_manifest(self):
        manifest_file = self.app_dir / "manifest.json"
        assert manifest_file.exists()
        manifest = json.loads(manifest_file.read_bytes())
        check_manifest(manifest)
        return manifest

    def check_files(self):
        for f in self._mandatory_files:
            absolute_path = self.app_dir / f
            if not absolute_path.exists():
                raise FileNotFoundError(f"{f} not found in the app directory!")


def check_manifest(config: dict):
    """
    Asserts that the manifest (``manifest.json``) matches our JSON-Schema.
    If not a :py:exc:`jsonschema.ValidationError` will be raised.
    """

    schema = json.loads(resource_bytes('schemes/manifest_schema.json'))
    jsonschema.validate(config, schema)

    input_types = config["application"]["input"]
    output_types = config["application"]["output"]

    def err_msg(x, y):
        return "'{}'-type not supported for {}-operations.".format(x, y)

    if input_types is not None:
        for name, properties in input_types.items():
            if properties["type"] == "output_only":
                raise RuntimeError(err_msg(properties["type"], "input"))

    if output_types is not None:
        for name, properties in output_types.items():
            if properties["type"] == "dataset_manifest":
                raise RuntimeError(err_msg(properties["type"], "output"))
