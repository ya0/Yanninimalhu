# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 12:43:25 2020

@author: amman
"""
import random


from cellular_automaton import CellularAutomaton, MooreNeighborhood, EdgeRule, CAWindow
from PrisonersDilemma import PrisonersDilemma


pd = PrisonersDilemma(1.2, 1 ,0.6 , 0.1)

class PrisonersDilemma(CellularAutomaton):
    
    def __init__(self):
        super().__init__(dimension=[100, 100],
                         neighborhood=MooreNeighborhood(EdgeRule.IGNORE_MISSING_NEIGHBORS_OF_EDGE_CELLS))
        
    def init_cell_state(self, _):
        rand = random.randrange(0, 4, 1)
        #return rand
    
        if rand % 2 == 0:
            return 0
        elif rand == 1:
            return 1
        else:
            return 2

            
    def evolve_rule(self, last_cell_state, neighbors_last_states):
        """ rule for each itteration, each zell will be called gets the last state
        and the states of the neighbours"""
        if last_cell_state == 0:
            return 0
        new_cell_state = last_cell_state
        money = 0
        for n in neighbors_last_states:
            money += pd.make_a_deal(last_cell_state -1, n -1)[0]
          
        # is not enough money then die
        if money < 3.5:
            new_cell_state = 0
        # if strategy not working then change
        elif money < 7.2:
            new_cell_state = 1 if last_cell_state == 2 else 2
        
        return new_cell_state
    
    
    @staticmethod
    def active_neighbours(neighbours):
        active_neighbours = []
        for n in neighbours:
            if n is not 0:
                active_neighbours.append(n)
        return active_neighbours
    

    
    
# color somehting  
def state_to_color(current_state):
    return 255 if current_state == 1 else 0, \
           255 if current_state == 2 else 0, \
           255 if current_state == 3 else 0
    
    
# call the library
CAWindow(cellular_automaton=PrisonersDilemma(), state_to_color_cb=state_to_color).run(evolutions_per_second=4)