import numpy as np
import pygame as pg
import itertools
import random
import time

from PrisonersDilemma import PrisonersDilemma, Player, Strategy
from RectangularGrid import RectangularGrid

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

def init_grid(width, height, cell_type=bool ):
    return RectangularGrid(height, width)

def init_cell_states(grid):
    """ the integer in the cell describes the strategy of that cell/actor.
    0: empty cell
    1: defect
    2: cooperate

    for the future: i think it is possible to save objects into numpy arrays
    but we could also just reference different strategies by numbers. if we
    want to distinguish between actors we need ID's or save an actual object.
    """
    for i in range(grid.width):
        for j in range(grid.height):
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
    static function and not future proof at all
    """
    for i in range(grid.width):
        for j in range(grid.height):

            # define top-left pixel of cell
            tup = (i * 16, j * 16, 16, 16)

            # determine cell colouring
            player = grid.grid[i][j]
            if player:
                if player.strategy == Strategy.cooperate:
                    pg.draw.rect(screen, (0, 255, 0), tup, 0)
                elif player.strategy == Strategy.defect:
                    pg.draw.rect(screen, (255, 0, 0), tup, 0)
                else:
                    pg.draw.rect(screen, (0, 0, 0), tup, 0)
            else:
                pg.draw.rect(screen, (0, 0, 0), tup, 0)

    pg.display.flip()

def get_neighbors(grid, i, j):
    """ returns a list of neighbors of a player at grid coordinates (i,j)
    """
    neighbors = []
    possible_neighbor_positions = [[i+1, j], [i-1, j], [i, j+1], [i, j-1]]

    for pnp in possible_neighbor_positions:
        # ignore cases when the possible neighbor index is out of bounds
        try:
            grid.grid[pnp[0], pnp[1]]
            # check whether neighboring cell contains a player
            if grid.grid[pnp[0], pnp[1]]:
                neighbors.append(n)
        except:
            continue

    return neighbors

def play_with_4_neighbors(grid, i, j, game):
    """ (i,j) plays the prisoners dilemma pd with neighbors in the grid
    return sum off all the games
    """
    neighbors = get_neighbors(grid, i, j)

    player = grid.grid[i][j]
    payoff = 0
    for neighbor in neighbors:
        payoff += game.Play(player, neighbor)[0]

    return payoff

def move(grid, player, x_new, y_new):
    try:
        # move player to new position if empty
        occupied = grid.grid[x_new][y_new] != None
        print(occupied)
        if not occupied:
            x_old = player.x_pos
            y_old = player.y_pos

            grid.grid[x_new][y_new] = player
            player.x_pos = x_new
            player.y_pos = y_new

            grid.grid[x_old][y_old] = None

    except:
        return

def update_player(player, grid, game):
    move(grid, player, player.x_pos + 1, player.y_pos + 1)
    # payoff = play_with_4_neighbors(grid, player.x_pos, player.y_pos, game)

def imitate_single_individual(grid, pd):
    """ select one individual  and compute the sum over the PD with its
    neighbors then compute the same for the neighbors and change to the
    strategy of the best neighbor"""
    # select random individual
    (i, j) = (np.random.randint(0, grid.width),
         np.random.randint(0, grid.height))

    # find a cell that actualy has a player
    counter = 0
    while not grid.grid[i][j].Active() and counter < 30:
        (i, j) = (np.random.randint(0, grid.width),
         np.random.randint(0, grid.height))
        counter += 1

    payoff = play_with_4neighbors(pd, grid, i, j)

    # list of potential neighbors
    neighbors = get_neighbors(grid,i,j)
    # only consider neighbors that are actual players and not empty
    neighbors = [n for n in neighbors if grid[n[0],n[1]]]

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
        grid[i,j] = grid[better_neighbor[0], better_neighbor[1]]


def migration(game):

    # grid setup
    x_dim = 30
    y_dim = 30
    grid = init_grid(y_dim, x_dim)
    init_cell_states(grid)

    # screen setup
    background_color = (0, 0, 0)
    cell_height = 16
    cell_width = 16
    screen_dimensions = (cell_width * x_dim, cell_height * y_dim)
    screen = setup_screen(screen_dimensions, background_color)

    # first rendering
    draw_update(screen, grid)

    # simulation loop
    running = True
    counter = 0
    while running:
        if counter >= 10000:
            running = False

        if running:
            # choose a player at random
            players = []
            for i in range(grid.width):
                for j in range(grid.height):
                    if grid.grid[i][j]:
                        players.append(grid.grid[i][j])
            if players:
                player = random.choice(players)
            else:
                running = False

            # update player strategy and position
            update_player(player, grid, game)

        draw_update(screen, grid)

        # proper closing of the window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()

if __name__ == "__main__":
    game = PrisonersDilemma(4, 3, 2, 1)
    migration(game)
