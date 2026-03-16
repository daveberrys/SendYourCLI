import sys

import src.print as print
from src.flags import runFlags
from src.interactive import runInteractive

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            runFlags(sys.argv[1:])
        else:
            runInteractive()
    except (KeyboardInterrupt, EOFError):
        print.warning("Terminated by user.")
        sys.exit(130)
