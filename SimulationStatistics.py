import abc, time, matplotlib.pyplot as plt
from Game import Strategy

class SimulationStatistics(abc.ABC):
    @abc.abstractmethod
    def record_stats(self, world, iteration):
        pass

    # override if desired
    def end_simulation(self, world, iteration):
        return False

    @abc.abstractmethod
    def print_results(self):
        pass


class StrategyFractionsTimeSeries(SimulationStatistics):
    def __init__(self):
        self.cooperator_fraction_ts = []
        self.defector_fraction_ts = []

    def record_stats(self, world, iteration):
        cooperator_fraction = \
            world.get_num_players_with_strategy(Strategy.cooperate)
        defector_fraction = \
            world.get_num_players_with_strategy(Strategy.defect)

        self.cooperator_fraction_ts.append(cooperator_fraction \
            / world.num_players)
        self.defector_fraction_ts.append(defector_fraction \
            / world.num_players)

    def end_simulation(self, world, iteration):
        if iteration > 500:
            return True
        else:
            return False

    def print_results(self):
        self.figure = plt.figure("Strategy Fractions Time Series")

        cooperator_fraction_plot = \
            plt.plot(self.cooperator_fraction_ts, label="Cooperator fraction")
        defector_fraction_plot = \
            plt.plot(self.defector_fraction_ts, label="Defector fraction")

        plt.xlabel('Iteration')
        plt.ylabel('Fraction of players with strategy')
        plt.legend()
        
        self.figure.canvas.flush_events()
        plt.show()

        # sleep to prevent results disappearing immediately
        time.sleep(20)
