# -*- coding: utf-8 -*-

###########################################
# redundant file atm
###########################################



"""
simulate the pirsoners dilemma
"""
from enum import Enum
import numpy as np

class Strategy(Enum):
    cooperate = 0
    defect = 1

class Player():
    def __init__(self, strategy, x, y, p):
        self.strategy = strategy
        self.i = x  # vertical position
        self.j = y  # horizontal position
        self.money = 0
        self.physio = np.random.choice(np.arange(0,2), p=[p, 1-p])
        self.safety = self.physio*np.random.choice(np.arange(0,2), p=[p, 1-p])
        self.love = self.safety*np.random.choice(np.arange(0,2), p=[p, 1-p])
        self.esteem = self.love*np.random.choice(np.arange(0,2), p=[p, 1-p])
        self.fulfill = self.esteem*np.random.choice(np.arange(0,2), p=[p, 1-p])

class AsPrisonersDilemma():
    def __init__(self, T, R, P, S):
        """ initialise the prisoners dilemma with:
            T: temptation
            R: reward
            S: sucker's payoff
            P: punishment
        """
        self.T = T
        self.R = R
        self.P = P
        self.S = S

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
