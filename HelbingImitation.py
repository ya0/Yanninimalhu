import random
from cellular_automaton import CellularAutomaton, MooreNeighborhood, EdgeRule, CAWindow
from PrisonersDilemma import PrisonersDilemma

class HelbingImitation(CellularAutomaton):
    # strategies
    COOPERATE = 1
    DEFECT = 0
    INACTIVE = -1

    # prisoner's dilemma game played between neighbors
    game = PrisonersDilemma(3, 2, 0, 1)

    # probability that the agent randomly resets their strategy
    r = 0.1

    # probability that the agent resets to COOPERATE, given that they are resetting
    q = 0.01

    # actions
    PLAY = 1
    UPDATE = 2

    def __init__(self):
        super().__init__(dimension=[100, 100], neighborhood=MooreNeighborhood(EdgeRule.IGNORE_MISSING_NEIGHBORS_OF_EDGE_CELLS))

    def init_cell_state(self, _):

        # randomly cooperative and defecting behaviours to agents
        rand = random.random()
        if rand < 0.6:
            strategy = HelbingImitation.COOPERATE
        elif rand < 0.65:
            strategy = HelbingImitation.DEFECT
        else:
            strategy = HelbingImitation.INACTIVE

        # initialize total payoff
        total_payoff = 0

        # set next action to play (as we require alternating playing and update rounds)
        next_action = HelbingImitation.PLAY

        state = (strategy, total_payoff, next_action)
        return state

    """
    The evolution process is simulated using two rounds; a "play" round in which
    the agents play the prisoner's dilemma game with their neighbors, and an
    "update" round in which the players update their strategies based on their
    own and neighbors' performances in the "play" round. The evolution
    alternates between these two rounds, using the next_action value in the
    state.
    This is done because it is impossible to access neighbors' states directly
    after playing them; this information is included only in the
    "neighbors_last_states" variable, containing information from the previous
    round.
    """
    def evolve_rule(self, last_cell_state, neighbors_last_states):
        # ignore inactive cells
        if last_cell_state[0] == HelbingImitation.INACTIVE:
            return last_cell_state

        # check whether this is an "update" or "play" round
        action = last_cell_state[2]

        if action == HelbingImitation.PLAY:
            # play prisoner's dilemma game with neighbors

            total_payoff = 0
            for neighbor_state in neighbors_last_states:
                if neighbor_state[0] != HelbingImitation.INACTIVE:
                    total_payoff += self.game.make_a_deal(last_cell_state[0], neighbor_state[0])[0]

            updated_cell_state = (last_cell_state[0], total_payoff, HelbingImitation.UPDATE)
            return updated_cell_state

        elif action == HelbingImitation.UPDATE:
            # update strategy based on results from last round

            rand = random.random()

            if rand < HelbingImitation.r:
                # reset strategy
                rand = random.random()
                if rand < HelbingImitation.q:
                    new_strategy = HelbingImitation.COOPERATE
                else:
                    new_strategy = HelbingImitation.DEFECT

            else:
                # imitate most successful neighbour's strategy ("best" strategy)
                best_strategy = last_cell_state[0]
                best_total_payoff = last_cell_state[1]

                for neighbor_state in neighbors_last_states:
                    neighbor_strategy = neighbor_state[0]
                    neighbor_total_payoff = neighbor_state[1]

                    if best_total_payoff < neighbor_total_payoff:
                        best_total_payoff = neighbor_total_payoff
                        best_strategy = neighbor_strategy

                new_strategy = best_strategy

            updated_cell_state = (new_strategy, last_cell_state[1], HelbingImitation.PLAY)
            return updated_cell_state

    @staticmethod
    def state_to_color(state):
        if state[0] == HelbingImitation.COOPERATE:
            return 0, 0, 255
        elif state[0] == HelbingImitation.DEFECT:
            return 255, 0, 0
        else:
            return 0, 0, 0

if __name__ == "__main__":
    CAWindow(cellular_automaton=HelbingImitation(),
             window_size=(800, 600), state_to_color_cb=HelbingImitation.state_to_color).run(evolutions_per_second=1)
