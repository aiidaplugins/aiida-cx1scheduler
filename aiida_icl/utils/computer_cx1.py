from aiida.common import NotExistent
from aiida.orm import Computer
from aiida.orm.utils.builders.computer import ComputerBuilder

_COMPUTER_NAME = 'icl_cx1'


def get_cx1_computer(work_dir=None, key_filename=None):
    """get or create a Computer node, to interface with the ICL Cx1 HPC

    Parameters
    ----------
    work_dir :str
        absolute path to the work directory
    key_filename : str
        ssh key filename, e.g. /Users/user_name/.ssh/id_rsa

    Returns
    -------
    aiida.orm.Computer

    """
    try:
        computer_cx1 = Computer.objects.get(name=_COMPUTER_NAME)
    except NotExistent:
        if work_dir is None:
            raise ValueError('work_dir not specified')
        computer_builder = ComputerBuilder(
            label=_COMPUTER_NAME,
            description='Imperial HPC cx1 computer',
            transport='ssh',
            scheduler='pbspro_cx1',
            hostname='login.cx1.hpc.ic.ac.uk',
            prepend_text='',
            append_text='',
            work_dir=work_dir,
            shebang='#!/bin/bash',
            mpiprocs_per_machine=16,
            mpirun_command='mpiexec')
        computer_cx1 = computer_builder.new()
        computer_cx1.store()
        computer_cx1.configure(
            look_for_keys=True,
            key_filename=key_filename,
            timeout=60,
            allow_agent=True,
            compress=True,
            load_system_host_keys=True,
            safe_interval=5.0)
    return computer_cx1
