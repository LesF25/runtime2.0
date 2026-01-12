import sys

LOGGING = None


def debug(
    message,
    tag: str = '',
    console = None,
):
    prefix = f'[{tag}]  ' if tag else ''
    print(f'{prefix}{message}', file=sys.stdout)


class DebugFile:
    def write(self, message) -> None:
        debug(message)
