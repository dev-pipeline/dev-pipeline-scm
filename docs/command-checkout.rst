checkout
========

Synopsis
--------
::

    dev-pipeline checkout [-h] [--list-scms] [--dependencies DEPENDENCIES]
                             [--executor EXECUTOR]
                             [targets [targets ...]]


Description
-----------
Determine the dependencies of targets and make sure the repositories are up to
date.  The tool with either perform a fresh checkout or an update
(:code:`git fetch`, :code:`hg pull`, etc.) depending on the status of the
local copy.

If no targets are specified, all targets will be checked out and/or updated.


Options
-------
  -h, --help            show this help message and exit
  --list-scms           List the available scm tools
  --dependencies DEPENDENCIES
                        Control how build dependencies are handled. (default:
                        deep)
  --executor EXECUTOR   The method to execute commands. (default: quiet)


Config Options
--------------
* :code:`scm` - (**Required**) The source control tool to use.  Available
  options are a union of what's built in and what's available via plugins.
* :code:`src_path` - The path where a package's source tree lives.  If
  unspecified, packages will be checked out in a folder matching their name
  under :code:`dp.src_root`.
