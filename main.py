import board
import tools

game_sts = 0
player = "P1"
fleet_p1 = {("Battleship", 4): 1,
            ("Destroyer", 3): 2,
            ("Submarine", 2): 3,
            ("Patrol Boat", 1): 5}
fleet_p2 = {("Battleship", 4): 1,
            ("Destroyer", 3): 2,
            ("Submarine", 2): 3,
            ("Patrol Boat", 1): 5}


def set_game_sts(new_game_sts):
    global game_sts
    game_sts = new_game_sts


def set_player(new_player):
    global player
    player = new_player


def main():
    board.Board.size = 10
    p1 = board.Board()
    p1.init_board()
    p2 = board.Board()
    p2.init_board()
    is_running = True
    while is_running:
        if game_sts == 0:
            print("Available game modes: 1 - Multiplayer, 2 - Single player, or write \"exit\" to terminate.")
            mode = input("Select the game mode: ")
            mode = mode.upper()
            if mode == "EXIT":
                break
            elif tools.is_mode_correct(mode):
                set_game_sts(int(mode))
            else:
                print('\033[31m', "The game mod you have selected is invalid, please select 1 or 2!", '\033[0m')
                continue
        elif game_sts == 1:
            tools.clear_console()
            if player == "P1":
                print(p1.ship_input_board_print())
                p1.print_message()
                print(f"\033[36mPlayer {player[1]} placing ships phase.\033[0m")
            else:
                print(p2.ship_input_board_print())
                p2.print_message()
                print(f"\033[34mPlayer {player[1]} placing ships phase.\033[0m")
            coord = input("Write coordinates of the ship (e.g. A1, D5): ")
            coord = coord.upper()
            if coord == "EXIT":
                break
            else:
                if player == "P1":
                    if p1.is_coordinates_correct(coord):
                        p1.add_ship(0, 0, 4, "H")
        elif game_sts == 2:
            pass


main()
