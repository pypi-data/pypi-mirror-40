from pathlib import Path
import json

from .defaults import DEFAULT_DATA_ROOT


class FGData(object):
    """This class stores the paths to data structured according to the
fastgenomics specification.  It also loads the input file mappings and
checks if the files exist.

    """

    _subdirs = ["data", "config", "output", "summary"]

    def __init__(self, data_root=DEFAULT_DATA_ROOT):
        if isinstance(data_root, str):
            data_root = Path(data_root)

        self.root = data_root
        self.paths = self.get_paths()
        self.input_file_mapping = self.get_input_file_mapping()
        self.parameters = self.get_parameters()

    def get_input_file_mapping(self):
        mapping_file = self.paths['config'] / "input_file_mapping.json"

        mapping = json.loads(mapping_file.read_bytes())

        # convert to absolute paths and check for existence
        for f, rel_path in mapping.items():

            abs_path = self.paths['data'] / rel_path
            if not abs_path.exists():
                raise FileNotFoundError(
                    f"File {f} from input_file_mapping.json not found in {self.paths['data']}.")
            mapping[f] = abs_path

        return mapping

    def get_paths(self):
        return {dir: self.root / dir for dir in self._subdirs}

    def get_parameters(self):
        params_file = self.paths['config'] / "parameters.json"
        if params_file.exists():
            return json.loads(params_file.read_bytes())
        else:
            return {}
