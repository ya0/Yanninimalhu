# TODO: Implement network as a Board subclass

import abc, random, math, pygame as pg
from Game import Player, Strategy

"""
An abstract base class for the board, the topological environmental in
which the players interact
"""
class Board(abc.ABC):
    @abc.abstractmethod
    def assign_player_to_cell(self, player, cell):
        pass

    @abc.abstractmethod
    def get_player_from_cell(self, cell):
        pass

    @abc.abstractmethod
    def occupied(self, cell):
        """ determine whether a cell is occupied by a player """
        pass

    @abc.abstractmethod
    def get_distance_between(self, cell1, cell2):
        pass

    @abc.abstractmethod
    def get_players_in_play_neighborhood(self, cell):
        """ gets the players which a player in a cell would be able to play
        with
        """
        pass

    @abc.abstractmethod
    def get_empty_cells_in_migration_neighboorhood(self, cell, M):
        """ gets the empty cells which a player in a cell would be able to
        migrate to
        """
        pass

    @abc.abstractmethod
    def random_cell_sequence(self):
        """ gets a list of all cells in random order """
        pass

    @abc.abstractmethod
    def draw(self):
        """ draws the board on screen """
        pass


class RectangularGrid(Board):
    def __init__(self, height, width):
        # grid setup
        self.height = height
        self.width = width
        self.grid = [[None for j in range(width)] for i in range(height)]

        # visualization setup
        background_color = (0, 0, 0)
        cell_height = 16
        cell_width = 16
        screen_dimensions = (cell_width * self.width,
                            cell_height * self.height)
        pg.init()
        self.screen = pg.display.set_mode(screen_dimensions)
        pg.display.set_caption("Strategy Evolution Simulation")
        self.screen.fill(background_color)

    def assign_player_to_cell(self, player, cell):
        self.grid[cell[0]][cell[1]] = player


    def get_player_from_cell(self, cell):
        return self.grid[cell[0]][cell[1]]


    def occupied(self, cell):
        return self.grid[cell[0]][cell[1]] != None


    def get_distance_between(self, cell1, cell2):
        y1, x1 = cell1
        y2, x2 = cell2
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


    def get_players_in_play_neighborhood(self, cell):
        """ gets the players in the Moore neighborhood of a cell
        """
        i, j = cell
        players = []

        # Moore neighborhood accounting for periodic boundary conditions
        cell_above = ((i - 1) % self.height, j)
        cell_below = ((i + 1) % self.height, j)
        cell_left = (i, (j - 1) % self.width)
        cell_right = (i, (j + 1) % self.width)
        moore_neighborhood = [cell_above, cell_below, cell_left, cell_right]

        for cell in moore_neighborhood:
            if self.occupied(cell):
                players.append(self.get_player_from_cell(cell))

        return players


    def get_empty_cells_in_migration_neighboorhood(self, cell, M):
        """ gets the empty cells in the Neumann neighborhood of the cell
        """
        i, j = cell
        neighboring_empty_cells = []

        for a in range(i - M, i + M + 1):
            for b in range(j - M, j + M + 1):
                # cell coordinates accounting for periodic boundary conditions
                m = a % self.height
                n = b % self.width

                # ignore the cell itself
                if m == i and n == j:
                    continue

                if self.grid[m][n] == None:
                    neighboring_empty_cells.append((m, n))

        return neighboring_empty_cells


    def random_cell_sequence(self):

        random_cell_sequence = []
        # add all cell coordinates to the list
        for i in range(self.height):
            for j in range(self.width):
                random_cell_sequence.append((i, j))
        random.shuffle(random_cell_sequence)

        return random_cell_sequence


    def draw(self):
        blue = (0, 0, 255)
        red = (255, 0, 0)
        white = (255, 255, 255)

        for i in range(self.height):
            for j in range(self.width):

                # define top-left pixel of cell
                tup = (j * 16, i * 16, 16, 16)

                # determine cell colouring
                player = self.grid[i][j]
                if player:
                    if player.strategy == Strategy.cooperate:
                        pg.draw.rect(self.screen, blue, tup, 0)
                    elif player.strategy == Strategy.defect:
                        pg.draw.rect(self.screen, red, tup, 0)
                    else:
                        pg.draw.rect(self.screen, white, tup, 0)
                else:
                    pg.draw.rect(self.screen, white, tup, 0)

        pg.display.update()
