# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 13:19:59 2020

@author: amman
"""

"""
simulate the pirsoners dilemma
"""

class PrisonersDilemma():
    
    T = 0
    R = 0
    S = 0
    P = 0
    
    def __init__(self, T, R, S, P):
        """ initialise the prisoners dilemma with:
            T: temptasion
            R: reward
            S: sucker's payoff
            P: punishment
            
            eg:
            pd = PrisonersDilemma(1.3, 1 ,0 , 0.1)
        """
        self.T = T
        self.R = R
        self.S = S
        self.P = P
        
        
    def make_a_deal(self, player_one, player_two):
        """ making a deal evaluates a deal. each player can cooperate "1" or be
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
        
class PlayerModel():
    p = 0
    money = 0
    
    def __init__(self, p):
        """ set player by describing the probability of aggreing to a deal
        int: p in [0,1]
        """
        self.p = p
        
    
        
        
    