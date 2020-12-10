import random, time, matplotlib.pyplot as plt
from World import World
from Board import RectangularGrid
from Game import PrisonersDilemma, AsymmetricPrisonersDilemma, Player, \
    PrisonersDilemmaPlayer, AsymmetricPrisonersDilemmaPlayer, Strategy
from SimulationStatistics import StrategyFractionsTimeSeries

def simulate(world, stats=None, time_max = 30, iteration_max = 100000, \
            show_animation = False):
    """ simulates the evolution of strategies in the world, allowing for
    visualization and the recording of statistics
    """
    if show_animation:
        world.board.draw()

    t = time.time()
    time_max = t + time_max
    iteration = 0
    while t < time_max and iteration < iteration_max:
        # perform one round of updates
        world.round()
        if show_animation:
            world.board.draw()

        # record statistics
        if stats:
            stats.record_stats(world, iteration)
            # stop simulation based on statistics
            if stats.end_simulation(world, iteration):
                break


        # update loop variables
        iteration += 1
        t = time.time()

    if stats:
        stats.print_results()

if __name__ == "__main__":
    """ Adjust simulation parameters here """

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

    # define the players in the world
    # choose a player type from Game.py
    num_players = grid_height * grid_width // 2
    p_cooperation = 0.5

    players = []
    for i in range(num_players):
        rand = random.random()
        if rand < p_cooperation:
            players.append(PrisonersDilemmaPlayer(Strategy.cooperate))
        else:
            players.append(PrisonersDilemmaPlayer(Strategy.defect))

    # define player update parameters
    r = 0.05 # probability that a player randomly resets its strategy
    q = 0.05 # conditional probability that a player resets to cooperate
    noise1 = False # a boolean indicating whether Noise 1 is present
    noise2 = False # a boolean indicating whether Noise 2 is present
    imitation = False # a boolean indicating whether players perform imitation
    migration = False # a boolean indicating whether players perform migration
    M = 5 # the range of the Moore neighborhood around each cell

    # simulation parameters
    time_max = 10
    iteration_max = 1000
    show_animation = True

    # define the statistics to record in the simulation
    # choose a simulations type from SimulationsStatistics.py
    stats = StrategyFractionsTimeSeries()

    # define the world to simulate evolution of strategies
    world = World(game, board, players, r, q, noise1, noise2, imitation, migration, M)

    # perform simulation
    simulate(world, stats, time_max, iteration_max, show_animation)
