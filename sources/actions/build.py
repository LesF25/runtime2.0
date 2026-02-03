from sources.startup import builder
from .auxiliary import warn


def run(
    list: bool = False,
    cleanup: bool = False,
    *extension,
) -> None:
    """
    build runtime binary modules
    :key switch list: show availavle exensions
    :key switch cleanup: cleanup building directories
    :arg extension: optional extensions to build
    """
    builder.run()

    if builder.show_warning:
        warn("must be called from the command line")
