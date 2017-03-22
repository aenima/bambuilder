#! /usr/bin/python
"""
@file: Some attempt to parse Bamboo Build Descriptions

"""

import os.path
import argparse

import yaml

from tasks import get_task_runner


DEFAULT_SOURCEFILE = "Bamboo.yml"

class ScriptError(Exception):
    """
    Generic Exception 
    """
    pass


def _parse_cmdline_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("path", default=".", help="Path to Bamboo.yml")
    argparser.add_argument("-v", "--verbose", action="count", help="Verbosity")
    return argparser.parse_args()


def _get_sourcefile_path(path_arg):
    if path_arg == ".":
        path_arg = DEFAULT_SOURCEFILE
    if os.path.isdir(path_arg):
        path_arg = os.path.join(path_arg, DEFAULT_SOURCEFILE)
    return path_arg


def _parse_sourcefile(sourcefile_path):
    try:
        with open(sourcefile_path) as sourcefile_f:
            data = yaml.load(sourcefile_f)
    except IOError as err:
        if err.errno == 2:
            raise ScriptError("File not found: {}".format(sourcefile_path))
        else:
            raise ScriptError(str(err))
    except Exception:
        raise
    return data


def _run_plan(stage_list):
    for stage_data in stage_list:
        print "Stage '{}'...".format(stage_data['name'])
        _run_stage(stage_data['jobs'])
        print "Stage completed.\n"
    return


def _run_stage(job_list):
    has_failed = False
    for job_data in job_list:
        try:
            print "\tJob '{}'...".format(job_data['name'])
            _run_job(job_data['tasks'])
        except ScriptError as err:
            print "\tJob failed: {}".format(err)
            has_failed = True
    if has_failed:
        raise ScriptError("Stage failed.")
    return


def _run_job(task_list):
    for task_data in task_list:
        task_runner = get_task_runner(task_data)
        task_runner()
    return


def _extract_stages(build_data):
    try:
        raw_stage_data = build_data['stages']
    except KeyError:
        raise ScriptError("No stage data found")
    return raw_stage_data


def main():
    """
    Main Method
    """
    try:
        args = _parse_cmdline_args()
        sourcefile_path = _get_sourcefile_path(args.path)
        plan_data = _parse_sourcefile(sourcefile_path)
        stage_data = _extract_stages(plan_data)
        print "Found build plan '{}' with {} stages.".format(plan_data['name'], len(stage_data))
        _run_plan(stage_data)
        print "Build plan completed."
    except ScriptError as err:
        print err.args[0]
        return 1
    return


if __name__ == "__main__":
    main()

