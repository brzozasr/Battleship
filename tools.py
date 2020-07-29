import os
import subprocess


def clear_console():
    """Function clears the console."""
    if os.name in ('nt', 'dos'):
        subprocess.call("cls")
    elif os.name in ('linux', 'osx', 'posix'):
        subprocess.call("clear")
    else:
        print("\n" * 120)


def is_mode_correct(mode_no):
    """The function checks the correctness of the game mode (number range from 1 to 2)."""
    try:
        num = int(mode_no)
        if num < 1 or num > 2:
            return False
    except ValueError:
        return False
    return True
