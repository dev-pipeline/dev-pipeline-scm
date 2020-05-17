#!/usr/bin/python3
"""This modules does the checkout of code from SCM."""

import argparse

import devpipeline_configure.load
import devpipeline_core.command

import devpipeline_scm
import devpipeline_scm.scm

_MAJOR = 0
_MINOR = 5
_PATCH = 0

_STRING = "{}.{}.{}".format(_MAJOR, _MINOR, _PATCH)


def _configure(parser):
    # parser.add_argument(
    # "--list-scms",
    # action="store_true",
    # default=argparse.SUPPRESS,
    # help="List the available scm tools",
    # )
    devpipeline_core.command.setup_task_parser(parser)
    devpipeline_core.command.add_version_info(parser, _STRING)


def _execute(arguments):
    def _list_scms():
        for scm in sorted(devpipeline_scm.SCMS):
            print("{} - {}".format(scm, devpipeline_scm.SCMS[scm][1]))

    if "list_scms" in arguments:
        _list_scms()
    else:
        devpipeline_core.command.process_tasks(
            arguments,
            [devpipeline_scm.scm.CHECKOUT_TASK],
            devpipeline_configure.load.update_cache,
        )


_SCM_COMMAND = ("Checkout the proper version of the source tree.", _configure, _execute)
