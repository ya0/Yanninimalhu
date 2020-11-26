# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 13:19:59 2020

@author: amman
"""

"""
simulate the pirsoners dilemma
"""
from enum import Enum
import numpy as np

class Strategy(Enum):
    cooperate = 0
    defect = 1

class Player():
    def __init__(self, strategy, x, y, p = False):
        self.strategy = strategy
        self.i = x  # vertical position
        self.j = y  # horizontal position
        self.money = 0
        # if players is initialised with a p value we set the assimetric model
        self.asymetric = False
        if p:
            self.asymetric = True
            self.physio = np.random.choice(np.arange(0,2), p=[p, 1-p])
            self.safety = self.physio*np.random.choice(np.arange(0,2), p=[p, 1-p])
            self.love = self.safety*np.random.choice(np.arange(0,2), p=[p, 1-p])
            self.esteem = self.love*np.random.choice(np.arange(0,2), p=[p, 1-p])
            self.fulfill = self.esteem*np.random.choice(np.arange(0,2), p=[p, 1-p])


class PrisonersDilemma():
    def __init__(self, T, R, P, S):
        """ initialise the prisoners dilemma with:
            T: temptacion
            R: reward
            S: sucker's payoff
            P: punishment
        """
        self.T = T
        self.R = R
        self.P = P
        self.S = S
        
    def make_a_deal(self, player_one, player_two):
        """
        do not delete
        making a deal evaluates a deal. each player can cooperate "1" or be
        egoistic "0"
        Parameters:
            - player_one, player_two: take True,False (respectifely 1 and 0)
        returns:
            tuple (payoff_one, payoff_two)
        """
        if player_one and player_two:
            return (self.R, self.R)
        elif not player_one and not player_two:
            return (self.P, self.P)
        elif player_one < player_two:
            return (self.T, self.S)
        else:
            return (self.S, self.T)

    def play(self, p1: Player, p2: Player):
        if p1.strategy == Strategy.cooperate:
            if p2.strategy == Strategy.cooperate:
                return (self.R, self.R)
            elif p2.strategy == Strategy.defect:
                return (self.S, self.T)
        elif p1.strategy == Strategy.defect:
            if p2.strategy == Strategy.cooperate:
                return (self.T, self.S)
            elif p2.strategy == Strategy.defect:
                return (self.P, self.P)
        else:
            print("Player strategies not well defined!")
            exit()
            
            
class AsPrisonersDilemma(PrisonersDilemma):
    """
    child class with new asymmetric play function
    """
    def play(self, p1: Player, p2: Player):
        if p1.strategy == Strategy.cooperate:
            if p2.strategy == Strategy.cooperate:
                return (self.R*(1+(p1.physio + p1.safety + p1.love + p1.esteem + p1.fulfill)/5),
                        self.R*(1+(p2.physio + p2.safety + p2.love + p2.esteem + p2.fulfill)/5))
            elif p2.strategy == Strategy.defect:
                return (self.S*(1+(p1.love + p1.esteem)/2),
                        self.T*(2/(1+(p2.physio + p2.safety + p2.love + p2.esteem + p2.fulfill)/5)))
        elif p1.strategy == Strategy.defect:
            if p2.strategy == Strategy.cooperate:
                return (self.T*(2/(1+(p1.physio + p1.safety + p1.love + p1.esteem + p1.fulfill)/5)),
                        self.S*(1+(p2.love + p2.esteem)/2))
            elif p2.strategy == Strategy.defect:
                return (self.P*(1+p1.fulfill), self.P*(1+p2.fulfill))
        else:
            print("Player strategies not well defined!")
            exit()
