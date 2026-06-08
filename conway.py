import sys
import os
import datetime as dt

from board import *

FRAMERATE = 20
DEFAULT_THEME = 0

def usage():
    print(
        "---------------------\n"
        "Conway's Game of Life\n"
        "[usage] python conway.py <pattern> <theme>(optional) -d/--debug (debug, optional)\n\n"
        "patterns:\n"
        "0 - checkerboard\n"
        "1 - diagonals\n"
        "2 - random\n\n"
        "theme:\n"
        "0 - black and white\n"
        "1 - blue and yellow\n"
        "2 - black and cyan\n"
        "3 - white and green\n\n"
        "debug: displays neighbor counts\n"
    )
def error_msg(msg):
    print(msg)
    usage()
    quit()

def systime():
    now = dt.datetime.now()
    return int(now.timestamp() * 1000)

def parse_args():
    theme = DEFAULT_THEME
    debug = False

    if len(sys.argv) > 4:
        error_msg("too many arguments")

    elif len(sys.argv) == 1:
        usage()
        quit()

    elif len(sys.argv) == 2:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            usage()
            quit()
        try:
            pattern = int(sys.argv[1])
        except ValueError:
            error_msg("pattern must be a number")

    elif len(sys.argv) == 3:
        try:
            pattern = int(sys.argv[1])
        except ValueError:
            error_msg("pattern must be a number")

        if sys.argv[2] == "-d" or sys.argv[2] == "--debug":
            debug = True
        else:
            try:
                theme = int(sys.argv[2])
            except ValueError:
                error_msg("theme must be a number")

    else:
        try:
            pattern = int(sys.argv[1])
        except ValueError:
            error_msg("pattern must be a number")

        try:
            theme = int(sys.argv[2])
        except ValueError:
            error_msg("theme must be a number")

        if sys.argv[3] == "-d" or sys.argv[3] == "--debug":
            debug = True
        else:
            error_msg("last argument unknown")

    return (pattern, theme, debug)


if __name__ == "__main__":
    pattern, theme, debug = parse_args()
    size = os.get_terminal_size().columns // 2
    board = Board(size, pattern, theme, debug)

    try:
        next_tick = systime()
        while(True):
            now = systime()
            if (now >= next_tick):
                board.refresh()
                next_tick += 1000 / FRAMERATE

                board.evolve()

    except KeyboardInterrupt:
        board.clear(all=True)
        quit()
