from aiida.common import NotExistent
from aiida.orm import Code
from aiida.orm.utils.builders.code import CodeBuilder
from aiida.plugins.entry_point import get_entry_point

_COMPUTER_NAME = 'icl_cx1'
_CRY_CODE_LABEL = 'pcrystal17_v2'
_PROPS_CODE_LABEL = 'pproperties17_v2'
DEFAULT_PCRYSTAL_PATH = ('/rds/general/user/gmallia/home/CRYSTAL17_cx1/v2/bin/Linux-mpiifort_MPP/'
                         'C17-v2_mod_Xeon___mpi__intel-2018___intel-suite__2016.3/Pcrystal')
DEFAULT_PPROPERTIES_PATH = ('/rds/general/user/gmallia/home/CRYSTAL17_cx1/v2/bin/Linux-mpiifort_MPP/'
                            'C17-v2_mod_Xeon___mpi__intel-2018___intel-suite__2016.3/Pproperties')


def get_crystal_code(computer, exec_path=DEFAULT_PCRYSTAL_PATH, modules=('intel-suite/2016.3', 'mpi/intel-5.1')):
    """create a Code node for the CRYSTAL17 code

    Parameters
    ----------
    computer : aiida.orm.Computer
    exec_path : str
        absolute path on the computer, to the crystal executable
    modules : list[str]
        modules to load before execution

    Returns
    -------
    aiida.orm.Code

    """
    try:
        code_cry17 = Code.objects.get(label=_CRY_CODE_LABEL)
    except NotExistent:
        code_builder = CodeBuilder(
            **{
                'label': _CRY_CODE_LABEL,
                'description': 'The CRYSTAL17 code on CX1',
                'code_type': CodeBuilder.CodeType.ON_COMPUTER,
                'computer': computer,
                'prepend_text': 'module load ' + ' '.join(modules),
                'append_text': '',
                'input_plugin': get_entry_point('aiida.calculations', 'crystal17.main'),
                'remote_abs_path': exec_path
            })
        code_cry17 = code_builder.new()
        code_cry17.store()
    return code_cry17


def get_crystal_props_code(computer,
                           exec_path=DEFAULT_PPROPERTIES_PATH,
                           modules=('intel-suite/2016.3', 'mpi/intel-5.1')):
    """create a Code node for the CRYSTAL17 Properties code

    Parameters
    ----------
    computer : aiida.orm.Computer
    exec_path : str
        absolute path on the computer, to the properties executable
    modules : list[str]
        modules to load before execution

    Returns
    -------
    aiida.orm.Code

    """
    try:
        code_props17 = Code.objects.get(label=_PROPS_CODE_LABEL)
    except NotExistent:
        code_builder = CodeBuilder(
            **{
                'label': _PROPS_CODE_LABEL,
                'description': 'The CRYSTAL17 PProperties code on CX1',
                'code_type': CodeBuilder.CodeType.ON_COMPUTER,
                'computer': computer,
                'prepend_text': 'module load ' + ' '.join(modules),
                'append_text': '',
                'input_plugin': get_entry_point('aiida.calculations', 'crystal17.doss'),
                'remote_abs_path': exec_path
            })
        code_props17 = code_builder.new()
        code_props17.store()
    return code_props17
