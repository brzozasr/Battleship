class Ship:
    def __init__(self, start_poz_x, start_poz_y, length, location):
        self.start_poz_x = start_poz_x
        self.start_poz_y = start_poz_y
        self.length = length
        self.location = location
        self.no_ship = {4: 1,
                        3: 2,
                        2: 3,
                        1: 5}
