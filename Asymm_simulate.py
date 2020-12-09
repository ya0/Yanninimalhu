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
    T = 2.1
    R = 1
    P = 0.3
    S = 0.1
    game = AsymmetricPrisonersDilemma(T, R, P, S)

    # define a world topology ("board") - e.g. grid, network
    # choose a board type from Board.py
    grid_height = 49
    grid_width = 49
    board = RectangularGrid(grid_height, grid_width)

    # define the players in the world
    # choose a player type from Game.py
    num_players = grid_height * grid_width // 2
    p_cooperation = 0.5
    coops=[]
    for n in range(1,10):
        coops=[]
        for i in range(0, 11):
            p=i // 10 ## prob that need is not satisfied

            players = []
            for i in range(num_players):
                rand = random.random()
                if rand < p_cooperation:
                    players.append(AsymmetricPrisonersDilemmaPlayer(Strategy.cooperate,p))
                else:
                    players.append(AsymmetricPrisonersDilemmaPlayer(Strategy.defect,p))

            # define player update parameters
            r = 0.05 # probability that a player randomly resets its strategy
            q = 0.05 # conditional probability that a player resets to cooperate
            noise1 = True # a boolean indicating whether Noise 1 is present
            noise2 = False # a boolean indicating whether Noise 2 is present
            imitation = True # a boolean indicating whether players perform imitation
            migration = True # a boolean indicating whether players perform migration
            M = 5 # the range of the Moore neighborhood around each cell

            # simulation parameters
            time_max = 30
            iteration_max = 200
            show_animation = False

            # define the statistics to record in the simulation
            # choose a simulations type from SimulationsStatistics.py
            stats = StrategyFractionsTimeSeries()
            

            # define the world to simulate evolution of strategies
            world = World(game, board, players, r, q, noise1, noise2, imitation, migration, M)

            # perform simulation
            
            simulate(world, stats, time_max, iteration_max, show_animation)
            coops.append(stats.record_stats(world,iteration_max))
            #print(coops)
            #f=open("/Users/malvika/Downloads/Yanninimalhu-master 4/coops.txt","w")
            ##f.close()

        with open('/Users/malvika/Downloads/Yanninimalhu-master 4/{0}{1}.txt'.format("coops_", n), 'w') as f:
            for item in coops:
                f.write("%s\n" % item)
            
