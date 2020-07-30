import board
import tools


# 0 - the beginning of the game,
# 1 - Multiplayer,
# 2 - Single player.
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
            if player == "P1" and tools.is_ship_available(fleet_p1)[0]:
                print(p1.ship_input_board_print())
                p1.print_message()
                p1.message = None
                ship = tools.is_ship_available(fleet_p1)
                print(f"\033[36mPlayer {player[1]} placing ships phase.\033[0m")
            else:
                set_player("P2")
                print(p2.ship_input_board_print())
                p2.print_message()
                p2.message = None
                ship = tools.is_ship_available(fleet_p2)
                print(f"\033[34mPlayer {player[1]} placing ships phase.\033[0m")
            coord = input(f"Write coordinates of the {ship[1]} (size: {ship[2]}) (e.g. A1, D5): ")
            coord = coord.upper()
            if coord == "EXIT":
                break
            else:
                if player == "P1":
                    if p1.is_coordinates_correct(coord):
                        coord_xy = tools.get_coordinates(coord)
                        coord_xy.append(ship[2])
                        if ship[2] > 1:
                            position = input(f"Set position of the {ship[1]}, \"H\" - horizontal, \"V\" - vertical: ")
                            position = position.upper()
                        else:
                            position = "H"
                        if tools.is_position_correct(position):
                            coord_xy.append(position)
                            is_added = p1.add_ship(*coord_xy)
                            if is_added:
                                fleet_p1[(ship[1], ship[2])] -= 1
                else:
                    if p2.is_coordinates_correct(coord):
                        coord_xy = tools.get_coordinates(coord)
                        coord_xy.append(ship[2])
                        if ship[2] > 1:
                            position = input(f"Set position of the {ship[1]}, \"H\" - horizontal, \"V\" - vertical: ")
                            position = position.upper()
                        else:
                            position = "H"
                        if tools.is_position_correct(position):
                            coord_xy.append(position)
                            is_added = p2.add_ship(*coord_xy)
                            if is_added:
                                fleet_p2[(ship[1], ship[2])] -= 1

        elif game_sts == 2:
            pass


main()
