# -*- coding: utf-8 -*-
import time
from RectangularGrid import RectangularGrid
from PrisonersDilemma import AsPrisonersDilemma, PrisonersDilemma


def simulate(game, grid, time_max = 0, iteration_max = 0):
    """
    - game is a Prisonersdilemma object
    - grid is a Rectangular Grid object
    - counter is the 
    - time_max you can specify a maximal amout of seconds the simulation runs
    - iteration_max you can specify a maximal amout of iterations calculated
    
    note: if both 0 you get an endless loop
    
    
    when the simulation is done the changes can be read directly form he grid object
    """
    
    ### To Do: an option for an "adaptive" simulation length. at some point it get stable???
    
    
    #setup counters
    t = time.time()
    time_max = t + time_max if time_max else 0
    iteration = 0
    
    while t <= time_max and iteration <= iteration_max:
        grid.update_player(game)
        
        # update conditions if needed
        iteration = iteration + 1 if iteration_max else 0
        t = time.time() if time_max else 0

""" code for the simulation setup
we can define the prisoners dilemma
    PrisonersDilemma(1.3, 1 ,0 , 0.1)

and the rectangular grid
    
    RectangularGrid(width,
                    height,
                    game = PrisonersDilemma(1.3, 1 ,0 , 0.1),
                    noise = 0.05,
                    radius = 2,
                    p_cooperate = 0.25,
                    p_defect = 0.25)
"""
    
game = AsPrisonersDilemma(1.2, 1 ,0 , 0.1)
grid = RectangularGrid(30, 40, game = game, p_needs = 0.25)
from animation import animation_2d

animation_2d(10,10, game, grid)


"""
PrisonersDilemma(1.3, 1 ,0 , 0.1)
    
grid_sizes = [10,15,20,25,30,35,40,45,50,55,60]
grids = [RectangularGrid(n, n, game) for n in grid_sizes]
# quotient of how many players are strategy cooperate

quotient = []

for grid in grids:
    simulate(game, grid, time_max=2)
    cooperators = grid.get_playercount_by_stretegy(1)
    total = cooperators + grid.get_playercount_by_stretegy(0)
    
    quotient.append(cooperators)
    
    
print(quotient)
"""