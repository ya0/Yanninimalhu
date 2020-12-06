# TODO: Implement network as a Board subclass

import abc, random, math, pygame as pg
from Game import Player, Strategy

class Board(abc.ABC):
    @abc.abstractmethod
    def set_cell(self, cell, data):
        pass

    @abc.abstractmethod
    def get_cell(self, cell):
        pass

    @abc.abstractmethod
    def occupied(self, cell):
        pass

    @abc.abstractmethod
    def get_distance_between(self, cell1, cell2):
        pass

    @abc.abstractmethod
    def get_neumann_neighboring_players(self, cell):
        pass

    @abc.abstractmethod
    def get_moore_neighboring_players(self, cell, radius):
        pass

    @abc.abstractmethod
    def get_moore_neighboring_empty_cells(self, cell, radius):
        pass

    @abc.abstractmethod
    def random_cell_sequence(self):
        pass

    @abc.abstractmethod
    def draw(self):
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

    # TODO: rename to SetPlayerAtCell or something
    def set_cell(self, cell, data):
        self.grid[cell[0]][cell[1]] = data


    def get_cell(self, cell):
        return self.grid[cell[0]][cell[1]]


    def occupied(self, cell):
        return self.grid[cell[0]][cell[1]] != None


    def get_distance_between(self, cell1, cell2):
        y1, x1 = cell1
        y2, x2 = cell2
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


    def get_neumann_neighboring_players(self, cell):
        i, j = cell
        players = []

        if i > 0:
            if self.occupied((i-1, j)):
                players.append(self.get_cell((i-1, j)))
        if i < self.height - 1:
            if self.occupied((i+1, j)):
                players.append(self.get_cell((i+1, j)))
        if j > 0:
            if self.occupied((i, j-1)):
                players.append(self.get_cell((i, j-1)))
        if j < self.width - 1:
            if self.occupied((i, j+1)):
                players.append(self.get_cell((i, j+1)))

        return players


    def get_moore_neighboring_players(self, cell, r):
        i, j = cell
        players = []

        # find empty cells with Chebyshev distance from the cell <= r
        for m in range(i - r, i + r + 1):
            for n in range(j - r, j + r + 1):
                # ignore out-of-bounds cells
                if (m < 0 or m >= self.height or n < 0 or n >= self.width):
                    continue

                # ignore the cell itself
                if m == i and n == j:
                    continue

                if abs(m - i) <= r and abs(n - j) <= r:
                    player = self.grid[m][n]
                    if player != None:
                        players.append(player)

        return players


    def get_moore_neighboring_empty_cells(self, cell, r):
        i, j = cell
        neighboring_empty_cells = []

        for m in range(i - r, i + r + 1):
            for n in range(j - r, j + r + 1):
                # ignore out-of-bounds cells
                if m < 0 or m >= self.height or n < 0 or n >= self.width:
                    continue

                # ignore the cell itself
                if m == i and n == j:
                    continue

                if abs(m - i) <= r and abs(n - j) <= r:
                    if self.grid[m][n] == None:
                        neighboring_empty_cells.append((m, n))

        return neighboring_empty_cells


    # TODO: Potential speed-up by simply implementing a get_random_cell() function
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
