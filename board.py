import os
import sys
import random
import numpy as np

from conway import error_msg

ALIVE = 1
DEAD = 0

NORMAL = "\33[0m"
WHITE = "\33[30;107m"
BLACK = "\33[97;40m"
CYAN = "\33[30;106m"
YELLOW = "\33[30;103m"
BLUE = "\33[97;104m"
GREEN = "\33[30;102m"

RAND_THRESH = 0.5

class Board:
    def __init__(self, pattern, theme, debug):
        self.debug = debug
        self.theme = theme

        screen = os.get_terminal_size()
        if screen.lines > (screen.columns // 2):
            self.size = screen.columns // 2
        else:
            self.size = screen.lines

        self.data = np.zeros((self.size, self.size), dtype=np.int8)
        self.nbr_buf = self.data

        match pattern:
            case 0:
                self.__checkerboard()
            case 1:
                self.__diagonals()
            case 2:
                self.__random()
            case _:
                error_msg("unknown pattern")

    def __checkerboard(self):
        for row in range(self.size):
            for col in range(self.size):
                self.data[col][row] = (col + row) % 2

    def __diagonals(self):
        for i in range(self.size):
            j = self.size - i - 1
            self.data[i][i] = ALIVE
            self.data[j][i] = ALIVE

    def __random(self):
        for row in range(self.size):
            for col in range(self.size):
                if (random.random() >= RAND_THRESH):
                    self.data[col][row] = ALIVE

    def __increment_neighbors(self, row, col):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                elif col+j < 0 or row+i < 0:
                    continue
                try:
                    self.nbr_buf[col+j][row+i] += 1
                except IndexError:
                    continue

    def evolve(self):
        # reset the neighbor buffer
        self.nbr_buf = np.zeros((self.size, self.size), dtype=np.int8)

        # neighbor count pass
        for row in range(self.size):
            for col in range(self.size):
                if self.data[col][row] == ALIVE:
                    self.__increment_neighbors(row, col)

        # board rules pass
        for row in range(self.size):
            for col in range(self.size):
                # case 2 is purposefully ignored
                match self.nbr_buf[col][row]:
                    case 0 | 1:
                        self.data[col][row] = DEAD
                    case 3:
                        self.data[col][row] = ALIVE
                    case 4 | 5 | 6 | 7 | 8:
                        self.data[col][row] = DEAD

    def refresh(self):
        text_buf = ""
        for row in range(self.size):
            for col in range(self.size):
                if self.debug:
                    char = str(self.nbr_buf[col][row])
                else:
                    char = " "

                if self.data[col][row] == ALIVE:
                    match self.theme:
                        case 0:
                            text_buf += WHITE+char+char
                        case 1:
                            text_buf += YELLOW+char+char
                        case 2:
                            text_buf += CYAN+char+char
                        case 3:
                            text_buf += GREEN+char+char
                        case _:
                            error_msg("unknown theme")
                else:
                    match self.theme:
                        case 0 | 2:
                            text_buf += BLACK+char+char
                        case 1:
                            text_buf += BLUE+char+char
                        case 3:
                            text_buf += WHITE+char+char
                        case _:
                            error_msg("unknown theme")
            text_buf += NORMAL + "\n"
        sys.stdout.write(text_buf)
        sys.stdout.flush()
        self.clear()

    def clear(self, all=False):
        if all:
            # clears the entire screen
            sys.stdout.write(NORMAL+"\033[2J\033[H")
        else:
            # clears only what's behind the cursor
            sys.stdout.write(NORMAL+"\033[J\033[H")
        sys.stdout.flush()