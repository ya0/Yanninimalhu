# -*- coding: utf-8 -*-
from PrisonersDilemma import PrisonersDilemma, AsPrisonersDilemma, Player, Strategy
import numpy as np
import random


class RectangularGrid():
    """
    we use this class to simulate the 2d grid
    """
    
    def __init__(self, width, height, game = PrisonersDilemma(1.3, 1 ,0 , 0.1), noise = 0.05, radius = 2, p_cooperate = 0.25, p_defect = 0.25):
        """
        - width, heith of grid
        - game is a PrisonersDilemma Object which rules how the agents interact
        - radius of neightbors (mooreneighborhood)
        - p_coperate, p_defect initiates the grid with these two agent types
        """
        self.width = width
        self.height = height
        self.grid = [[0 for i in range(width)] for j in range(height)]
        
        self.noise = noise
        self.radius = radius
        
        # init players based on percentages given to the RectangularGrid object
        for i in range(self.height):
            for j in range(self.width):
                r = np.random.random()
                if r < p_cooperate:
                    self.grid[i][j] = Player(Strategy.cooperate, i, j)
                elif r < p_cooperate + p_defect:
                    self.grid[i][j] = Player(Strategy.defect, i, j)
                else:
                    self.grid[i][j] = None
                    
    def get_playercount_by_stretegy(self, strat):
        """ returns how many agents on the grid follow a given stratgy"""
        counter = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j] != None and self.grid[i][j].strategy == strat:
                    counter = counter + 1
        return counter
                    
        
    def get_neighboring_cell_coordinates(self, i, j):
        """ returns a list of coordinates of neighboring cells
        """
        # radius of the Moore neighborhood
    
        coordinates = []
    
        # obtain Moore neighborhood algorithmically
        for m in range(self.height):
            for n in range(self.width):
                if m == i and n == j:
                    continue
                elif abs(m - i) <= self.radius and abs(n - j) <= self.radius:
                    coordinates.append((m, n))
    
        return coordinates
    
    def play_with_neighbors(self, player, game):
        """ makes a player play a game with its four neighbors and update its total
        payoff
        """
        neighbor_positions = self.get_neighboring_cell_coordinates(player.i, player.j)
    
        player.money = 0
        for neighbor_position in neighbor_positions:
            neighbor = self.grid[neighbor_position[0]][neighbor_position[1]]
            if neighbor != None:
                player.money += game.play(player, neighbor)[0]
                
    def move(self, player, i_new, j_new):
        """ moves a player from its current position on the grid to the position
        defined by the coordinates (i_new, y_new)
        """
        # check that the new position is not out of bounds
        if i_new < 0 or i_new >= self.height:
            return
        if j_new < 0 or j_new >= self.width:
            return
    
        # move player to new position if empty
        occupied = self.grid[i_new][j_new] != None
        if not occupied:
            i_old = player.i
            j_old = player.j
    
            self.grid[i_new][j_new] = player
            player.i = i_new
            player.j = j_new
    
            self.grid[i_old][j_old] = None
            
            
    def update_player(self, game):
        """ updates a player based on the imitation and migration procedures
        described in the Helbing paper
        """
        # choose a player at random
        players = []
        for m in range(self.height):
            for n in range(self.width):
                if self.grid[m][n] != None:
                    players.append(self.grid[m][n])
        player = random.choice(players)
        current_position = (player.i, player.j)
    
        # dictionary to record most favorable position in neighborhood
        migration_score = {}
    
        # calculate payoff in current position
        self.play_with_neighbors(player, game)
        migration_score[current_position] = player.money
    
        # simulate payoffs in neighbouring empty positions
        neighbor_positions = self.get_neighboring_cell_coordinates(player.i, player.j)
        for (k, l) in neighbor_positions:
            neighbor = self.grid[k][l]
            if neighbor != None:
                continue
            else:
                self.move(player, k, l)
                self.play_with_neighbors(player, game)
                migration_score[(k, l)] = player.money
    
        # migrate to most favorable position
        most_favorable_position = max(migration_score, key=migration_score.get)
        self.move(player, most_favorable_position[0], most_favorable_position[1])
    
        # introduce noise
        rand1 = random.random()
        r = self.noise
    
        if rand1 < r:
            # implement random strategy reset
    
            rand2 = random.random()
            q = 0.05
            if rand2 < q:
                player.strategy = Strategy.cooperate
            else:
                player.strategy = Strategy.defect
    
        else:
            # imitate most successful neighbor
    
            self.play_with_neighbors(player, game)
            best_payoff = player.money
            best_strategy = player.strategy
    
            # find most successful neighbor
            neighbor_positions = self.get_neighboring_cell_coordinates(player.i, player.j)
            for (k, l) in neighbor_positions:
                neighbor = self.grid[k][l]
                if neighbor != None:
                    self.play_with_neighbors(neighbor, game)
                    if neighbor.money > best_payoff:
                        best_payoff = neighbor.money
                        best_strategy = neighbor.strategy
    
            player.strategy = best_strategy
