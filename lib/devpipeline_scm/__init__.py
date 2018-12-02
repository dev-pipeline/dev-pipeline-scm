#!/usr/bin/python3

"""
Main module for devpipeline_scm.  It provides SCMS, a dictionary with all
detected scm plugins.
"""

import os.path

import devpipeline_core.paths
import devpipeline_core.plugin

SCMS = devpipeline_core.plugin.query_plugins('devpipeline.scms')

_SRC_PATH_KEYS = ['scm.src_path', 'src_path']
_SCM_TOOL_KEYS = ['scm.tool', 'scm']


def _find_key(component, keys):
    for key in keys:
        if key in component:
            return key
    return None


def _no_scm_check(configuration, error_fn):
    for component_name in configuration.components():
        component = configuration.get(component_name)
        scm_key = _find_key(component, _SCM_TOOL_KEYS)
        if not scm_key:
            error_fn("No scm declared in {}".format(component_name))
        _final_deprecated_check(scm_key, _SCM_TOOL_KEYS[0],
                                component_name, error_fn)


def _final_deprecated_check(real_key, expected_key, component_name, error_fn):
    if real_key and (real_key != expected_key):
        error_fn("{}: {} is deprecated; migrate to {}".format(
            component_name, real_key, expected_key))


def _check_deprecated_helper(configuration, keys, error_fn):
    for component_name in configuration.components():
        component = configuration.get(component_name)
        key = _find_key(component, keys)
        _final_deprecated_check(key, keys[0], component_name, error_fn)


def _deprecated_scm_path_check(configuration, error_fn):
    _check_deprecated_helper(configuration, _SRC_PATH_KEYS, error_fn)


def _make_src_dir(configuration):
    for component_name in configuration.components():
        component = configuration.get(component_name)
        if ("import" in component) and ("scm.fixed_revision" in component):
            shared_scm = component.get("dp.import_name")
            src_root = devpipeline_core.paths.make_path(
                component, "scm.cache", shared_scm)
            src_path = devpipeline_core.paths.make_path(
                component, "scm.cache", "{}-{}".format(shared_scm, component.get("dp.import_version")))
            component.set("dp.src_dir_shared", src_root)
            component.set("dp.src_dir", src_path)
        else:
            key = _find_key(component, _SRC_PATH_KEYS) or _SRC_PATH_KEYS[0]
            src_path = component.get(key, fallback=component.name())
            component.set(
                'dp.src_dir',
                os.path.join(
                    component.get("dp.src_root"),
                    src_path))


class _SimpleScm(devpipeline_core.toolsupport.SimpleTool):

    """This class is a simple SCM tool."""

    def __init__(self, real, current_target):
        super().__init__(current_target, real)

    def checkout(self, *args):
        """This function checks out source code."""
        self._call_helper("Checking out", self.real.checkout,
                          *args)

    def update(self, *args):
        """This funcion updates a checkout of source code."""
        self._call_helper("Updating", self.real.update,
                          *args)


def make_simple_scm(real_scm, configuration):
    """
    Create an Scm instance that leverages executors.

    Arguments:
    real_scm - a class instance that provides an Scm interface
    configuration - the configuration for the Scm target
    """
    return _SimpleScm(real_scm, configuration)
