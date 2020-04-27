from datetime import datetime

from itertools import cycle

from os import name, system

from sys import stdin, stdout

from threading import current_thread

from time import sleep

from typing import Optional

from modules.formatter.formatter import Formatter as F

from modules.utils.constants import (DEFAULT_MARGIN_H as def_h,
                                     DEFAULT_MARGIN_V as def_v, ERASE_LINE)


def _l(string: str = '', left: int = def_h) -> str:
    """
    Formats a string with a margin of `left` chars to the left.

    ---
    Arguments
    ---

        string (str, '')
    Some string to format.

        left (int, def_h)
    A number of chars for the left margin.

    ---
    Returns
    ---

        str
    The string with the margin.
    """

    # Returns the formatted string.
    return _lt(string, left, 0)


def _ltb(string: str = '',
         left: int = def_h,
         top: int = def_v,
         bottom: int = def_v) -> str:
    """
    Formats a string with a margin of `left` characters to the left, `top` lines
    above and `bottom` lines below.

    ---
    Arguments
    ---

        string (str, '')
    Some string to format.

        left (int, def_h)
    A number of chars for the left margin.

        top (int, def_v)
    A number of lines for the top margin.

        bottom (int, def_v)
    A number of lines for the bottom margin.

    ---
    Returns
    ---

        str
    The string with the margins.
    """

    # Sets the margins.
    left = abs(int(left)) + len(str(string))
    top = '\n' * abs(int(top))
    bottom = '\n' * abs(int(bottom))

    # Returns the formatted string.
    return '{top}{:>{left}}{bottom}'.format(str(string),
                                            left=left,
                                            top=top,
                                            bottom=bottom)


def _lt(string: str = '', left: int = def_h, top: int = def_v) -> str:
    """
    Formats a string with a margin of `left` characters to the left and `top`
    lines above.

    ---
    Arguments
    ---

        string (str, '')
    Some string to format.

        left (int, def_h)
    A number of chars for the left margin.

        top (int, def_v)
    A number of lines for the top margin.

    ---
    Returns
    ---

        str
    The string with the margins.
    """

    # Returns the formatted string.
    return _ltb(string, left, top, 0)


def chevron(marker: str = '>',
            marker_formatter: F = None,
            margin: int = def_h) -> str:
    """
    Makes an user input marker.

    ---
    Arguments
    ---

        marker (str, '>')
    Some marker to use.

        marker_formatter (Formatter, None)
    A Formatter to format the marker.

        margin (int, def_h)
    A number of chars for the left margin.

    ---
    Returns
    ---

        str
    The formatted user input marker.
    """

    # If a marker formatter was not provided,...
    if marker_formatter is None:

        # ... instantiates a new one.
        marker_formatter = F()

    # Returns the formatted user input marker.
    return '\n' + _l(marker_formatter.write(marker), margin) + ' '


def clear() -> None:
    """
    Clean the terminal screen.
    """

    try:

        # Runs the command corresponding to the current operating system.
        system('cls' if name == 'nt' else 'clear')

    # Ctrl+C pressed.
    except (EOFError, KeyboardInterrupt):
        pass


def ellipsis(string: str = '',
             formatter: F = None,
             max_points: int = 3,
             freq: float = 2.0) -> None:
    """
    Shows a ellipsis feedback animation while a process is running.

    ---
    Arguments
    ---

        string (str, '')
    Some string to print before the ellipsis.

        formatter (Formatter, None)
    A Formatter for the final printed string.

        max_points (int, 3)
    Maximum number of points for the ellipsis.

        freq (float, 2.0)
    Frequency of the animation cycle.
    """

    # Gets the current thread.
    thread = current_thread()

    # The threads start alive.
    thread.alive = True

    # If a Formatter was not provided,...
    if formatter is None:

        # ... instantiates a new one.
        formatter = F()

    # Lists the animation pieces.
    chars = ['.' * i for i in range(1, max_points + 1)]

    # The animation cycles through the elements of the pieces list.
    for char in cycle(chars):

        # If the thread has stopped,...
        if not thread.alive:

            # ... then stops the animation.
            break

        # Prints the string followed by the current piece.
        stdout.write('\r' + formatter.erase(string + char).render() +
                     ERASE_LINE)
        stdout.flush()

        # Pauses for a period.
        sleep(1 / freq)


def error(string: str) -> F:
    """
    Shows a formatted error message.

    ---
    Arguments
    ---

        string (str)
    Some string for the error message.

    ---
    Returns
    ---

        Formatter
    The formatted string.
    """

    # Returns the formatted string.
    return F().bold().red(string)


def flush_input() -> None:
    """
    Flushes the input buffer.

    Taken from:
    https://rosettacode.org/wiki/Keyboard_input/Flush_the_keyboard_buffer#Python
    """

    try:

        # Tries to flush with the module for Windows.
        import msvcrt

        while msvcrt.kbhit():
            msvcrt.getch()

    # If it is unable to import,...
    except ImportError:

        # ... tries the module for Linux.
        import termios

        termios.tcflush(stdin, termios.TCIOFLUSH)


def info(string: str) -> F:
    """
    Shows a formatted information message.

    ---
    Arguments
    ---

        string (str)
    Some string for the information message.

    ---
    Returns
    ---

        Formatter
    The formatted string.
    """

    # Returns the formatted string.
    return F().blue(string)


def label(string: str,
          label_string: str = None,
          label_formatter: F = None) -> F:
    """
    Inserts a label in front of a string.

    ---
    Arguments
    ---

        string (str)
    Some string to labelize.

        label_string (str, None)
    A label to insert.

        label_formatter (Formatter, None)
    A Formatter for the label.

    ---
    Returns
    ---

        Formatter
    A Formatter instance with the labelized string.
    """

    # If a label was not provided,...
    if label_string is None:

        # ... uses the string produced by the now() method.
        label_string = now()

    # If a labe formatter was not provided,...
    if label_formatter is None:

        # ... instantiates a new one.
        label_formatter = F().black()

    # Returns the labelized string.
    return F(label_formatter.write('[').write(label_string).write('] ')).write(
        string)


def now() -> str:
    """
    Gets the current date and time.

    ---
    Returns
    ---

        str
    The formatted date and time.
    """

    # Returnas the formatted date and time.
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S')


def press_enter_to(action: str,
                   formatter: F = None,
                   enter_formatter: F = None,
                   wait: bool = True,
                   left: int = def_h) -> Optional[str]:
    """
    Shows the message "Press [ENTER] to `action`...".

    ---
    Arguments
    ---

        action (str)
    Some action to use in the message.

        formatter (Formatter, None)
    A message Formatter.

        enter_formatter (Formatter, None)
    The "[ENTER]" string Formatter.

        wait (bool, True)
    Sets whether the input() method should be used.

        left (int, def_h)
    A number of chars for the left margin.

    ---
    Returns
    ---

        Optional[str]
    The formatted message, if the `wait` flag is False.
    """

    # If a message formatter was not provided,...
    if formatter is None:

        # ... instantiates a new one.
        formatter = F()

    # If a "[ENTER]" string formatter was not provided,...
    if enter_formatter is None:

        # ... instantiates a new one.
        enter_formatter = F()

    # Saves the output string in a variable.
    output = _lt(
        formatter.write('Press [').write(
            enter_formatter.write('ENTER')).write('] to ').write(F().write(
                str(action).lower())).write('...'), left)

    # If it should not wait,...
    if not wait:

        # ... just returns the output string.
        return output

    try:

        # Flushes some previous inputs.
        flush_input()

        # Waits for the user to press the ENTER key.
        input(output)

    # Ctrl+C pressed.
    except (EOFError, KeyboardInterrupt):
        pass


def success(string: str) -> F:
    """
    Shows a formatted success message.

    ---
    Arguments
    ---

        string (str)
    Some string for the success message.

    ---
    Returns
    ---

        Formatter
    The formatted string.
    """

    # Returns the formatted string.
    return F().bold().green(string)


def title(margin: int = def_h, clear_screen: bool = True) -> str:
    """
    Returns the PyRadio title string, with a margin around.

    ---
    Arguments
    ---

        margin (int, def_h)
    A number of chars for the margin, based on the left margin.

        clear_screen (bool, True)
    Sets whether the title should be printed on a clean screen.

    ---
    Returns
    ---

        str
    The formatted title.
    """

    # It does not accept negative or odd margins.
    margin_h = abs(int(margin)) - int(margin) % 2

    # Vertical margins are half of the left margin.
    margin_v = margin_h / 2

    # Typography generated at:
    # http://patorjk.com/software/taag/#p=display&f=ANSI%20Shadow&t=PyRadio
    #
    # There was an elongation of a line in the capital letters, only.
    lines = [
        '██████╗          ██████╗',
        '██╔══██╗██╗   ██╗██╔══██╗ █████╗ ██████╗ ██╗ ██████╗',
        '██████╔╝╚██╗ ██╔╝██████╔╝██╔══██╗██╔══██╗██║██╔═══██╗',
        '██╔═══╝  ╚████╔╝ ██╔══██╗███████║██║  ██║██║██║   ██║',
        '██║       ╚██╔╝  ██║  ██║██╔══██║██║  ██║██║██║   ██║',
        '██║        ██║   ██║  ██║██║  ██║██████╔╝██║╚██████╔╝',
        '╚═╝        ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝ ╚═════╝'
    ]

    # If the [clear_screen] flag is True,...
    if clear_screen:

        # ... clean the terminal screen before printing.
        clear()

    # Returns the formatted joining of the lines list with a breakline.
    return _ltb('{:{margin}}'.format('\n', margin=margin_h + 1).join(lines),
                margin_h, margin_v, margin_v)


def warning(string: str) -> F:
    """
    Shows a formatted warning message.

    ---
    Arguments
    ---

        string (str)
    Some string for the warning message.

    ---
    Returns
    ---

        Formatter
    The formatted string.
    """

    # Returns the formatted string.
    return F().yellow(string)
