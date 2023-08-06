# coding: utf-8

from pathlib import Path

import fastgenomics.deprecated as fg_io

HERE = Path(__file__).parent

dir_app = HERE / 'sample_app'
dir_data_1 = HERE / 'sample_data'
dir_data_2 = HERE / 'sample_data_2'


def test_parameters():
    fg_io.set_paths(dir_app, dir_data_1)
    assert fg_io.get_parameter('int_value') == 150
    assert fg_io.get_parameter('str_value') == 'hello from parameters.json'

    fg_io.set_paths(dir_app, dir_data_2)
    assert fg_io.get_parameter('str_value') == 'hello from app 2’s parameters.json'


def test_input_file_mapping():
    fg_io.set_paths(dir_app, dir_data_1)
    assert fg_io.get_input_path('some_input').name == 'input.csv'

    fg_io.set_paths(dir_app, dir_data_2)
    assert fg_io.get_input_path('some_input').name == 'data'


def test_manifest():
    # TODO
    pass
