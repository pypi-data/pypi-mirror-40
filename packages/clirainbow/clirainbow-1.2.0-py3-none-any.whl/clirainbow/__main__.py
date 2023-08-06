from clirainbow.clirainbow import Colorizer
from clirainbow.colors import *


def main():
    c = Colorizer()
    c.print(
        'Welcome to <C><L><I><R><A><I><N><B><O><W>',
        BRIGHT_RED,
        BRIGHT_GREEN,
        BRIGHT_BLUE,
        BRIGHT_YELLOW,
        BRIGHT_CYAN,
        BRIGHT_MAGENTA,
        BRIGHT_RED,
        BRIGHT_GREEN,
        BRIGHT_BLUE,
        BRIGHT_YELLOW,
    )


if __name__ == '__main__':
    main()
