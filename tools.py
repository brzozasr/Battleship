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


def get_coordinates(coord):
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    if coord[0] in letters and coord[1:] in numbers:
        poz_x = letters.index(coord[0])
        poz_y = numbers.index(coord[1:])
        return [poz_x, poz_y]


def is_ship_available(fleet):
    for (k, v) in fleet.items():
        if v > 0:
            return True, k[0], k[1]
    return False, None, None


def is_position_correct(pos):
    pos_list = ["H", "V"]
    if pos in pos_list:
        return True
    else:
        return False
