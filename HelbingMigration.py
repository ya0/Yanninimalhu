import random
from cellular_automaton import CellularAutomaton, MooreNeighborhood, EdgeRule, CAWindow
from PrisonersDilemma import PrisonersDilemma

class HelbingMigration(CellularAutomaton):
    L = 10 # side length of square game board

    # strategies
    COOPERATE = 1
    DEFECT = 0
    INACTIVE = -1

    # prisoner's dilemma game played between neighbors
    game = PrisonersDilemma(3, 2, 0, 1)

    r = 0.1 # probability that the agent randomly resets their strategy
    q = 0.01 # probability that the agent resets to COOPERATE, given that they are resetting

    # actions
    PLAY = 1
    EVALUATE = 2
    MIGRATE = 3
    EMIGRATE = 4
    UPDATE = 5

    aspiring_immigrators = dict()
    immigrated = list()

    def __init__(self):
        super().__init__(dimension=[HelbingMigration.L, HelbingMigration.L], neighborhood=MooreNeighborhood(EdgeRule.IGNORE_MISSING_NEIGHBORS_OF_EDGE_CELLS))

    def init_cell_state(self, coordinates):
        # randomly assign cooperative and defecting behaviours to agents
        rand = random.random()
        if rand < 0.6:
            strategy = HelbingMigration.COOPERATE
        elif rand < 0.65:
            strategy = HelbingMigration.DEFECT
        else:
            strategy = HelbingMigration.INACTIVE

        # coordinates of cell (required for migration step)
        xcoord, ycoord = coordinates

        # initialize total payoff
        total_payoff = 0

        # set next action to play (as we require alternating playing and update rounds)
        next_action = HelbingMigration.PLAY

        state = (xcoord, ycoord, next_action, strategy, total_payoff)
        return state

    def evolve_rule(self, last_cell_state, neighbors_last_states):
        # make sure migration dictionary is clear for next step
        HelbingMigration.aspiring_immigrators.clear()

        # check whether this is an "update", "inactive play cooperate", "inactive play defect", "evalute", "migrate", or "update" round.
        action = last_cell_state[2]

        # play prisoner's dilemma game with neighbors
        if action == HelbingMigration.PLAY:

            if last_cell_state[3] == HelbingMigration.INACTIVE:
                # simulate games in empty sites with both strategies
                total_payoff_coop = 0
                total_payoff_defect = 0
                for neighbor_state in neighbors_last_states:
                    if neighbor_state[3] != HelbingMigration.INACTIVE:
                        total_payoff_coop += self.game.make_a_deal(HelbingMigration.COOPERATE, neighbor_state[3])[0]
                        total_payoff_defect += self.game.make_a_deal(HelbingMigration.DEFECT, neighbor_state[3])[0]
                new_cell_state = (last_cell_state[0], last_cell_state[1], HelbingMigration.EVALUATE, HelbingMigration.INACTIVE, total_payoff_coop, total_payoff_defect)

            else:
                # play games between active agents
                total_payoff = 0
                for neighbor_state in neighbors_last_states:
                        if neighbor_state[3] != HelbingMigration.INACTIVE:
                            total_payoff += self.game.make_a_deal(last_cell_state[3], neighbor_state[3])[0]
                new_cell_state = (last_cell_state[0], last_cell_state[1], HelbingMigration.EVALUATE, last_cell_state[3], total_payoff)

            return new_cell_state

        # check whether active agents would benefit from moving
        if action == HelbingMigration.EVALUATE:

            if last_cell_state[3] == HelbingMigration.INACTIVE:
                return (last_cell_state[0], last_cell_state[1], HelbingMigration.MIGRATE, last_cell_state[3])

            for neighbor_state in neighbors_last_states:
                # check the payoffs of inactive cells using agent's strategy
                if neighbor_state[3] == HelbingMigration.INACTIVE:

                    if last_cell_state[3] == HelbingMigration.COOPERATE:
                        if neighbor_state[4] > last_cell_state[4]:
                            # desirable to migrate
                            if (neighbor_state[0], neighbor_state[1]) in HelbingMigration.aspiring_immigrators:
                                HelbingMigration.aspiring_immigrators[(neighbor_state[0], neighbor_state[1])].append(last_cell_state)
                            else:
                                HelbingMigration.aspiring_immigrators[(neighbor_state[0], neighbor_state[1])] = last_cell_state

                    elif last_cell_state[1] == HelbingMigration.DEFECT:
                        if neighbor_state[5] > last_cell_state[4]:
                            # desirable to migrate
                            if (neighbor_state[0], neighbor_state[1]) in HelbingMigration.aspiring_immigrators:
                                HelbingMigration.aspiring_immigrators[(neighbor_state[0], neighbor_state[1])].append(last_cell_state)
                            else:
                                HelbingMigration.aspiring_immigrators[(neighbor_state[0], neighbor_state[1])] = last_cell_state

            return (last_cell_state[0], last_cell_state[1], HelbingMigration.MIGRATE, last_cell_state[3], last_cell_state[4])

        # move agents *into* desirable empty sites
        if action == HelbingMigration.MIGRATE:

            if last_cell_state[3] != HelbingMigration.INACTIVE:
                new_cell_state = (last_cell_state[0], last_cell_state[1], HelbingMigration.EMIGRATE, last_cell_state[3], last_cell_state[4])

            else:
                new_cell_state = (last_cell_state[0], last_cell_state[1], HelbingMigration.EMIGRATE, last_cell_state[3], last_cell_state[4])

                if HelbingMigration.aspiring_immigrators((last_cell_state[0], last_cell_state[1])):
                    immigration = 0
                    while(immigration == 0 and HelbingMigration.aspiring_immigrators):
                        immigrant = random.choice(HelbingMigration.aspiring_immigrators)
                        HelbingImitation.aspiring_immigrators.remove(immigrant)
                        if immigrant not in HelbingMigration.immigrated:
                            HelbingMigration.immigrated.append(immigrant)
                            immigration = 1
                            new_cell_state = (immigrant[0], immigrant[1], HelbingMigration.EMIGRATE, immigrant[3], immigrant[4])

            return new_cell_state

        # move agents *out of* their undesirable current cells
        if action == HelbingMigration.EMIGRATE:

            if last_cell_state[3] == HelbingMigration.INACTIVE:
                new_cell_state = (last_cell_state[0], last_cell_state[1], HelbingMigration.EMIGRATE, last_cell_state[3], last_cell_state[4])

            else:
                # I need to remove the round from the state for the list reference to work here.
                new_cell_state = last_cell_state

            return new_cell_state

    @staticmethod
    def state_to_color(state):
        if state[3] == HelbingMigration.COOPERATE:
            return 0, 0, 255 # color cooperators blue
        elif state[3] == HelbingMigration.DEFECT:
            return 255, 0, 0 # color defectors red
        else:
            return 0, 0, 0 # color inactive cells black

if __name__ == "__main__":
    CAWindow(cellular_automaton=HelbingMigration(),
             window_size=(800, 600), state_to_color_cb=HelbingMigration.state_to_color).run(evolutions_per_second=1)
