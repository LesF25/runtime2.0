from pathlib import Path
from sys import exit
from typing import Any

from argparse import ArgumentParser
from setuptools import Extension

from sources import settings
from sources.utils.output import show, warn
from .builder import Builder, ReportBuilderFailureError

EXTENSIONS = {
    'vdomxml': Extension(
        'memory.vdomxml._loads',
        sources=['memory/vdomxml/loads.c'],
        include_dirs=['memory/vdomxml/include'],
    )
}

show_warning = False


class ArgumentsError(Exception):
    pass


class ExceptionalArgumentParser(ArgumentParser):
    def error(self, message):
        raise ArgumentsError(message)


def _register_build_command(subparsers: Any) -> ArgumentParser:
    subparser = subparsers.add_parser(
        'build',
        help='...',
    )
    subparser.add_argument(
        '-l',
        '--list',
        action='store_true',
        dest='list',
        default=False,
        help='show available extensions',
    )
    subparser.add_argument(
        '--cleanup',
        action='store_true',
        dest='cleanup',
        default=False,
        help='cleanup building directories',
    )
    subparser.add_argument(
        'extensions',
        nargs='*',
        metavar='extension',
        help='optional extensions to build',
    )

    return subparser


def _register_deploy_command(subparsers: Any) -> ArgumentParser:
    subparser = subparsers.add_parser(
        'deploy',
        help='...',
    )

    return subparser


def _register_install_command(subparsers: Any) -> ArgumentParser:
    subparser = subparsers.add_parser(
        'install',
        help='...',
    )
    subparser.add_argument('application.xml')

    return subparser


def _parse_args() -> dict[str, Any]:
    parser = ExceptionalArgumentParser(add_help=False)
    parser.add_argument(
        '-c',
        '--configure',
        dest='filename',
        default=None
    )

    subparsers = parser.add_subparsers(dest='action')

    _register_build_command(subparsers)
    _register_deploy_command(subparsers)
    _register_install_command(subparsers)

    return vars(parser.parse_args())


def _ensure_temp_directory() -> None:
    temp_path = Path(settings.TEMPORARY_LOCATION)
    if temp_path.is_dir():
        return

    show('Prepare temporary directory')
    try:
        temp_path.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        warn(f'Unable to prepare temporary directory: {error}')
        exit(1)


def _run_builder(args: dict[str, Any]) -> None:
    builder = Builder(EXTENSIONS)

    if args.get('list'):
        builder.list()
    elif args.get('cleanup'):
        builder.cleanup()
    else:
        ext = args.get('extensions')
        builder.build(
            *(ext if ext else [])
        )


def run() -> None:
    global show_warning

    try:
        args = _parse_args()
    except ArgumentsError:
        show_warning = True
        return

    _ensure_temp_directory()

    try:
        _run_builder(args)
    except ReportBuilderFailureError:
        pass


if __name__ == '__main__':
    run()
