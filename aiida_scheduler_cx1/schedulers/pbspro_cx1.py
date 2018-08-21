# -*- coding: utf-8 -*-
###########################################################################
# Copyright (c), The AiiDA team. All rights reserved.                     #
# This file is part of the AiiDA code.                                    #
#                                                                         #
# The code is hosted on GitHub at https://github.com/aiidateam/aiida_core #
# For further information on the license, see the LICENSE.txt file        #
# For further information please visit http://www.aiida.net               #
###########################################################################
"""
Plugin for PBSPro.
This has been tested on PBSPro v. 12.
"""
from __future__ import division

import logging

from aiida.scheduler.plugins.pbsbaseclasses import PbsBaseClass

_LOGGER = logging.getLogger(__name__)

# This maps PbsPro status letters to our own status list

## List of states from the man page of qstat
# B  Array job has at least one subjob running.
# E  Job is exiting after having run.
# F  Job is finished.
# H  Job is held.
# M  Job was moved to another server.
# Q  Job is queued.
# R  Job is running.
# S  Job is suspended.
# T  Job is being moved to new location.
# U  Cycle-harvesting job is suspended due to  keyboard  activity.
# W  Job is waiting for its submitter-assigned start time to be reached.
# X  Subjob has completed execution or has been deleted.


# class Pbscx1JobResource(NodeNumberJobResource):
#     def __init__(self, *args, **kwargs):
#         """
#         It extends the base class init method and calculates the
#         num_cores_per_machine fields to pass to PBSlike schedulers.
#
#         Checks that num_cores_per_machine is a multiple of
#         num_cores_per_mpiproc and/or num_mpiprocs_per_machine
#
#         Check sequence
#
#         1. If num_cores_per_mpiproc and num_cores_per_machine both are
#            specified check whether it satisfies the check
#         2. If only num_cores_per_mpiproc is passed, calculate
#            num_cores_per_machine
#         3. If only num_cores_per_machine is passed, use it
#         """
#         super(Pbscx1JobResource, self).__init__(*args, **kwargs)
#
#         value_error = ("num_cores_per_machine must be equal to "
#                        "num_cores_per_mpiproc * num_mpiprocs_per_machine, "
#                        "and in perticular it should be a multiple of "
#                        "num_cores_per_mpiproc and/or num_mpiprocs_per_machine")
#
#         if (self.num_cores_per_machine is not None and
#                     self.num_cores_per_mpiproc is not None):
#             if self.num_cores_per_machine != (self.num_cores_per_mpiproc
#                                                   * self.num_mpiprocs_per_machine):
#                 # If user specify both values, check if specified
#                 # values are correct
#                 raise ValueError(value_error)
#         elif self.num_cores_per_mpiproc is not None:
#             if self.num_cores_per_mpiproc < 0:
#                 raise ValueError("num_cores_per_mpiproc must be >=0")
#             # calculate num_cores_per_machine
#             # In this plugin we never used num_cores_per_mpiproc so if it
#             # is not defined it is OK.
#             self.num_cores_per_machine = (self.num_cores_per_mpiproc
#                                           * self.num_mpiprocs_per_machine)


class Pbscx1Scheduler(PbsBaseClass):
    """
    Subclass to support the PBSPro scheduler
    (http://www.pbsworks.com/).
    But altered to fit the Imperial College London cx1 scheduler spec

    I redefine only what needs to change from the base class
    """

    ## I don't need to change this from the base class
    # _job_resource_class = PbsJobResource

    ## For the time being I use a common dictionary, should be sufficient
    ## for the time being, but I can redefine it if needed.
    # _map_status = _map_status_pbs_common

    def _get_resource_lines(self, num_machines, num_mpiprocs_per_machine,
                            num_cores_per_machine, max_memory_kb, max_wallclock_seconds):
        """
        Return the lines for machines, memory and wallclock relative
        to pbspro.
        """
        # Note: num_cores_per_machine is not used here but is provided by
        #       the parent class ('_get_submit_script_header') method

        return_lines = []

        select_string = "select={}".format(num_machines)
        if num_cores_per_machine:
            select_string += ":ncpus={}".format(num_cores_per_machine)
        else:
            raise ValueError("ncpus must be greater than 0! It is instead '{}'"
                    "".format((num_cores_per_machine)))
        # if num_mpiprocs_per_machine:
        #     select_string += ":mpiprocs={}".format(num_mpiprocs_per_machine)

        if max_wallclock_seconds is not None:
            try:
                tot_secs = int(max_wallclock_seconds)
                if tot_secs <= 0:
                    raise ValueError
            except ValueError:
                raise ValueError(
                    "max_wallclock_seconds must be "
                    "a positive integer (in seconds)! It is instead '{}'"
                    "".format(max_wallclock_seconds))
            hours = tot_secs // 3600
            tot_minutes = tot_secs % 3600
            minutes = tot_minutes // 60
            seconds = tot_minutes % 60
            return_lines.append("#PBS -l walltime={:02d}:{:02d}:{:02d}".format(
                hours, minutes, seconds))

        if max_memory_kb:
            try:
                virtualMemoryKb = int(max_memory_kb)
                if virtualMemoryKb <= 0:
                    raise ValueError
            except ValueError:
                raise ValueError(
                    "max_memory_kb must be "
                    "a positive integer (in kB)! It is instead '{}'"
                    "".format((max_memory_kb)))
            select_string += ":mem={}kb".format(virtualMemoryKb)

        return_lines.append("#PBS -l {}".format(select_string))
        return return_lines
