import os
import subprocess
import board
import time


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


def print_both_boards(player1, player2, game_status):
    if game_status == 1:
        header_p1 = "\033[1;36mPLAYER 1\033[0m"
        header_p2 = "\033[1;34mPLAYER 2\033[0m"
    elif game_status == 2:
        header_p1 = "\033[1;36mPLAYER 1\033[0m"
        header_p2 = "\033[1;34mAI\033[0m"
    else:
        header_p1 = ""
        header_p2 = ""
    letter_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    margin_left = " " * 5
    margin_right = " " * 5
    margin_log = " " * 2
    line = margin_left + "  " + "+---" * board.Board.size
    top_no = f"{margin_left}  "
    for i in range(1, board.Board.size + 1):
        top_no += f"  \033[1;35m{i}\033[0m "
    txt = ""
    txt += f"{margin_left}  {header_p1:_^52}{margin_right}       {header_p2:_^52}\n"
    txt += f"{top_no}{margin_right}{top_no}{margin_log} \033[31mLast 10 moves:\033[0m\n"
    count_letter = 0
    for row1, row2 in zip(player1.board, player2.board):
        line_p1 = ""
        line_p2 = ""
        counter = 0
        txt += line + "+" + margin_right + line + "+\n"
        for cell1, cell2 in zip(row1, row2):
            if counter == 0:
                letter = f"{margin_left}\033[1;33m{letter_list[count_letter]}\033[0m" + " "
                count_letter += 1
            else:
                letter = ""

            if cell1.content == "0":
                cell1_content = f" \033[1;34m{cell1.content}\033[0m "
            elif cell1.content == "M":
                cell1_content = f" \033[1;32m{cell1.content}\033[0m "
            elif cell1.content == "H":
                cell1_content = f" \033[1;36m{cell1.content}\033[0m "
            elif cell1.content == "S":
                cell1_content = f" \033[1;31m{cell1.content}\033[0m "
            else:
                cell1_content = cell1.content

            if cell2.content == "0":
                cell2_content = f" \033[1;34m{cell2.content}\033[0m "
            elif cell2.content == "M":
                cell2_content = f" \033[1;32m{cell2.content}\033[0m "
            elif cell2.content == "H":
                cell2_content = f" \033[1;36m{cell2.content}\033[0m "
            elif cell2.content == "S":
                cell2_content = f" \033[1;31m{cell2.content}\033[0m "
            else:
                cell2_content = cell2.content

            line_p1 += f"{letter}|{cell1_content}"
            line_p2 += f"{letter}|{cell2_content}"
            count_log = count_letter - 1
            log_print = ""
            player = ""
            if len(board.Board.logs) > 0:
                if len(board.Board.logs) > count_log:
                    log = board.Board.logs[count_log]
                    if game_status == 1:
                        if log[1] == "P1":
                            player = "\033[34mP2:\033[0m"
                        else:
                            player = "\033[36mP1:\033[0m"
                    if game_status == 2:
                        if log[1] == "P2":
                            player = "\033[36mP1:\033[0m"
                        else:
                            player = "\033[34mAI:\033[0m"
                    if len(log[2]) >= 26:
                        mess = f"{log[2][:25]}..."
                    else:
                        mess = log[2]
                    log_print = f"\033[31m{log[0]:>3}\033[0m {player:<3} \033[32m{mess:<15}\033[0m"
            if counter == board.Board.size - 1:
                txt += f"{line_p1}|{margin_right}{line_p2}|{margin_log}{log_print}\n"
            counter += 1
    txt += f"{line}+{margin_right}{line}+\n"
    legend = f"{margin_left}  \033[1;34m0: an undiscovered tile\033[0m, \033[1;32mM: a missed shot\033[0m, " \
             f"\033[1;36mH: a hit ship part\033[0m, \033[1;31mS: a sunk ship part\033[0m."
    txt += legend
    print(txt)


def winner(file):
    """Print winner ASCI art from the text file."""
    current_dir = os.path.dirname(os.path.realpath(__file__))
    data_line = os.path.join(current_dir, file)

    if os.path.exists(data_line):
        with open(data_line, "r") as ascii_line:
            margin_left = " " * 3
            for line in ascii_line:
                line = line.strip(os.linesep)
                print(f'{margin_left}\033[01;31;40m{line:^65}\033[0m')
                time.sleep(0.4)
    else:
        print('\033[31m', f"The file \"{data_line}\" doesn't exist!", '\033[0m')


if __name__ == '__main__':
    board.Board.size = 10
    p1 = board.Board("P1")
    p1.init_board()
    p2 = board.Board("P2")
    p2.init_board()
    print_both_boards(p1, p2, 1)
