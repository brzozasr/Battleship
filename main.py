import board
import tools
import time

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


def set_fleet_p1():
    global fleet_p1
    fleet_p1 = {("Battleship", 4): 1,
                ("Destroyer", 3): 2,
                ("Submarine", 2): 3,
                ("Patrol Boat", 1): 5}


def set_fleet_p2():
    global fleet_p2
    fleet_p2 = {("Battleship", 4): 1,
                ("Destroyer", 3): 2,
                ("Submarine", 2): 3,
                ("Patrol Boat", 1): 5}


def reset_game():
    set_game_sts(0)
    set_player("P1")
    set_fleet_p1()
    set_fleet_p2()


def main():
    board.Board.size = 10
    board.Board.index = 1
    board.Board.logs.clear()
    p1 = board.Board("P1")
    p1.init_board()
    p2 = board.Board("P2")
    p2.init_board()
    is_running = True
    is_wrong_enter_mode = False
    while is_running:
        if game_sts == 0:
            tools.clear_console()
            if is_wrong_enter_mode:
                print('\033[31m', "The game mod you have selected is invalid, please select 1 or 2!", '\033[0m')
                is_wrong_enter_mode = False
            print("Available game modes: 1 - Multiplayer, 2 - Single player, or write \"exit\" to terminate.")
            mode = input("Select the game mode: ")
            mode = mode.upper()
            if mode == "EXIT":
                break
            elif tools.is_mode_correct(mode):
                set_game_sts(int(mode))
            else:
                is_wrong_enter_mode = True
                continue
        elif game_sts == 1:
            tools.clear_console()
            if tools.is_ship_available(fleet_p1)[0] or tools.is_ship_available(fleet_p2)[0]:
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
                                position = input(
                                    f"Set location of the {ship[1]}, \"H\" - horizontal, \"V\" - vertical: ")
                                position = position.upper()
                            else:
                                position = "H"
                            if p1.is_location_correct(position):
                                coord_xy.append(position)
                                is_added = p1.add_ship(*coord_xy)
                                if is_added:
                                    fleet_p1[(ship[1], ship[2])] -= 1
                    else:
                        if p2.is_coordinates_correct(coord):
                            coord_xy = tools.get_coordinates(coord)
                            coord_xy.append(ship[2])
                            if ship[2] > 1:
                                position = input(
                                    f"Set position of the {ship[1]}, \"H\" - horizontal, \"V\" - vertical: ")
                                position = position.upper()
                            else:
                                position = "H"
                            if p2.is_location_correct(position):
                                coord_xy.append(position)
                                is_added = p2.add_ship(*coord_xy)
                                if is_added:
                                    fleet_p2[(ship[1], ship[2])] -= 1
                                    if not tools.is_ship_available(fleet_p2)[0]:
                                        set_player("P1")
                                        board.Board.logs.clear()
                                        board.Board.index = 1
            else:
                tools.clear_console()
                if player == "P1":
                    tools.print_both_boards(p1, p2, game_sts)
                    p2.print_message()
                    p2.message = None
                    print(f"\033[36mPlayer {player[1]}\'s turn.\033[0m")
                else:
                    tools.print_both_boards(p1, p2, game_sts)
                    p1.print_message()
                    p1.message = None
                    print(f"\033[34mPlayer {player[1]}\'s turn.\033[0m")
                shot = input(f"Player {player[1]} shot: ")
                shot = shot.upper()
                if shot == "EXIT":
                    break
                else:
                    if player == "P1":
                        if p2.is_coordinates_correct(shot):
                            coord_xy = tools.get_coordinates(shot)
                            is_shot = p2.shot(*coord_xy)
                            tools.clear_console()
                            tools.print_both_boards(p1, p2, game_sts)
                            p2.print_message()
                            p2.message = None
                            if is_shot:
                                set_player("P2")
                            time.sleep(2)
                            if p2.has_lost():
                                p2.message = "Player 1 has won!!!"
                                p2.print_message()
                                p2.message = None
                                del p1
                                del p2
                                reset_game()
                                board.Board.size = 10
                                board.Board.index = 1
                                board.Board.logs.clear()
                                p1 = board.Board("P1")
                                p1.init_board()
                                p2 = board.Board("P2")
                                p2.init_board()
                                time.sleep(4)
                                tools.winner("p1.txt")
                    elif player == "P2":
                        if p1.is_coordinates_correct(shot):
                            coord_xy = tools.get_coordinates(shot)
                            is_shot = p1.shot(*coord_xy)
                            tools.clear_console()
                            tools.print_both_boards(p1, p2, game_sts)
                            p1.print_message()
                            p1.message = None
                            if is_shot:
                                set_player("P1")
                            time.sleep(2)
                            if p1.has_lost():
                                p1.message = "Player 2 has won!!!"
                                p1.print_message()
                                p1.message = None
                                del p1
                                del p2
                                reset_game()
                                board.Board.size = 10
                                board.Board.index = 1
                                board.Board.logs.clear()
                                p1 = board.Board("P1")
                                p1.init_board()
                                p2 = board.Board("P2")
                                p2.init_board()
                                time.sleep(4)
                                tools.winner("p2.txt")

        elif game_sts == 2:
            tools.clear_console()
            if tools.is_ship_available(fleet_p1)[0] or tools.is_ship_available(fleet_p2)[0]:
                if player == "P1" and tools.is_ship_available(fleet_p1)[0]:
                    print(p1.ship_input_board_print())
                    p1.print_message()
                    p1.message = None
                    print(f"\033[36mPlayer {player[1]} placing ships phase.\033[0m")
                    ship = tools.is_ship_available(fleet_p1)
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
                                    position = input(
                                        f"Set position of the {ship[1]}, \"H\" - horizontal, \"V\" - vertical: ")
                                    position = position.upper()
                                else:
                                    position = "H"
                                if p1.is_location_correct(position):
                                    coord_xy.append(position)
                                    is_added = p1.add_ship(*coord_xy)
                                    if is_added:
                                        fleet_p1[(ship[1], ship[2])] -= 1
                                        if not tools.is_ship_available(fleet_p1)[0]:
                                            set_player("AI")
                else:
                    p2.ai_place_ships(fleet_p2)
                    p2.message = None
                    set_player("P1")
                    board.Board.logs.clear()
                    board.Board.index = 1
            else:
                tools.clear_console()
                if player == "P1":
                    tools.print_both_boards(p1, p2, game_sts)
                    print(f"\033[36mPlayer {player[1]}\'s turn.\033[0m")
                    p2.print_message()
                    p2.message = None
                    shot = input(f"Player {player[1]} shot: ")
                    shot = shot.upper()
                    if shot == "EXIT":
                        break
                    else:
                        if player == "P1":
                            if p2.is_coordinates_correct(shot):
                                coord_xy = tools.get_coordinates(shot)
                                is_shot = p2.shot(*coord_xy)
                                tools.clear_console()
                                tools.print_both_boards(p1, p2, game_sts)
                                p2.print_message()
                                p2.message = None
                                if is_shot:
                                    set_player("AI")
                                time.sleep(2)
                                if p2.has_lost():
                                    p2.message = "Player 1 has won!!!"
                                    p2.print_message()
                                    p2.message = None
                                    del p1
                                    del p2
                                    board.Board.size = 10
                                    board.Board.index = 1
                                    board.Board.logs.clear()
                                    p1 = board.Board("P1")
                                    p1.init_board()
                                    p2 = board.Board("P2")
                                    p2.init_board()
                                    reset_game()
                                    time.sleep(4)
                                    tools.winner("p1.txt")
                        else:
                            tools.clear_console()
                            tools.print_both_boards(p1, p2, game_sts)
                            p2.print_message()
                            p2.message = None
                elif player == "AI":
                    p1.ai_shot()
                    tools.clear_console()
                    tools.print_both_boards(p1, p2, game_sts)
                    print(f"\033[34mPlayer AI\'s turn.\033[0m")
                    p1.print_message()
                    p1.message = None
                    set_player("P1")
                    time.sleep(3)
                    if p1.has_lost():
                        p1.message = "Player AI has won!!!"
                        p1.print_message()
                        p1.message = None
                        del p1
                        del p2
                        board.Board.size = 10
                        board.Board.index = 1
                        board.Board.logs.clear()
                        p1 = board.Board("P1")
                        p1.init_board()
                        p2 = board.Board("P2")
                        p2.init_board()
                        reset_game()
                        time.sleep(4)
                        tools.winner("ai.txt")


main()
