""" Script to run a script in a given container """
import sys
import subprocess
import shutil

import bilby_pipe
from bilby_pipe.bilbyargparser import BilbyArgParser
from bilby_pipe.main import Input, DataDump, parse_args


def create_parser():
    """ Generate a parser for the exec_in_container script

    Additional options can be added to the returned parser beforing calling
    `parser.parse_args` to generate the arguments`

    Returns
    -------
    parser: BilbyArgParser
        A parser with all the default options already added

    """
    parser = BilbyArgParser(ignore_unknown_config_file_keys=True)
    parser.add('--ini', is_config_file=True, help='The ini-style config file')
    parser.add('-s', '--singularity-container', type=str, help='The singularity image')
    return parser


args, unknown_args = parse_args(sys.argv[1:], create_parser())
exec_args = ['singularity', 'exec', args.singularity_container]
print_args = ['echo', '"Running in singularity container"']
add_bilby_pipe_args = ['PYTHONPATH="${{PYTHONPATH}}:{}"'.format(
    '/' + '/'.join(bilby_pipe.__file__.split('/')[:-2]))]
job_args = ['python', shutil.which('bilby_pipe_generation')]
call_arg_list = exec_args + print_args + [';'] + add_bilby_pipe_args + job_args + unknown_args
print(' '.join(call_arg_list))
print(subprocess.getoutput(call_arg_list))
#return_code = subprocess.call(call_arg_list)
