from collections import namedtuple
from aiida.common.extendeddicts import AttributeDict

Cx1Resources = namedtuple('Cx1Resources',
                          ('nnodes_min', 'nnodes_max', 'ncpus', 'mem_gb_default', 'mem_gb_max', 'walltime_hrs'))

# See:
# http://www.imperial.ac.uk/admin-services/ict/self-service/research-support/rcs/computing/high-throughput-computing/job-sizing/
JOB_CLASSES = AttributeDict({
    'throughput_24': Cx1Resources(1, 1, 8, 10, 96, 24),
    'throughput_72': Cx1Resources(1, 1, 8, 10, 96, 72),
    'general_24': Cx1Resources(1, 16, 32, 10, 62, 24),
    'general_72': Cx1Resources(1, 16, 32, 10, 62, 72),
    'singlenode_24': Cx1Resources(1, 1, 48, 10, 124, 24),
    'multinode_24': Cx1Resources(3, 16, 12, 10, 46, 24),
    'multinode_48': Cx1Resources(3, 16, 12, 10, 46, 48),
    'debug': Cx1Resources(1, 1, 8, 10, 96, 0.5)
})


def get_calulation_options(resources, nnodes=None, queue=None, mem_gb=None):
    # type: (Cx1Resources, int, str) -> dict
    """ return dict to parse to calculation `metadata.options`
    """
    assert isinstance(resources, Cx1Resources)
    if nnodes is None:
        nnodes = resources.nnodes_min
    assert resources.nnodes_min <= nnodes <= resources.nnodes_max
    if mem_gb is None:
        mem_gb = resources.mem_gb_default
    assert 1 <= mem_gb <= resources.mem_gb_max

    options = {
        'resources': {
            'num_machines': int(nnodes),
            'num_mpiprocs_per_machine': resources.ncpus,
        },
        'max_memory_kb': int(mem_gb * 1e6),
        'max_wallclock_seconds': int(resources.walltime_hrs * 3600),
        'withmpi': True,
    }

    if queue is not None:
        options['queue_name'] = queue

    return options
