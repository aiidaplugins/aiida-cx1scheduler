from aiida_icl.utils import (get_cx1_computer, get_crystal_code, get_crystal_props_code, JOB_CLASSES,
                             get_calulation_options)


def test_get_cx1_computer(new_database):
    computer = get_cx1_computer('/test/workdir/')
    assert computer.get_workdir() == '/test/workdir/'
    new_computer = get_cx1_computer()
    assert computer.pk == new_computer.pk


def test_get_crystal_code(new_database):
    computer = get_cx1_computer('/test/workdir/')
    code = get_crystal_code(computer)
    assert code.get_input_plugin_name() == 'crystal17.main'
    new_code = get_crystal_code(computer)
    assert code.pk == new_code.pk


def test_get_crystal_props_code(new_database):
    computer = get_cx1_computer('/test/workdir/')
    code = get_crystal_props_code(computer)
    assert code.get_input_plugin_name() == 'crystal17.doss'
    new_code = get_crystal_props_code(computer)
    assert code.pk == new_code.pk


def test_cx1_resources(data_regression):
    options = get_calulation_options(JOB_CLASSES.general_24)
    data_regression.check(options)
