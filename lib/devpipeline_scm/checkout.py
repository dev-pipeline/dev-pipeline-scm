#!/usr/bin/python3
"""This modules does the checkout of code from SCM."""

import argparse

import devpipeline_configure.load
import devpipeline_core.command

import devpipeline_scm
import devpipeline_scm.scm


def _list_scms():
    for scm in sorted(devpipeline_scm.SCMS):
        print("{} - {}".format(scm, devpipeline_scm.SCMS[scm][1]))


_MAJOR = 0
_MINOR = 5
_PATCH = 0

_STRING = "{}.{}.{}".format(_MAJOR, _MINOR, _PATCH)


class CheckoutCommand(devpipeline_core.command.TaskCommand):
    """
    Provide the checkout command to dev-pipeline.
    """

    def __init__(self, config_fn):
        super().__init__(
            config_fn=config_fn,
            tasks=[devpipeline_scm.scm.CHECKOUT_TASK],
            prog="dev-pipeline checkout",
            description="Checkout repositories",
        )
        self.add_argument(
            "--list-scms",
            action="store_true",
            default=argparse.SUPPRESS,
            help="List the available scm tools",
        )
        self.set_version(_STRING)

    def process(self, arguments):
        if "list_scms" in arguments:
            _list_scms()
        else:
            super().process(arguments)


def main(args=None, config_fn=devpipeline_configure.load.update_cache):
    # pylint: disable=missing-docstring
    checkout = CheckoutCommand(config_fn)
    devpipeline_core.command.execute_command(checkout, args)


_SCM_COMMAND = (main, "Checkout the proper version of the source tree.")

if __name__ == "__main__":
    main()
