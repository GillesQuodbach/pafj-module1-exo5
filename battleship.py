from typing import List

# on défini la position des bateaux
aircraft_carrier = {(2, 2): True, (2, 3): True, (2, 4): True, (2, 5): True, (2, 6): True}
cruiser = {(4, 1): True, (5, 1): True, (6, 1): True, (7, 1): True}
destroyer = {(5, 3): True, (6, 3): True, (7, 3): True}
submarine = {(5, 8): True, (5, 9): True, (5, 10): True}
torpedo_boat = {(9, 5): True, (9, 6): True}
ships_list = [aircraft_carrier, cruiser, destroyer, submarine, torpedo_boat]


class Grid:
    GRID_SIZE: int = 10
    LETTERS: List[str] = [chr(letter_code) for letter_code in range(ord('A'), ord('A') + GRID_SIZE)]
    SEA: int = 0
    MISSED_SHOT: int = 1
    HIT_SHOT: int = 2
    SUNK_SHOT: int = 3
    SQUARE_STATE_REPR: List[str] = [' ', 'X', '#', '-']

    def __init__(self):
        self.played_shots = set()
        self.ships = []
        self.ship_by_coord = {}

    def add_ship(self, ship):
        self.ships.append(ship)
        for coord in ship.coords:
            self.ship_by_coord[coord] = ship

    def grid_square_state(self, coord):
        if coord in self.played_shots:
            square_ship = self.ship_by_coord.get(coord)
            if square_ship:
                square_state = self.SUNK_SHOT if square_ship.is_sunk() else self.HIT_SHOT
            else:
                square_state = self.MISSED_SHOT
        else:
            square_state = self.SEA

        return square_state

    def display_grid(self):
        """Affichage de la grille de jeu"""
        print('    ', end='')
        for x in range(self.GRID_SIZE):
            letter = self.LETTERS[x]
            print(f' {letter}  ', end='')
        print()
        print('  ', '+---' * self.GRID_SIZE + '+')
        for line_no in range(1, self.GRID_SIZE + 1):
            print(f'{line_no:>2} |', end='')
            for column_no in range(1, self.GRID_SIZE + 1):
                coord = (line_no, column_no)
                square_state = self.grid_square_state(coord)
                state_str = self.SQUARE_STATE_REPR[square_state]
                print(f' {state_str} |', end='')
            print()
            print('  ', '+---' * self.GRID_SIZE + '+')

    def analyse_shot(self, coord):
        # ajout du tir au tableau des tirs joués
        self.played_shots.add(coord)

        # vérification si un bateau se trouve sur la position de tir
        ship = self.ship_by_coord.get(coord)
        if ship:
            print("Bateau touché")
            ship.is_hit(coord)
            if ship.is_sunk():
                print("Bateau coulé")
                self.ships.remove(ship)
        else:
            print("Le tir est tombé dans l'eau")

    def is_remaining_ship(self):
        return bool(self.ships)


class Ship:

    def __init__(self, coords):
        self.coords = {coord: True for coord in coords}

    def is_hit(self, coord):
        if coord in self.coords:
            self.coords[coord] = False

    def is_sunk(self):
        return not any(self.coords.values())


class Game:
    def __init__(self):
        self.grid = Grid()

    def setup(self):
        ships_coords = [list(ship.keys()) for ship in ships_list]
        for coords in ships_coords:
            self.grid.add_ship(Ship(coords))

    def ask_coord(self):
        valid_coord = False
        while not valid_coord:
            player_input = input("Entre les coordonnées de votre tir (ex A1):")
            if 2 <= len(player_input) <= 3:
                letter, number = player_input[0], player_input[1:]
                letter = letter.upper()
                try:
                    line_no = int(number)
                    column_no = ord(letter) - ord('A') + 1
                    if 1 <= line_no <= self.grid.GRID_SIZE and letter in self.grid.LETTERS:
                        valid_coord = True
                        return line_no, column_no
                except ValueError:
                    pass
            print("Coordonnées invalides, veuillez réessayer.")

    def play(self):
        self.setup()
        while self.grid.is_remaining_ship():
            self.grid.display_grid()
            shot_coord = self.ask_coord()
            self.grid.analyse_shot(shot_coord)
            print()

        self.grid.display_grid()
        print("Bravo, tous les navires ont été coulés")


if __name__ == "__main__":
    game = Game()
    game.play()
