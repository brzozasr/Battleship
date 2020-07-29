import ship


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

    def __init__(self):
        self.size = Board.size
        self.board = []

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
            else:
                print('\033[31m', "Ships are too close!", '\033[0m')
        else:
            print('\033[31m', "Invalid input! The ship is out of the board!", '\033[0m')

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
            return False

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


Board.size = 10
p1 = Board()
p1.init_board()
p2 = Board()
p2.init_board()
print(p1)
