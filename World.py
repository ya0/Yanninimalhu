import random
from Game import Strategy
from Board import RectangularGrid

# delete later
import time

class World():
    def __init__(self, game, board, players, r = 0, q = 0, noise1 = False, noise2 = False, imitation = False, migration = False, moore_neighborhood_range = 0):
        """
        - game: the game played between two players during an interaction
        - board: the topology of the world
        - players: a list of players in the world
        - r: the probability of a player randomly resetting its strategy
        - q: the probability that a player resets its strategy to cooperate
        - noise1: a boolean indicating whether Noise 1 is present
        - noise2: a boolean indicating whether Noise 2 is present
        - imitation: a boolean indicating whether players perform imitation
        - migration: a boolean indicating whether
        - moore_neighborhood_range: the range of the Moore neighborhood around each cell
        """
        self.game = game
        self.board = board
        self.players = players
        self.r = r
        self.q = q
        self.noise1 = noise1
        self.noise2 = noise2
        self.imitation = imitation
        self.migration = migration
        self.moore_neighborhood_range = moore_neighborhood_range

        # randomly insert players in board cells
        random.shuffle(players)
        random_cell_sequence = board.random_cell_sequence()

        if len(players) > len(random_cell_sequence):
            print("Error! Number of players exceeds the number of cells on the board")
            exit()

        for i in range(len(players)):
            players[i].cell = random_cell_sequence[i]
            self.board.set_cell(random_cell_sequence[i], players[i])
            self.board.get_cell(random_cell_sequence[i])


    def round(self):
        """ carries out one round of updates, in which each player is updated
        once based on the parameters of the world
        """
        random.shuffle(self.players)
        for player in self.players:
            self.play_with_neighbors(player)

            # perform migration step
            if self.migration:
                self.migration_update(player)

            rand = random.random()
            if rand < self.r:
                # randomly reset player strategy and/or location
                if self.noise1:
                    self.noise1_update(player)

                if self.noise2:
                    self.noise2_update(player)

            else:
                # perform imitation step
                if self.imitation:
                    self.imitation_update(player)


    def move_player(self, player, new_cell):
        """ moves a player from its current cell on the board to the new cell
        on the board (only if the new cell is unoccupied)
        """
        occupied = self.board.get_cell(new_cell) != None
        if not occupied:
            self.board.set_cell(player.cell, None)
            self.board.set_cell(new_cell, player)
            player.cell = new_cell


    def play_with_neighbors(self, player):
        """ makes a player play a game with its four neighbors and update its
        total payoff
        """
        neighbors = self.board.get_neumann_neighboring_players(player.cell)

        player.payoff = 0
        for neighbor in neighbors:
            player.payoff += self.game.play(player, neighbor)[0]


    def noise1_update(self, player):
        """ resets the strategy of the player according to the Noise 1 process
        described in the Helbing paper
        """
        rand = random.random()
        if rand < self.q:
            player.strategy = Strategy.cooperate
        else:
            player.strategy = Strategy.defect


    def noise2_update(self, player):
        """ randomizes the location of the player according to the Noise 1
        process described in the Helbing paper
        """
        random_cell_sequence = self.board.random_cell_sequence()
        while random_cell_sequence:
            random_cell = random_cell_sequence.pop(0)
            if not self.board.occupied(random_cell):
                self.move_player(player, random_cell)
                break


    def migration_update(self, player):
        """ performs a migration step for a player according to the migration
        process described in the Helbing paper
        """
        # dictionary to record most favorable cell in neighborhood
        migration_score = {}

        # calculate payoff in current cell
        current_cell = player.cell
        self.play_with_neighbors(player)
        migration_score[player.cell] = player.payoff

        # simulate payoffs in neighboring empty cells
        empty_cells = self.board.get_moore_neighboring_empty_cells(player.cell, self.moore_neighborhood_range)
        for empty_cell in empty_cells:
            self.move_player(player, empty_cell)
            self.play_with_neighbors(player)
            migration_score[player.cell] = player.payoff

        # migrate to most favorable cell
        most_favorable_cell = max(migration_score, key=migration_score.get)
        self.move_player(player, most_favorable_cell)


    def imitation_update(self, player):
        """ performs an imitation step for a player according to the imitation
        process described in the Helbing paper
        """
        most_successful_neighbor = player
        greatest_payoff = player.payoff

        neighbors = self.board.get_neumann_neighboring_players(player.cell)
        for neighbor in neighbors:
            if neighbor.payoff > greatest_payoff:
                greatest_payoff = neighbor.payoff
                most_successful_neighbor = neighbor

        player.strategy = most_successful_neighbor.strategy

    def get_num_players_with_stretegy(self, strat):
        """ returns the number of players on the grid using a given stratgy
        """
        counter = 0
        for i in range(len(self.players)):
            if self.players[i].strategy == strat:
                counter += 1

        return counter
