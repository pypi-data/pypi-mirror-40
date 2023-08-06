import logging
import jsonschema

from fastgenomics.app import FGApp
from fastgenomics.data import FGData
from fastgenomics.process import FGProcess


def test_fgapp(app_dir):
    FGApp(app_dir)


def test_app_validation_error(app_dir_validation_error):
    try:
        FGApp(app_dir_validation_error)
    except jsonschema.ValidationError:
        assert True


def test_app_runtime_error(app_dir_runtime_error):
    try:
        FGApp(app_dir_runtime_error)
    except RuntimeError:
        assert True


def test_fgdata_1(data_root):
    FGData(data_root)


def test_fgdata_2(data_root_2):
    FGData(data_root_2)


def test_fgprocess_1(app_dir, data_root, caplog):
    caplog.set_level(logging.DEBUG)
    FGProcess(app_dir, data_root)
    assert any(["Parameters" in x.message for x in caplog.records]), "Parameter logs are not set"


def test_fgprocess_2(app_dir, data_root_2, caplog):
    caplog.set_level(logging.DEBUG)
    FGProcess(app_dir, data_root_2)
    assert any(["Parameters" in x.message for x in caplog.records]), "Parameter logs are not set"
