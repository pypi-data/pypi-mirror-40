from .app import FGApp
from .data import FGData
from .parameters import FGParameters
from .io import Files
from .defaults import DEFAULT_APP_DIR, DEFAULT_DATA_ROOT
from pathlib import Path
from logging import getLogger

logger = getLogger('fastgenomics.common')


class FGProcess(object):
    def __init__(self, app_dir=DEFAULT_APP_DIR, data_dir=DEFAULT_DATA_ROOT):
        self.data = FGData(data_dir)
        self.app = FGApp(app_dir)

        check_input_file_mapping(
            self.data.input_file_mapping, self.app.manifest)

        self.parameters = self.app.default_parameters.copy()
        self.parameters.update(self.data.parameters)

        # log the updated parameter values
        info = "\n".join(f"{k}:{v.value}"
                         for k, v in self.parameters.parameter.items())
        logger.info(f"Parameters: \n{info}")

        self.files = Files(
            self.app.inputs, self.app.outputs,
            self.data.paths['data'], self.data.paths['output'],
            self.data.input_file_mapping)


def check_input_file_mapping(input_file_mapping: Path, manifest: dict):
    """checks the keys in input_file_mapping and existence of the files

    raises a KeyError on missing Key and FileNotFoundError on missing file
    """
    manifest = manifest["application"]['input']

    not_in_manifest = set(input_file_mapping.keys()) - set(manifest.keys())
    not_in_ifm = set(manifest.keys()) - set(input_file_mapping.keys())

    optional = set(
        entry for entry, settings in manifest.items()
        if settings.get('optional', False))

    missing = not_in_ifm - optional

    # check keys
    if not_in_manifest:
        logger.warning(
            f"Ignoring Keys defined in input_file_mapping: {not_in_manifest}")

    if missing:
        raise KeyError(
            f"Non-optional keys not defined in input_file_mapping: {missing}")

    # check for existence
    for key, entry in input_file_mapping.items():
        if not entry.exists():
            if key in optional:
                logger.info(
                    f"Optional file {entry} is not present and may cause an error - be aware!")
            else:
                raise FileNotFoundError(
                    f"{entry}, defined in input_file_mapping, not found!")
