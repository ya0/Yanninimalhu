import random
from Game import Strategy
from Board import RectangularGrid

"""
The world in which the simulation takes place
"""
class World():
    def __init__(self, game, board, players, r = 0, q = 0, noise1 = False, noise2 = False, imitation = False, migration = False, M = 0):
        """
        - game: game played between two players during an interaction
        - board: topology of the world
        - players: a list of players in the world
        - r: probability that a player randomly resets its strategy
        - q: conditional probability that a player resets to cooperate
        - noise1: a boolean indicating whether Noise 1 is present
        - noise2: a boolean indicating whether Noise 2 is present
        - imitation: a boolean indicating whether players perform imitation
        - migration: a boolean indicating whether players perform migration
        - M: the range of the Moore neighborhood around each cell
        """
        self.game = game
        self.board = board
        self.num_players = len(players)
        self.players = players
        self.r = r
        self.q = q
        self.noise1 = noise1
        self.noise2 = noise2
        self.imitation = imitation
        self.migration = migration
        self.M = M

        # randomly insert players in board cells
        random_cell_sequence = board.random_cell_sequence()
        if len(players) > len(random_cell_sequence):
            print("Error! Number of players exceeds the number of cells")
            quit()

        random.shuffle(self.players)
        for i in range(len(self.players)):
            self.players[i].cell = random_cell_sequence[i]
            self.board.assign_player_to_cell(self.players[i], \
                                            random_cell_sequence[i])


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
        occupied = self.board.get_player_from_cell(new_cell) != None
        if not occupied:
            self.board.assign_player_to_cell(None, player.cell)
            self.board.assign_player_to_cell(player, new_cell)
            player.cell = new_cell


    def play_with_neighbors(self, player):
        """ makes a player play a game with its four neighbors and record its
        total payoff
        """
        neighbors = self.board.get_players_in_play_neighborhood(player.cell)

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
        """ randomizes the location of the player according to the Noise 2
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
        current_cell = player.cell

        # dictionary to record most favorable cell in neighborhood
        migration_payoff = {}

        # calculate payoff in current cell
        current_cell = player.cell
        self.play_with_neighbors(player)
        migration_payoff[player.cell] = player.payoff
        best_payoff = player.payoff

        # simulate payoffs in neighboring empty cells
        empty_cells = \
            self.board.get_empty_cells_in_migration_neighboorhood(player.cell, self.M)
        for empty_cell in empty_cells:
            self.move_player(player, empty_cell)
            self.play_with_neighbors(player)

            migration_payoff[player.cell] = player.payoff
            if player.payoff > best_payoff:
                best_payoff = player.payoff

        # migrate to most closest favorable cell
        best_cells = []
        for cell in migration_payoff:
            if migration_payoff[cell] == best_payoff:
                best_cells.append(cell)

        random.shuffle(best_cells)
        closest_best_cell = min(best_cells, key=lambda cell: self.board.get_distance_between(cell, current_cell))
        self.move_player(player, closest_best_cell)


    def imitation_update(self, player):
        """ performs an imitation step for a player according to the imitation
        process described in the Helbing paper
        """
        most_successful_neighbor = player
        greatest_payoff = player.payoff

        neighbors = self.board.get_players_in_play_neighborhood(player.cell)
        for neighbor in neighbors:
            # check payoff of neighbor in its current neighborhood
            self.play_with_neighbors(neighbor)

            if neighbor.payoff > greatest_payoff:
                greatest_payoff = neighbor.payoff
                most_successful_neighbor = neighbor

        player.strategy = most_successful_neighbor.strategy

    def get_num_players_with_strategy(self, strat):
        """ returns the number of players on the grid using a given stratgy
        """
        counter = 0
        for i in range(len(self.players)):
            if self.players[i].strategy == strat:
                counter += 1

        return counter
