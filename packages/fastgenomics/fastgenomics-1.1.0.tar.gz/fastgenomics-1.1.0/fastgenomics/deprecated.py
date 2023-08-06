from .process import FGProcess

_PROCESS = None

def get_process():
    if _PROCESS is None:
        raise NameError(
            f"call set_paths(app_dir, data_root) before accessing the global process.")
    else:
        return _PROCESS


def set_paths(app_dir, data_root):
    global _PROCESS
    _PROCESS = FGProcess(app_dir, data_root)
    _PROCESS.data.paths['app'] = app_dir


def get_parameter(key):
    return get_process().parameters[key]


def get_input_path(filename):
    return get_process().files[filename].path


def get_output_path(filename):
    return get_process().files[filename].path


def get_summary_path():
    return get_process().data.paths['summary'] / "summary.md"


def get_paths():
    return {**get_process().data.paths, 'app': get_process().app.app_dir}


def get_app_manifest():
    return get_process().app.manifest


def get_parameters():
    return {name: param.value
            for name, param in get_process().parameters.parameter.items()}


def load_input_file_mapping():
    return get_process().data.input_file_mapping


def get_input_file_mapping():
    return get_process().data.input_file_mapping


# this is supposed to convert the file mapping names to paths but we
# already do that when constructing input_file_mapping anyway
def str_to_path_file_mapping(ifm_dict):
    return get_process().data.input_file_mapping
