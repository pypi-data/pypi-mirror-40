import logging

import pytest
import pathlib
import jsonschema
import json

from fastgenomics.app import FGApp
from fastgenomics import deprecated


def test_paths_are_initialized(local):
    deprecated.get_paths()


def test_custom_init_paths(app_dir, data_root):
    deprecated.set_paths(app_dir, data_root)
    deprecated.get_paths()


def test_paths_from_env(fg_env):
    deprecated.get_paths()


def test_cannot_init_nonexisting_paths():
    with pytest.raises(FileNotFoundError):
        deprecated.set_paths("i_don't_exist", "me_neither")


def test_custom_init_path_within_docker(fake_docker, app_dir, data_root):
    with pytest.warns(None):
        deprecated.set_paths(app_dir, data_root)
        deprecated.get_paths()


def test_get_app_manifest(local):
    deprecated.get_app_manifest()


# replaced by test_app_checker
@pytest.mark.skip
def test_assert_manifest_is_valid(local):
    manifest = deprecated.get_app_manifest()
    deprecated.assert_manifest_is_valid(manifest)


# replaced by test_app_{runtime,validation}_error in test_app_checker
@pytest.mark.skip
def test_assert_standard_types(local):
    manifest_file = deprecated.get_paths()['app'] / 'manifest.json'
    config = json.loads(manifest_file.read_bytes())
    config['application']['input']['test'] = {
        'type': 'this_is_a_mistake',
        'usage': 'None'
    }

    try:
        deprecated.assert_manifest_is_valid(config)
    except jsonschema.ValidationError:
        assert True

    config['application']['input']['test'] = {
        'type': 'output_only',
        'usage': 'None'
    }

    try:
        deprecated.assert_manifest_is_valid(config)
    except RuntimeError:
        assert True


def test_can_get_parameters(local):
    parameters = deprecated.get_parameters()
    assert len(parameters) > 0


# no idea what this tests
@pytest.mark.skip
def test_get_paramerets_dont_run_into_recursion(monkeypatch, local):
    monkeypatch.setattr("fastgenomics.deprecated.load_parameters_from_manifest", dict)
    monkeypatch.setattr("fastgenomics.deprecated.load_runtime_parameters", dict)
    io.get_parameters()


def test_parameters(local):
    parameters = deprecated.get_parameters()

    assert "str_value" in parameters
    assert parameters["str_value"] == "hello from parameters.json"

    assert "int_value" in parameters
    assert parameters["int_value"] == 150

    assert "float_value" in parameters
    assert parameters["float_value"] == float(100)

    assert "bool_value" in parameters
    assert parameters["bool_value"] is True

    assert "list_value" in parameters
    assert parameters["list_value"] == [1, 2, 3]

    assert "dict_value" in parameters
    assert parameters["dict_value"] == {"foo": 42, "bar": "answer to everything"}

    assert "optional_int_value_concrete" in parameters
    assert parameters["optional_int_value_concrete"] == 4

    assert "optional_int_value_null" in parameters
    assert parameters["optional_int_value_null"] is None

    assert "enum_value" in parameters
    assert parameters["enum_value"] == "X"

    # moved to test_app_checker because logs are printed at a different time now
    # assert any(["Parameters" in x.message for x in caplog.records]), "Parameter logs are not set"


def test_can_get_specific_parameter(local):
    assert deprecated.get_parameter("int_value") == 150


def test_can_get_null_parameter(local):
    assert deprecated.get_parameter("optional_int_value_null") is None


# I have no idea how runtime parameters are supposed to work
@pytest.mark.skip
def test_can_have_different_type(local, monkeypatch):
    # patch custom parameter load function
    monkeypatch.setattr("fastgenomics.deprecated.load_runtime_parameters", lambda: {"str_value": 1})

    # get parameters and compare parameters of different types
    with pytest.warns(None):
        parameters = deprecated.get_parameters()
        assert 1 == parameters["str_value"]


def test_load_input_file_mapping(local):
    input_file_mapping = deprecated.load_input_file_mapping()
    assert "some_input" in input_file_mapping


def test_input_file_mapping_to_paths(local):
    ifm_dict = deprecated.load_input_file_mapping()
    input_file_mapping = deprecated.str_to_path_file_mapping(ifm_dict)
    assert isinstance(input_file_mapping['some_input'], pathlib.Path)
    assert input_file_mapping['some_input'].exists()


# tests internals, difficult to reproduce in a new implementation
@pytest.mark.skip
def test_check_input_file_mapping(local):
    ifm_dict = deprecated.load_input_file_mapping()
    input_file_mapping = deprecated.str_to_path_file_mapping(ifm_dict)

    # test everything is ok
    deprecated.check_input_file_mapping(input_file_mapping)

    # test if additional keys trigger warning
    input_file_mapping['unused_key'] = pathlib.Path(".")
    with pytest.warns(None):
        deprecated.check_input_file_mapping(input_file_mapping)

    # test raises KeyError on missing entry
    with pytest.raises(KeyError):
        deprecated.check_input_file_mapping({})

    # test raises FileNotFoundError on wrong item
    with pytest.raises(FileNotFoundError):
        deprecated.check_input_file_mapping({"some_input": pathlib.Path("i_don't_exist")})


# should this be supported anyway?
@pytest.mark.skip
def test_load_input_file_mapping_from_env(local, monkeypatch):
    monkeypatch.setenv('INPUT_FILE_MAPPING', '{"some_key_from_env": "some_value"}')
    monkeypatch.setattr('pathlib.Path.exists', lambda self: False if "input_file_mapping.json" in self.name else True)
    input_file_mapping = deprecated.load_input_file_mapping()
    assert "some_input" not in input_file_mapping, "input_file_mapping from file used instead if env!"
    assert "some_key_from_env" in input_file_mapping
    # test if rest of deprecated still works
    _ = deprecated.get_app_manifest()
    _ = deprecated.get_parameters()


def test_get_input_file_mapping(local):
    input_file_mapping = deprecated.get_input_file_mapping()
    assert "some_input" in input_file_mapping
    assert input_file_mapping['some_input'].exists()


# again, should this be supported?
@pytest.mark.skip
def test_get_input_file_mapping_from_env(local, monkeypatch):
    monkeypatch.setenv('INPUT_FILE_MAPPING', '{"some_input": "input.csv", "some_key_from_env": "input.csv"}')
    input_file_mapping = deprecated.get_input_file_mapping()
    assert input_file_mapping['some_key_from_env'].exists()
