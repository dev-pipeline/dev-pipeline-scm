#!/usr/bin/python3
"""This modules does the checkout of code from SCM."""

import devpipeline_core.command

import devpipeline_scm.scm


def main(args=None):
    # pylint: disable=missing-docstring
    checkout = devpipeline_core.command.make_command([
        devpipeline_scm.scm.scm_task
    ], prog="dev-pipeline checkout", description="Checkout repositories")
    devpipeline_core.command.execute_command(checkout, args)


if __name__ == '__main__':
    main()
