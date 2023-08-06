# coding: utf-8

from pathlib import Path


class Files(object):
    def __init__(self, inputs: dict, outputs: dict,
                 input_dir: Path, output_dir: Path,
                 input_mapping: dict):
        self.files = {}
        for name, spec in outputs.items():
            self.files[name] = FileOutput(name, spec, output_dir)

        for name, spec in inputs.items():
            self.files[name] = FileInput(name, spec, input_dir, input_mapping)

    def __getitem__(self, key):
        return self.files[key]

    def __contains__(self, key):
        return key in self.files


class File(object):
    def __init__(self, name, spec):
        self.name = name
        try:
            self.type = spec['type']
            self.usage = spec['usage']
        except KeyError:
            raise KeyError(
                f"File {self.name} is missing a required field (type or usage) in manifest.json.")

    def raise_if_not_exists(self):
        if not self.path.exists():
            raise FileNotFoundError(f"File {self.name}: not found under {self.path}")


class FileInput(File):
    def __init__(self, name, spec, root, mapping):
        super().__init__(name, spec)

        self.optional = spec.get('optional', False)

        if name not in mapping:
            if self.optional:
                self.path = None
            else:
                raise KeyError(f"File {name}: not found in input_file_mapping.json")
        else:
            self.path = root / mapping[name]
            self.raise_if_not_exists()


class FileOutput(File):
    def __init__(self, name, spec, root):
        super().__init__(name, spec)
        self.path = root / spec['file_name']
