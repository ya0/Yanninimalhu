# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 13:19:59 2020

@author: amman
"""

"""
simulate the pirsoners dilemma
"""
from enum import Enum

class Strategy(Enum):
    cooperate = 0
    defect = 1

class Player():
    def __init__(self, strategy, x, y):
        self.strategy = strategy
        self.i = x  # vertical position
        self.j = y  # horizontal position
        self.money = 0

class PrisonersDilemma():
    def __init__(self, T, R, P, S):
        """ initialise the prisoners dilemma with:
            T: temptasion
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
