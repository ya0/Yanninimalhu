import numpy as np
import pygame as pg
import itertools
import random
import time

from AsymmetricPrisonersDilemma import AsPrisonersDilemma, Player, Strategy
from RectangularGrid import RectangularGrid


# sets up the screen (dimensions, title, background color)
def setup_screen(screen_dimensions, background_colour):
    """ sets up graphics
    """
    pg.init()
    screen = pg.display.set_mode((screen_dimensions[1], screen_dimensions[0]))
    pg.display.set_caption("Conway's Game of Life")
    screen.fill(background_colour)
    pg.display.flip()
    return screen

def init_grid(width, height, cell_type=bool):
    return RectangularGrid(width, height)

def init_cell_states(grid):
    """ initiates players in the grid
    """
    p_cooperate = 0.25 # probability of initiating a cooperative player
    p_defect = 0.25 # probability of initiating a defecting cell
    p_needs = 0.25 # probability that a need is not met

    for i in range(grid.height):
        for j in range(grid.width):
            r = np.random.random()
            if r < p_cooperate:
                grid.grid[i][j] = Player(Strategy.cooperate, i, j, p_needs)
            elif r < p_cooperate + p_defect:
                grid.grid[i][j] = Player(Strategy.defect, i, j, p_needs)
            else:
                grid.grid[i][j] = None


def draw_update(screen, grid):
    """ updates the display according the the grid
    """
    green = (0, 255, 0)
    red = (255, 0, 0)
    black = (0, 0, 0)

    for i in range(grid.height):
        for j in range(grid.width):

            # define top-left pixel of cell
            tup = (i * 16, j * 16, 16, 16)

            # determine cell colouring
            player = grid.grid[i][j]
            if player:
                if player.strategy == Strategy.cooperate:
                    pg.draw.rect(screen, green, tup, 0)
                elif player.strategy == Strategy.defect:
                    pg.draw.rect(screen, red, tup, 0)
                else:
                    pg.draw.rect(screen, black, tup, 0)
            else:
                pg.draw.rect(screen, black, tup, 0)

    pg.display.flip()

def get_neighboring_cell_coordinates(grid, i, j):
    """ returns a list of coordinates of neighboring cells
    """
    # radius of the Moore neighborhood
    radius = 2

    coordinates = []

    # obtain Moore neighborhood algorithmically
    for m in range(grid.height):
        for n in range(grid.width):
            if m == i and n == j:
                continue
            elif abs(m - i) <= radius and abs(n - j) <= radius:
                coordinates.append((m, n))

    return coordinates

def play_with_neighbors(player, grid, game):
    """ makes a player play a game with its four neighbors and update its total
    payoff
    """
    neighbor_positions = get_neighboring_cell_coordinates(grid, player.i, player.j)
    player.money = 0
    for neighbor_position in neighbor_positions:
        neighbor = grid.grid[neighbor_position[0]][neighbor_position[1]]
        if neighbor != None:
            player.money += game.play(player, neighbor)[0]

def move(grid, player, i_new, j_new):
    """ moves a player from its current position on the grid to the position
    defined by the coordinates (i_new, y_new)
    """
    # check that the new position is not out of bounds
    if i_new < 0 or i_new >= grid.height:
        return
    if j_new < 0 or j_new >= grid.width:
        return

    # move player to new position if empty
    occupied = grid.grid[i_new][j_new] != None
    if not occupied:
        i_old = player.i
        j_old = player.j

        grid.grid[i_new][j_new] = player
        player.i = i_new
        player.j = j_new

        grid.grid[i_old][j_old] = None

def update_player(grid, game):
    """ updates a player based on the imitation and migration procedures
    described in the Helbing paper
    """
    # choose a player at random
    players = []
    for m in range(grid.height):
        for n in range(grid.width):
            if grid.grid[m][n] != None:
                players.append(grid.grid[m][n])
    player = random.choice(players)
    current_position = (player.i, player.j)

    # dictionary to record most favorable position in neighborhood
    migration_score = {}

    # calculate payoff in current position
    play_with_neighbors(player, grid, game)
    migration_score[current_position] = player.money

    # simulate payoffs in neighbouring empty positions
    neighbor_positions = get_neighboring_cell_coordinates(grid, player.i, player.j)
    for (k, l) in neighbor_positions:
        neighbor = grid.grid[k][l]
        if neighbor != None:
            continue
        else:
            move(grid, player, k, l)
            play_with_neighbors(player, grid, game)
            migration_score[(k, l)] = player.money

    # migrate to most favorable position
    most_favorable_position = max(migration_score, key=migration_score.get)
    move(grid, player, most_favorable_position[0], most_favorable_position[1])

    # introduce noise
    rand1 = random.random()
    r = 0.05

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

        play_with_neighbors(player, grid, game)
        best_payoff = player.money
        best_strategy = player.strategy

        # find most successful neighbor
        neighbor_positions = get_neighboring_cell_coordinates(grid, player.i, player.j)
        for (k, l) in neighbor_positions:
            neighbor = grid.grid[k][l]
            if neighbor != None:
                play_with_neighbors(neighbor, grid, game)
                if neighbor.money > best_payoff:
                    best_payoff = neighbor.money
                    best_strategy = neighbor.strategy

        player.strategy = best_strategy


def migration(game):
    """ runs a simulation of agents playing a game
    """

    # grid setup
    grid_width = 30
    grid_height = 40
    grid = init_grid(grid_width, grid_height)
    init_cell_states(grid)

    # screen setup
    background_color = (0, 0, 0)
    cell_height = 16
    cell_width = 16
    screen_dimensions = (cell_width * grid_width, cell_height * grid_height)
    screen = setup_screen(screen_dimensions, background_color)

    # first rendering
    draw_update(screen, grid)

    # simulation loop
    running = True
    counter = 0
    while running:

        # counter to prevent infinite loop
        counter += 1
        if counter >= 100000:
            running = False

        if running:
            # group updates together to speed up visualization
            for i in range(50):
                update_player(grid, game)
            draw_update(screen, grid)

        # proper closing of the window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()

if __name__ == "__main__":
    game = AsPrisonersDilemma(1.3, 1 ,0 , 0.1)
    migration(game)
