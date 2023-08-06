# Benchmarking Suite
# Copyright 2014-2017 Engineering Ingegneria Informatica S.p.A.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Developed in the ARTIST EU project (www.artist-project.eu) and in the
# CloudPerfect EU project (https://cloudperfect.eu/)

import argparse
import os
import time

from argcomplete import warn

from benchsuite.core.config import ControllerConfiguration
from benchsuite.core.controller import PROVIDER_STRING_ENV_VAR_NAME, \
    SERVICE_TYPE_STRING_ENV_VAR_NAME, BenchmarkingController
from benchsuite.core.sessionmanager import SessionStorageManager

DEFAULT_CMDS_MAPPING = {
    'new_session_cmd': None,
    'list_sessions_cmd': None,
    'destroy_session_cmd': None,
    'new_execution_cmd': None,
    'prepare_execution_cmd': None,
    'cleanup_execution_cmd': None,
    'run_execution_cmd': None,
    'collect_results_cmd': None,
    'multiexec_cmd': None,
    'list_executions_cmd': None,
    'list_providers_cmd': None,
    'list_benchmarks_cmd': None,
    'start_shell_cmd': None
}


# functions to generate autocomplete items


def completer_list_providers(prefix, parsed_args, **kwargs):
    conf = ControllerConfiguration(alternative_config_dir=os.environ.get('BENCHSUITE_CONFIG_FOLDER'))
    return [p.name for p in conf.list_available_providers()]


def completer_list_service_types(prefix, parsed_args, **kwargs):
    if parsed_args.provider:
        conf = ControllerConfiguration(alternative_config_dir=os.environ.get('BENCHSUITE_CONFIG_FOLDER'))
        prov = conf.get_provider_by_name(parsed_args.provider)
        return prov.service_types
    else:
        return []


def completer_most_recent_session(prefix, parsed_args, **kwargs):
    conf = ControllerConfiguration(alternative_config_dir=os.environ.get('BENCHSUITE_CONFIG_FOLDER'))
    session_storage = SessionStorageManager(conf.get_default_data_dir())
    session_storage.load()
    sessions = list(session_storage.list())
    sessions.sort(key=lambda x: x.created, reverse=True)
    return [sessions[0].id]


def completer_most_recent_exec(prefix, parsed_args, **kwargs):
    bc = BenchmarkingController()
    execs = bc.list_executions()
    execs.sort(key=lambda x: x.created, reverse=True)
    return [execs[0].id]


def completer_list_tools(prefix, parsed_args, **kwargs):
    conf = ControllerConfiguration(alternative_config_dir=os.environ.get('BENCHSUITE_CONFIG_FOLDER'))
    return [t.id for t in conf.list_available_tools()]


def completer_list_workloads(prefix, parsed_args, **kwargs):
    if parsed_args.tool:
        conf = ControllerConfiguration(alternative_config_dir=os.environ.get('BENCHSUITE_CONFIG_FOLDER'))
        tool_cfg = conf.get_benchmark_by_name(parsed_args.tool)
        return [w['id'] for w in tool_cfg.workloads]


def get_options_parser(cmds_mapping=DEFAULT_CMDS_MAPPING):

    # create the top-level parser
    parser = argparse.ArgumentParser(prog='benchsuite')
    parser.add_argument('--verbose', '-v', action='count', help='print more information (3 levels)')
    parser.add_argument('--quiet', '-q', action='store_true', help='suppress normal output')
    parser.add_argument('--config', '-c', type=str, help='foo help')
    subparsers = parser.add_subparsers(help='sub-command help')

    #
    # SHELL
    #
    sub_parser = subparsers.add_parser('shell',
                                       help="Starts an interactive shell")
    sub_parser.set_defaults(func=cmds_mapping['start_shell_cmd'])


    #
    # NEW SESSION
    #

    sub_parser = subparsers.add_parser('new-session',
                                       help='Creates a new benchmarking session',
                                       epilog='Example: benchsuite new-session -p myamazon -s centos_tiny')

    x = sub_parser.add_argument('--provider', '-p', type=str,
                            help='The name for the service provider configuration or the filepath of the provider '
                                 'configuration file. Alternatively, the provider configuration can be specified in '
                                 'the environment variable {0} (the content of the variable must be the actual '
                                 'configuration not the filepath)'.format(PROVIDER_STRING_ENV_VAR_NAME))
    x.completer = completer_list_providers

    x = sub_parser.add_argument('--service-type', '-s',
                            help='The name of one of the service types defined in the provider configuration. '
                                 'Alternatively, it can be specified in the {0} environment '
                                 'varaible'.format(SERVICE_TYPE_STRING_ENV_VAR_NAME))
    x.completer = completer_list_service_types

    sub_parser.add_argument('--property', '-P', type=str, action='append',
                            help='Add a user defined property to the session. The property must be expressed in the '
                                 'format <name>=<value>')

    sub_parser.add_argument('--user', '-u', type=str,
                            help='sets the "user" property. It is a shortcut for "--property user=<name>')

    sub_parser.add_argument('--tag', '-t', type=str, action='append',
                            help='sets one or more session tags. Internally, tags are stored as properties')


    sub_parser.set_defaults(func=cmds_mapping['new_session_cmd'])



    #
    # NEW EXECUTION
    #

    sub_parser = subparsers.add_parser('new-exec',
                                     help='Creates a new execution',
                                     epilog='Example: benchsuite new-exec 73cff747-d31a-488c-98f5-a70b9a77a11f '
                                            'filebench varmail')

    x = sub_parser.add_argument('session', type=str, help='a valid session id')
    x.completer = completer_most_recent_session

    x = sub_parser.add_argument('tool', type=str, help='a valid benchmarking tool')
    x.completer = completer_list_tools

    x = sub_parser.add_argument('workload', type=str, help='a valid benchmarking tool workload')
    x.completer = completer_list_workloads

    sub_parser.set_defaults(func=cmds_mapping['new_execution_cmd'])



    #
    # PREPARE EXEC
    #

    sub_parser = subparsers.add_parser('prepare-exec',
                                       help='Executes the install scripts for an execution',
                                       epilog='Example: benchsuite prepare-exec 4a5a86d4-88b6-11e7-9f96-742b62857160')

    x = sub_parser.add_argument('id', type=str, help='a valid id of the execution')
    x.completer = completer_most_recent_exec
    sub_parser.set_defaults(func=cmds_mapping['prepare_execution_cmd'])



    #
    # CLEANUP EXEC
    #

    sub_parser = subparsers.add_parser('cleanup-exec',
                                       help='Executed the cleanup script for an execution',
                                       epilog='Example: benchsuite cleanup-exec 4a5a86d4-88b6-11e7-9f96-742b62857160')
    x = sub_parser.add_argument('id', type=str, help='a valid id of the execution')
    x.completer = completer_most_recent_exec
    sub_parser.set_defaults(func=cmds_mapping['cleanup_execution_cmd'])



    #
    # RUN EXEC
    #

    sub_parser = subparsers.add_parser('run-exec',  help='Executes the execute scripts for an execution',
                                       epilog='Example: benchsuite run-exec 4a5a86d4-88b6-11e7-9f96-742b62857160')

    sub_parser.add_argument('--storage-config', '-r', type=str,
                            help='Specify a custom location for the storage configuration file')

    x = sub_parser.add_argument('id', type=str, help='a valid id of the execution')
    x.completer = completer_most_recent_exec

    sub_parser.add_argument('--async', action='store_true', help='start the execution of the scripts and return (do not'
                                                                 ' wait for the execution to finish)')
    sub_parser.set_defaults(func=cmds_mapping['run_execution_cmd'])


    parser_a = subparsers.add_parser('list-sessions', help='a help')
    parser_a.set_defaults(func=cmds_mapping['list_sessions_cmd'])

    parser_a = subparsers.add_parser('list-providers', help='a help')
    parser_a.set_defaults(func=cmds_mapping['list_providers_cmd'])

    parser_a = subparsers.add_parser('list-benchmarks', help='a help')
    parser_a.set_defaults(func=cmds_mapping['list_benchmarks_cmd'])

    parser_a = subparsers.add_parser('destroy-session', help='a help')
    parser_a.add_argument('id', type=str, help='bar help')
    parser_a.set_defaults(func=cmds_mapping['destroy_session_cmd'])

    parser_a = subparsers.add_parser('list-execs', help='lists the executions')
    parser_a.set_defaults(func=cmds_mapping['list_executions_cmd'])

    parser_a = subparsers.add_parser('collect-exec', help='collects the outputs of an execution')
    parser_a.add_argument('id', type=str, help='the execution id')
    parser_a.set_defaults(func=cmds_mapping['collect_results_cmd'])




    #
    # MULTIEXEC
    #

    sub_parser = subparsers.add_parser('multiexec',
                                       help='Execute multiple tests in a single benchmarking session',
                                       epilog='Example: benchsuite multiexec -p myamazon -s centos_tiny cfd:workload1 '
                                              'ycsb:workloada ycsb:workloadb')

    x = sub_parser.add_argument('--provider', '-p', type=str,
                            help='The name for the service provider configuration or the filepath of the provider '
                                 'configuration file')
    x.completer = completer_list_providers

    x = sub_parser.add_argument('--service-type', '-s', type=str,
                            help='The name of one of the service types defined in the provider configuration. If not '
                                 'specified, all service types will be used')
    x.completer = completer_list_service_types

    sub_parser.add_argument('--storage-config', '-r', type=str,
                            help='Specify a custom location for the storage configuration file')

    sub_parser.add_argument('--property', '-P', type=str, action='append',
                            help='Add a user defined property to the session. The property must be expressed in the '
                                 'format <name>=<value>')

    sub_parser.add_argument('--user', '-u', type=str,
                            help='sets the "user" property. It is a shortcut for "--property user=<name>')

    sub_parser.add_argument('--tag', '-t', type=str, action='append',
                            help='sets one or more session tags. Internally, tags are stored as properties')

    sub_parser.add_argument('--failonerror', '-e', action='store_true', default=False,
                            help='If set, exits immediately if one of the tests fail. It is false by default')

    sub_parser.add_argument('--keep-env', '-k', action='store_true', default=False,
                            help='If set, doesn\'t destroy the session after the end of the tests')

    sub_parser.add_argument('--max-retry', '-m', type=int,
                            help='If a test fails, retry for a maximum of max-retry times (default is 1)')

    sub_parser.add_argument('tests', nargs='+',
                            help='one or more tests in the format <tool>[:<workload>]. If workload is omitted, all '
                                 '  workloads defined for that tool will be executed')

    sub_parser.set_defaults(func=cmds_mapping['multiexec_cmd'])

    return parser

