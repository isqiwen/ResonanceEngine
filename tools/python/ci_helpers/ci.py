import sys
from pathlib import Path
from argparse import ArgumentParser, RawTextHelpFormatter

python_project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(python_project_root))

from common.logger_config import Logger
from common.shell_utils import run_command
from common.file_utils import clean
from common.platform_utils import Platform

from ci_helpers.ci_constants import log_configuration, PROJECT_NAME
from ci_helpers.ci_win import WinBuilder
from ci_helpers.conan_setup import setup_conan_home


def gen_parser():
    command_example = '''[example] {command}  # build with default setttings'''.format(
        command = __file__
    )
    parser = ArgumentParser(
        prog = __file__,
        formatter_class = RawTextHelpFormatter,
        description = f'Build {PROJECT_NAME}',
        epilog = command_example
    )

    workflow = parser.add_argument_group('workflow')

    workflow.add_argument(
        "--clean",
        dest = 'clean',
        help = f'Clean {PROJECT_NAME}',
        default = False,
        action = 'store_true'
    )

    workflow.add_argument(
        "--build",
        dest = 'build',
        help = f'Build {PROJECT_NAME}',
        default = False,
        action = 'store_true'
    )

    workflow.add_argument(
        "--pack",
        dest = 'pack',
        help = f'Pack {PROJECT_NAME}',
        default = False,
        action = 'store_true'
    )

    workflow.add_argument(
        "--test",
        dest = 'test',
        help = f'Test {PROJECT_NAME}',
        default = False,
        action = 'store_true'
    )

    flags = parser.add_argument_group('flags')

    flags.add_argument(
        "--debug",
        dest = 'debug',
        help = 'Build Debug Version',
        default = False,
        action = 'store_true'
    )

    flags.add_argument(
        "--verbose",
        dest = 'verbose',
        help = "Build with verbose log",
        default = False,
        action = 'store_true'
    )

    return parser


def ci_entry(config):
    builder = WinBuilder()
    builder.setup_and_run(config)

def ci_main(argv):
    setup_conan_home()

    log_configuration()

    parser = gen_parser()
    config = parser.parse_args(argv)
    ci_entry(config)


if '__main__' == __name__:
    ci_main(sys.argv[1:])
