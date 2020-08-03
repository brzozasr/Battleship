import ship
import random
import tools


class Cell:
    def __init__(self, poz_x, poz_y, content, object_ship=None):
        """Content indicates:
        - 0: an undiscovered tile,
        - M: a missed shot,
        - H: a hit ship part,
        - S: a sunk ship part."""
        self.poz_x = poz_x
        self.poz_y = poz_y
        self.content = content
        self.object_ship = object_ship


class Board:
    size = 10
    logs = []
    index = 1

    def __init__(self, cls_name):
        self.cls_name = cls_name
        self.size = Board.size
        self.board = []
        self._message = None

    @classmethod  # TODO usunąć
    def test(cls):
        print(cls.logs)

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    def print_message(self):
        if self._message is not None:
            print(f"\033[31m{self._message}\033[0m")
            if len(Board.logs) >= 10:
                Board.logs.pop(0)
                Board.logs.append((f"{Board.index}.", self.cls_name.upper(), self._message))
                Board.index += 1
            else:
                Board.logs.append((f"{Board.index}.", self.cls_name.upper(), self._message))
                Board.index += 1

    def init_board(self):
        for i in range(self.size):
            board_row = []
            for j in range(self.size):
                cell = Cell(i, j, "0")
                board_row.append(cell)
            self.board.append(board_row)

    def find_cell(self, x, y):
        for line in self.board:
            for cell in line:
                if cell.poz_x == x and cell.poz_y == y:
                    return cell.content

    def add_ship(self, x, y, length, location):
        if Board.is_out_of_range(x, y, length, location):
            if not self.is_intersect(x, y, length, location):
                for line in self.board:
                    for cell in line:
                        if location == "H":
                            if cell.poz_x == x and y <= cell.poz_y < y + length:
                                for i in range(length):
                                    cell.object_ship = ship.Ship(x, y, length, location)
                        if location == "V":
                            if x <= cell.poz_x < x + length and cell.poz_y == y:
                                for i in range(length):
                                    cell.object_ship = ship.Ship(x, y, length, location)
                return True
            else:
                self._message = "Ships are too close!"
                return False
        else:
            self._message = "Invalid input! The ship is out of the board!"
            return False

    def is_intersect(self, x, y, length, location):
        intersect_set = set()
        if location == "H":
            counter_h = 1
            for _ in range(length):
                for i in range(3):
                    poz = (x, (y - 1) + i)
                    if (poz[0] >= 0 and poz[1] >= 0) and (poz[0] < Board.size and poz[1] < Board.size):
                        intersect_set.add(poz)
                for j in range(3):
                    poz = (x - 1, (y - 1) + j)
                    if (poz[0] >= 0 and poz[1] >= 0) and (poz[0] < Board.size and poz[1] < Board.size):
                        intersect_set.add(poz)
                for k in range(3):
                    poz = (x + 1, (y - 1) + k)
                    if (poz[0] >= 0 and poz[1] >= 0) and (poz[0] < Board.size and poz[1] < Board.size):
                        intersect_set.add(poz)
                y += counter_h
        if location == "V":
            counter_v = 1
            for _ in range(length):
                for i in range(3):
                    poz = ((x - 1) + i, y)
                    if (poz[0] >= 0 and poz[1] >= 0) and (poz[0] < Board.size and poz[1] < Board.size):
                        intersect_set.add(poz)
                for j in range(3):
                    poz = ((x - 1) + j, y - 1)
                    if (poz[0] >= 0 and poz[1] >= 0) and (poz[0] < Board.size and poz[1] < Board.size):
                        intersect_set.add(poz)
                for k in range(3):
                    poz = ((x - 1) + k, y + 1)
                    if (poz[0] >= 0 and poz[1] >= 0) and (poz[0] < Board.size and poz[1] < Board.size):
                        intersect_set.add(poz)
                x += counter_v
        for line in self.board:
            for cell in line:
                if (cell.poz_x, cell.poz_y) in intersect_set and cell.object_ship is not None:
                    return True
        intersect_set.clear()
        return False

    def ship_input_board_print(self):
        letter_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        margin = " " * 2
        line = margin + "+---" * Board.size
        top_no = f"{margin}"
        for i in range(1, Board.size + 1):
            top_no += f"  \033[1;35m{i}\033[0m "
        txt = ""
        txt += top_no + "\n"
        count_letter = 0
        for row in self.board:
            counter = 0
            txt += line + "+\n"
            for cell in row:
                if counter == 0:
                    letter = f"\033[1;33m{letter_list[count_letter]}\033[0m" + " "
                    count_letter += 1
                else:
                    letter = ""
                if cell.content == "0" and cell.object_ship is None:
                    cell_content = f"\033[1;36m.\033[0m"
                else:
                    cell_content = f"\033[1;31mX\033[0m"

                txt += f"{letter}| {cell_content} "
                if counter == Board.size - 1:
                    txt += "|\n"
                counter += 1
        txt += f"{line}+"
        return txt

    def __str__(self):
        letter_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        margin = " " * 2
        line = margin + "+---" * Board.size
        top_no = f"{margin}"
        for i in range(1, Board.size + 1):
            top_no += f"  \033[1;35m{i}\033[0m "
        txt = ""
        txt += top_no + "\n"
        count_letter = 0
        for row in self.board:
            counter = 0
            txt += line + "+\n"
            for cell in row:
                if counter == 0:
                    letter = f"\033[1;33m{letter_list[count_letter]}\033[0m" + " "
                    count_letter += 1
                else:
                    letter = ""
                if cell.content == "0":
                    cell_content = f"\033[1;34m{cell.content}\033[0m"
                elif cell.content == "M":
                    cell_content = f"\033[1;32m{cell.content}\033[0m"
                elif cell.content == "H":
                    cell_content = f"\033[1;36m{cell.content}\033[0m"
                elif cell.content == "S":
                    cell_content = f"\033[1;31m{cell.content}\033[0m"
                else:
                    cell_content = cell.content

                txt += f"{letter}| {cell_content} "
                if counter == Board.size - 1:
                    txt += "|\n"
                counter += 1
        txt += f"{line}+\n"
        legend = f"\033[1;34m0: an undiscovered tile\033[0m, \033[1;32mM: a missed shot\033[0m, \n" \
                 f"\033[1;36mH: a hit ship part\033[0m, \033[1;31mS: a sunk ship part\033[0m."
        txt += legend
        return txt

    def is_coordinates_correct(self, coord):
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        coordinates = []
        for i in range(Board.size):
            for j in range(Board.size):
                coordinates.append(letters[i] + numbers[j])
        if coord in coordinates:
            return True
        else:
            self._message = f"Invalid coordinates ({coord})!"
            return False

    def is_location_correct(self, pos):
        pos_list = ["H", "V"]
        if pos in pos_list:
            return True
        else:
            self._message = "You entered the wrong location, you can choose \"H\" or \"V\"!!!"
            return False

    def shot(self, x, y):
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        coord = f"({letters[x]}{numbers[y]})"
        if self.board[x][y].content == "M" or self.board[x][y].content == "H" or \
                self.board[x][y].content == "S":
            self._message = f"The shot {coord} was already here!"
            return False
        elif self.board[x][y].content == "0" and self.board[x][y].object_ship is None:
            self.board[x][y].content = "M"
            self._message = f"You've missed {coord}!"
            return True
        elif self.board[x][y].content == "0" and self.board[x][y].object_ship is not None:
            if self.board[x][y].object_ship.length == 1:
                self.board[x][y].content = "S"
                self._message = f"You've sunk a ship {coord}!"
                return True
            else:
                if self.board[x][y].object_ship.location == "H":
                    self.board[x][y].content = "H"
                    sx = self.board[x][y].object_ship.start_poz_x
                    sy = self.board[x][y].object_ship.start_poz_y
                    tmp_ship = [self.board[sx][i].content for i in range(sy, sy + self.board[x][y].object_ship.length)]
                    if "0" not in tmp_ship:
                        for i in range(sy, sy + self.board[x][y].object_ship.length):
                            self.board[sx][i].content = "S"
                        self._message = f"You've sunk a ship {coord}!"
                    else:
                        self._message = f"You've hit a ship {coord}!"
                    return True
                elif self.board[x][y].object_ship.location == "V":
                    self.board[x][y].content = "H"
                    sx = self.board[x][y].object_ship.start_poz_x
                    sy = self.board[x][y].object_ship.start_poz_y
                    tmp_ship = [self.board[i][sy].content for i in range(sx, sx + self.board[x][y].object_ship.length)]
                    if "0" not in tmp_ship:
                        for i in range(sx, sx + self.board[x][y].object_ship.length):
                            self.board[i][sy].content = "S"
                        self._message = f"You've sunk a ship {coord}!"
                    else:
                        self._message = f"You've hit a ship {coord}!"
                    return True

    def has_lost(self):
        for line in self.board:
            for cell in line:
                if cell.content == "0" and cell.object_ship is not None:
                    return False
        return True

    def ai_place_ships(self, fleet):
        is_placing = True
        while is_placing:
            x = random.randint(0, Board.size - 1)
            y = random.randint(0, Board.size - 1)
            loc = random.choice(["H", "V"])
            ship_data = tools.is_ship_available(fleet)
            if tools.is_ship_available(fleet)[0]:
                if self.add_ship(x, y, ship_data[2], loc):
                    fleet[(ship_data[1], ship_data[2])] -= 1
            else:
                is_placing = False

    def ai_shot(self):
        not_shoot_fields = set()
        first_shoot = set()
        for line in self.board:
            for cell in line:
                if cell.content == "S":
                    for i in range(3):
                        pos = (cell.poz_x, (cell.poz_y - 1) + i)
                        if (pos[0] >= 0 and pos[1] >= 0) and (pos[0] < Board.size and pos[1] < Board.size):
                            not_shoot_fields.add(pos)
                    for j in range(3):
                        pos = (cell.poz_x - 1, (cell.poz_y - 1) + j)
                        if (pos[0] >= 0 and pos[1] >= 0) and (pos[0] < Board.size and pos[1] < Board.size):
                            not_shoot_fields.add(pos)
                    for k in range(3):
                        pos = (cell.poz_x + 1, (cell.poz_y - 1) + k)
                        if (pos[0] >= 0 and pos[1] >= 0) and (pos[0] < Board.size and pos[1] < Board.size):
                            not_shoot_fields.add(pos)
                elif cell.content == "H" and self.len_h() == 1:
                    pos_top = (cell.poz_x - 1, cell.poz_y)
                    if (pos_top[0] >= 0 and pos_top[1] >= 0) and (pos_top[0] < Board.size and pos_top[1] < Board.size):
                        if self.board[pos_top[0]][pos_top[1]].content == "0":
                            first_shoot.add(pos_top)
                    pos_left = (cell.poz_x, cell.poz_y - 1)
                    if (pos_left[0] >= 0 and pos_left[1] >= 0) and (
                            pos_left[0] < Board.size and pos_left[1] < Board.size):
                        if self.board[pos_left[0]][pos_left[1]].content == "0":
                            first_shoot.add(pos_left)
                    pos_right = (cell.poz_x, cell.poz_y + 1)
                    if (pos_right[0] >= 0 and pos_right[1] >= 0) and (
                            pos_right[0] < Board.size and pos_right[1] < Board.size):
                        if self.board[pos_right[0]][pos_right[1]].content == "0":
                            first_shoot.add(pos_right)
                    pos_bottom = (cell.poz_x + 1, cell.poz_y)
                    if (pos_bottom[0] >= 0 and pos_bottom[1] >= 0) and (
                            pos_bottom[0] < Board.size and pos_bottom[1] < Board.size):
                        if self.board[pos_bottom[0]][pos_bottom[1]].content == "0":
                            first_shoot.add(pos_bottom)
                elif cell.content == "H" and self.len_h() > 1:
                    line_h_list = self.pos_h()
                    if line_h_list[0][0] == line_h_list[1][0]:
                        pos_left = (cell.poz_x, cell.poz_y - 1)
                        if (pos_left[0] >= 0 and pos_left[1] >= 0) and (
                                pos_left[0] < Board.size and pos_left[1] < Board.size):
                            if self.board[pos_left[0]][pos_left[1]].content == "0":
                                first_shoot.add(pos_left)
                        pos_right = (cell.poz_x, cell.poz_y + 1)
                        if (pos_right[0] >= 0 and pos_right[1] >= 0) and (
                                pos_right[0] < Board.size and pos_right[1] < Board.size):
                            if self.board[pos_right[0]][pos_right[1]].content == "0":
                                first_shoot.add(pos_right)
                    elif line_h_list[0][1] == line_h_list[1][1]:
                        pos_top = (cell.poz_x - 1, cell.poz_y)
                        if (pos_top[0] >= 0 and pos_top[1] >= 0) and (
                                pos_top[0] < Board.size and pos_top[1] < Board.size):
                            if self.board[pos_top[0]][pos_top[1]].content == "0":
                                first_shoot.add(pos_top)
                        pos_bottom = (cell.poz_x + 1, cell.poz_y)
                        if (pos_bottom[0] >= 0 and pos_bottom[1] >= 0) and (
                                pos_bottom[0] < Board.size and pos_bottom[1] < Board.size):
                            if self.board[pos_bottom[0]][pos_bottom[1]].content == "0":
                                first_shoot.add(pos_bottom)

        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

        if len(first_shoot) > 0:
            poz = first_shoot.pop()
            if self.shot(*poz):
                if self._message.startswith("You've missed"):
                    self._message = f"AI has missed ({letters[poz[0]]}{numbers[poz[1]]})!"
                elif self._message.startswith("You've sunk a ship"):
                    self._message = f"AI has sunk a ship ({letters[poz[0]]}{numbers[poz[1]]})!"
                elif self._message.startswith("You've hit a ship"):
                    self._message = f"AI has hit a ship ({letters[poz[0]]}{numbers[poz[1]]})!"
        else:
            is_shooting = True
            while is_shooting:
                x = random.randint(0, Board.size - 1)
                y = random.randint(0, Board.size - 1)
                if self.board[x][y].content == "0" and (x, y) not in not_shoot_fields:
                    if self.shot(x, y):
                        if self._message.startswith("You've missed"):
                            self._message = f"AI has missed ({letters[x]}{numbers[y]})!"
                        elif self._message.startswith("You've sunk a ship"):
                            self._message = f"AI has sunk a ship ({letters[x]}{numbers[y]})!"
                        elif self._message.startswith("You've hit a ship"):
                            self._message = f"AI has hit a ship ({letters[x]}{numbers[y]})!"
                        is_shooting = False

    def len_h(self):
        counter = 0
        for line in self.board:
            for cell in line:
                if cell.content == "H":
                    counter += 1
        return counter

    def pos_h(self):
        pos_list = []
        for line in self.board:
            for cell in line:
                if cell.content == "H":
                    pos_list.append((cell.poz_x, cell.poz_y))
        return pos_list

    @classmethod
    def is_out_of_range(cls, x, y, length, location):
        if location == "H":
            if (0 <= x < cls.size) and (y >= 0 and y + length - 1 < cls.size):
                return True
            else:
                return False
        if location == "V":
            if (0 <= y < cls.size) and (x >= 0 and x + length - 1 < cls.size):
                return True
            else:
                return False
        else:
            return False


if __name__ == '__main__':
    Board.size = 10
    p1 = Board("P1")
    p1.init_board()
    p2 = Board("P2")
    p2.init_board()
    # print(p1.ship_input_board_print())
    fleet_p1 = {("Battleship", 4): 1,
                ("Destroyer", 3): 2,
                ("Submarine", 2): 3,
                ("Patrol Boat", 1): 5}
    p1.ai_place_ships(fleet_p1)
    print(p1.ship_input_board_print())
