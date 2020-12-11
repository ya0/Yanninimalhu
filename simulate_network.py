import random, time, matplotlib.pyplot as plt
from World import World
from Board import RectangularGrid, Network
from Game import (
    PrisonersDilemma,
    AsymmetricPrisonersDilemma,
    Player,
    PrisonersDilemmaPlayer,
    AsymmetricPrisonersDilemmaPlayer,
    Strategy,
)
from SimulationStatistics import StrategyFractionsTimeSeries4Network
import numpy as np


def simulate(
    world, stats=None, time_max=30, iteration_max=100000, show_animation=False
):
    """simulates the evolution of strategies in the world, allowing for
    visualization and the recording of statistics
    """
    if show_animation:
        world.board.draw()

    # record statistics
    if stats:
        stats.record_stats(world, 0)

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
        cooperator_fraction_ts = stats.print_results()

    # Returns the fraction of cooperators
    return cooperator_fraction_ts


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
    # grid_height = 50
    # grid_width = 50
    # board = RectangularGrid(grid_height, grid_width)
    num_nodes = 100  # Number of nodes
    number_cases = 10  # Number of simulations
    number_single = 10  # Number of samples for each simulation

    k = np.linspace(2, 15, number_cases)  # Different values of mean degree
    # p=np.linspace(0.00001,0.01,number_cases) #Different values of probability of rewiring
    average_fraction_single = 0  # Average of fraction of cooperators per simulation
    average_fraction_array = np.zeros(
        number_cases
    )  # Array with the averages of fraction of cooperators per simulation
    for z in range(0, number_cases):
        ka = int(k[z])
        # pa=p[z]
        for j in range(0, number_single):
            board = Network(num_nodes, ka, 0.05)
            # define the players in the world
            # choose a player type from Game.py
            num_players = num_nodes  # No empty cells
            p_cooperation = 0.5

            players = []
            for i in range(num_players):
                rand = random.random()
                if rand < p_cooperation:
                    players.append(PrisonersDilemmaPlayer(Strategy.cooperate))
                else:
                    players.append(PrisonersDilemmaPlayer(Strategy.defect))

            # define player update parameters
            r = 0.05  # probability that a player randomly resets its strategy
            q = 0.05  # conditional probability that a player resets to cooperate
            noise1 = True  # a boolean indicating whether Noise 1 is present
            noise2 = False  # a boolean indicating whether Noise 2 is present
            imitation = True  # a boolean indicating whether players perform imitation
            migration = False  # a boolean indicating whether players perform migration
            M = 5  # the range of the Moore neighborhood around each cell

            # simulation parameters
            time_max = 10
            iteration_max = 5000
            show_animation = False

            # define the statistics to record in the simulation
            # choose a simulations type from SimulationsStatistics.py
            stats = StrategyFractionsTimeSeries4Network()

            # define the world to simulate evolution of strategies
            world = World(
                game, board, players, r, q, noise1, noise2, imitation, migration, M
            )

            # perform simulation
            cooperator_fraction_ts = simulate(
                world, stats, time_max, iteration_max, show_animation
            )
            average_fraction_single += cooperator_fraction_ts[-1]
            print(
                "Sum of fractions for each simulation and each loop:",
                average_fraction_single,
            )
        average_fraction_array[z] = average_fraction_single / number_single
        average_fraction_single = 0
        print(
            "Average fraction of cooperators for each simulation=",
            average_fraction_array[z],
        )

    plt.plot(k, average_fraction_array, marker="o")
    plt.xlabel("Value of k")
    plt.ylabel("Average fraction of cooperators with noise")
