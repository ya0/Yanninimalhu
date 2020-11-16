# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 11:11:06 2020

@author: amman
"""
import numpy as np
import pygame as pg
import itertools
import time

# other file. for modeling the PrisonersDilemma. at the moment very empty
# in the future maybe just one file
from PrisonersDilemma import PrisonersDilemma, Player, Strategy
from RectangularGrid import RectangularGrid

# egsample i think form the paper
pd = PrisonersDilemma(1.3, 1, 0, 0.1)

"""states: 0 empty, 1 allways defect, 0 allwaasy cooperate (subject to change)
i chose this numbering because to calculate a "deal" 0 stands for defecting and
1 for cooperating. so just subtracting 1 from the cell value gives the correct
optin"""

# sets up the screen (dimensions, title, background color)
def setup_screen(screen_dimensions, background_colour):
    """ some things for the graphics....
    """
    pg.init()
    screen = pg.display.set_mode((screen_dimensions[1], screen_dimensions[0]))
    pg.display.set_caption("Conway's Game of Life")
    screen.fill(background_colour)
    pg.display.flip()
    return screen

# sets up the grid for the game (grid of rectangular cells)
def init_grid(horizontal_cells, vertical_cells, cell_type=bool):
    """ initialices and returns a numpy array with given dimension and datatype
    (maybe we can define our own datatype)
    """
    return RectangularGrid(horizontal_cells, vertical_cells)

def init_cell_states(grid):
    """ the integer in the cell describes the strategy of that cell/actor.
    0: empty cell
    1: defect
    2: cooperate

    for the future: i think it is possible to save objects into numpy arrays
    but we could also just reference different strategies by numbers. if we
    want to distinguish between actors we need ID's or save an actual object.
    """
    for i in range(grid.height):
        for j in range(grid.width):
            r = np.random.random()
            if r > 0.5:
                grid.grid[i][j] = None
            elif r > 0.25:
                grid.grid[i][j] = Player(Strategy.cooperate, i, j)
            else:
                grid.grid[i][j] = Player(Strategy.defect, i, j)

# draws a rectangle for each cell that is alive
def draw_update(screen, grid):
    """ updates the display according the the grid (numpy matrix) this is a very
    static functoin and not future prove at all
    """
    for i in range(grid.height):
        for j in range(grid.width):
            tup = (i * 16, j * 16, 16, 16)

            player = grid.grid[i][j]
            if player:
                if player.strategy == Strategy.cooperate:
                    pg.draw.rect(screen, (0,255,0), tup, 0)
                elif player.strategy == Strategy.defect:
                    pg.draw.rect(screen, (255,0,0), tup, 0)
                else:
                    pg.draw.rect(screen, (0, 0, 0), tup, 0)
    pg.display.flip()


def get_neighbors(grid, i, j):
    """ returns a list of possible neighbors of an index (i.j)
    """
    neighbors = []
    #define list of neighbors to check if they can be added
    possible = [[i+1,j], [i-1,j], [i,j+1], [i,j-1]]

    for n in possible:
        # if the index is out of bounds just ignors this case and continues
        try:
            grid.grid[n[0]][n[1]]
            neighbors.append(n)
        except:
            True

    return neighbors



def play_with_4neighbors(pd, grid, i, j):
    """ (i,j) plays the prisoners dilemma pd with neighbors in the grid
    return sum off all the games
    """
    payoff = 0
    neighbors = get_neighbors(grid,i,j)

    for n in neighbors:
        if grid.grid[n[0]][n[1]] != None:
            payoff += pd.play(grid.grid[i][j], grid.grid[n[0]][n[1]])[0]

    return payoff



def imitate_single_individual(grid, pd):
    """ select one individual  and compute the sum over the PD with its
    neighbors then compute the same for the neightbors and change to the
    strategy of the best neighbor"""
    # select random individual
    (i, j) = (np.random.randint(0, grid.height),
         np.random.randint(0, grid.width))

    # find a cell that actualy has a player...
    counter = 0
    while not grid.grid[i][j] and counter < 30:
        (i, j) = (np.random.randint(0, grid.height),
         np.random.randint(0, grid.width))
        counter += 1

    payoff = play_with_4neighbors(pd, grid, i, j)

    # list of potential neighbors
    neighbors = get_neighbors(grid,i,j)
    # only consider neighbors that are actual players and not empty
    neighbors = [n for n in neighbors if grid.grid[n[0]][n[1]]]

    # no neighbors.. just return?
    if not neighbors:
        return

    # calculate the payoff of all the neighbors
    neighbors_payoff = []
    for n in neighbors:
        neighbors_payoff.append(play_with_4neighbors(pd, grid, n[0], n[1]))

    # no good neighbors ? idk
    if not neighbors_payoff:
        return

    best_neighbor = max(neighbors_payoff)

    if best_neighbor > payoff:
        better_neighbor = neighbors[neighbors_payoff.index(best_neighbor)]
        grid.grid[i][j] = grid.grid[better_neighbor[0]][better_neighbor[1]]


"""

background_colour = (0, 0, 0)
width, height = 2 ** 10, 2 ** 10
cell_size = 2 ** 4
horizontal_cells, vertical_cells = width // cell_size, height // cell_size


grid = init_grid(horizontal_cells, vertical_cells, cell_type=int)
init_cell_states(grid)
"""


def imitation():
    """
    main function that executes the whole simulation
    """

    background_color = (0, 0, 0)
    # setup the matrix dimenision
    x_dim = 30
    y_dim = 40
    # the cell sizes are 16*16 pixels
    screen_dimensions = (x_dim*16, y_dim*16)
    # get screen for running the graphics
    screen = setup_screen(screen_dimensions, background_color)
    # initiate the grid and set it up with individuals
    grid = init_grid(x_dim, y_dim, cell_type=int)
    init_cell_states(grid)
    # first rendering
    draw_update(screen, grid)

    # simulation loop
    running = True
    while running:
        # this loop makes the graphics run faster for a bigger range without
        # updating the greaphics
        imitate_single_individual(grid, pd)
        #imitate_single_individual(grid, pd)
        draw_update(screen, grid)

        # proper closing of the window....
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
                #exit()



imitation()



#screen = setup_screen()
#draw_update(screen, grid)
