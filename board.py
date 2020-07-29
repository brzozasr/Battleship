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
                cell = Cell(i, j, "0")  # TODO improve content
                board_row.append(cell)
            self.board.append(board_row)

    def find_cell(self, x, y):
        for line in self.board:
            for cell in line:
                if cell.poz_x == x and cell.poz_y == y:
                    return cell.content

    def add_ship(self, x, y, length, location):
        if Board.is_out_of_range(x, y, length, location):
            for line in self.board:
                for cell in line:  # TODO check out of range and neighbors
                    if location == "H":
                        if cell.poz_x == x and y <= cell.poz_y < y + length:
                            for i in range(length):
                                cell.object_ship = ship.Ship(x, y, length, location)
                    if location == "V":
                        if x <= cell.poz_x < x + length and cell.poz_y == y:
                            for i in range(length):
                                cell.object_ship = ship.Ship(x, y, length, location)
        else:
            print('\033[31m', f"Invalid input! The ship is out of the board!", '\033[0m')

    def is_intersect(self, x, y, length, location):
        pass

    def __str__(self):
        txt = ""
        for row in self.board:
            for cell in row:
                txt += f"x: {cell.poz_x}, y: {cell.poz_y} - {cell.content} {cell.object_ship}\n"
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
c = Board()
c.init_board()

c.add_ship(7, 5, 4, "V")
# print(c.is_out_of_range(4, 3, 4, "V"))
# print(c)
