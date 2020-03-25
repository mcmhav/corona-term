import sys
import os

from corona_term.app import App


def main() -> None:
    """Entry point for leakage-package."""
    App().fetch()


if __name__ == '__main__':
    try:
        main()
        # main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0) # pylint: disable=protected-access
