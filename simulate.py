import random, time
from World import World
from Board import RectangularGrid
from Game import PrisonersDilemma, AsymmetricPrisonersDilemma, Player, \
    PrisonersDilemmaPlayer, AsymmetricPrisonersDilemmaPlayer, Strategy
# from animation import setup_screen, draw_update

def simulate(world, time_max = 30, iteration_max = 1000000, show_animation = False):
    """ simulates the evolution of strategies in the world
    N.B. animation only works with grid topology at the moment
    """

    # TODO: Implement the animation procedure in the Board class
    # TODO: Update to allow network animation animation setup
    if show_animation:
        world.board.draw()

    # loop simulation
    t = time.time()
    time_max = t + time_max
    iteration = 0
    while t < time_max and iteration < iteration_max:
        world.round()

        if show_animation:
            world.board.draw()

        iteration += 1
        t = time.time()

        if iteration == 200:
            time.sleep(5)

if __name__ == "__main__":

    # define the game played between two players during an interaction
    # choose a game type from Game.py
    T = 1.3
    R = 1
    P = 0.1
    S = 0
    game = PrisonersDilemma(T, R, P, S)

    # define a world topology ("board") - e.g. grid, network
    # choose a board type from Board.py
    grid_height = 50
    grid_width = 50
    board = RectangularGrid(grid_height, grid_width)

    # player parameters
    num_players = grid_height * grid_width // 2
    p_cooperation = 0.5

    # define the players in the world
    # choose a player type from Game.py
    players = []
    for i in range(num_players):
        rand = random.random()
        if rand < p_cooperation:
            players.append(PrisonersDilemmaPlayer(Strategy.cooperate))
        else:
            players.append(PrisonersDilemmaPlayer(Strategy.defect))

    # define player update parameters
    r = 0.05
    q = 0.05
    noise1 = False
    noise2 = False
    imitation = False
    migration = False
    # TODO: rename this to 'M' to match the paper
    moore_neighborhood_range = 5

    # simulation parameters
    time_max = 60
    iteration_max = 1000
    show_animation = True

    # create world to simulate evolution of strategies
    world = World(game, board, players, r, q, noise1, noise2, imitation, migration, moore_neighborhood_range)
    simulate(world, time_max, iteration_max, show_animation)
