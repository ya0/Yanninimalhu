# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 11:42:57 2020

@author: Nikos
"""
import numpy as np
import pygame as pg
import pylab
import itertools
import time
import networkx as nx
from matplotlib.pyplot import pause
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation

import matplotlib.pyplot as plt
import random
from PrisonersDilemma import PrisonersDilemma

pd = PrisonersDilemma(1.3, 1 ,0 , 0.1)


"""states: 0 empty, 1 allways defect, 0 allwaasy cooperate (subject to change)
i chose this numbering because to calculate a "deal" 0 stands for defecting and
1 for cooperating. so just subtracting 1 from the cell value gives the correct
optin"""

def get_neighbors(graph, i):
    """ returns a list of possible neighbors of node i
    """
    neighbors = [n for n in graph.neighbors(i)]
    
    return neighbors
    
    
    
def play_with_4neighbors(pd, graph, i, strategy):
    """ i plays the prisoners dilemma pd with neighbors in the grid
    return sum off all the games
    """
    payoff = 0    
    neighbors = get_neighbors(graph,i)
    
    for n in neighbors:
        payoff += pd.make_a_deal(strategy[i]-1, strategy[n]-1)[0]      
    
    return payoff
    


def imitate_single_individual(graph, pd,strategy):
    """ select one individual  and compute the sum over the PD with its 
    neighbors then compute the same for the neightbors and change to the 
    strategy of the best neighbor"""
    strategy
    # select random individual
    i = np.random.randint(0, N)
    # find a cell that actualy has a player...
    counter = 0
    while not i and counter < 30:
        i = np.random.randint(0, N)
        counter += 1
 
    payoff = play_with_4neighbors(pd, graph, i, strategy)
    
    # list of potential neighbors
    neighbors = get_neighbors(graph,i)
    # only consider neighbors that are actual players and not empty
    #neighbors = [n for n in neighbors if graph(n)]

    # no neighbors.. just return?
    if not neighbors:
        return
    
    # calculate the payoff of all the neighbors
    neighbors_payoff = []
    for n in neighbors:
        neighbors_payoff.append(play_with_4neighbors(pd, graph, n, strategy))
            
    # no good neighbors ? idk
    if not neighbors_payoff:
        return
    
    best_neighbor = max(neighbors_payoff)

    if best_neighbor > payoff:
        better_neighbor = neighbors[neighbors_payoff.index(best_neighbor)]
        strategy[i] = strategy[better_neighbor]
        

def init_cell_states(graph):
    """ the integer in the cell describes the strategy of that cell/actor. 
    0: empty cell
    1: defect
    2: cooperate
    
    for the future: i think it is possible to save objects into numpy arrays
    but we could also just reference different strategies by numbers. if we
    want to distinguish between actors we need ID's or save an actual object.
    """
    strategy=np.zeros(N)
    color_map = []
    for node in graph:
        r = np.random.random()
        if r>0.5:
            strategy[node]=1
            color_map.append('red')
        else:
            strategy[node]=2
            color_map.append('green')
    return strategy
                
"""
background_colour = (0, 0, 0)
width, height = 2 ** 10, 2 ** 10
cell_size = 2 ** 4
horizontal_cells, vertical_cells = width // cell_size, height // cell_size
grid = init_grid(horizontal_cells, vertical_cells, cell_type=int)
init_cell_states(grid)
"""
def imitation(graph,strategy,iterations):
    """
    main function that executes the whole simulation
    """

    for i in range(0,iterations):
        imitate_single_individual(graph, pd,  strategy)
        
    color_map = []
    for node in graph:
        if strategy[node]==1:
            color_map.append('red')
        elif strategy[node]==2:
            color_map.append('green')
        
    nx.draw(graph, node_color=color_map, with_labels=True, pos=pos)
    
def hubs(graph):
    "Calculates the number of hubs"
    degrees=np.zeros(N)
    for i in range(N):
        degrees[i]=graph.degree[i]    
        d_average=np.mean(degrees)

    hubs_array=np.argwhere(degrees > d_average*1.4)
    return hubs_array

def equilibrium(graph,strategy_past,strategy,n_eq):
    "Calculates when the global strategy simulation has gone into equilibrium"
    equil="False"
    v= strategy_past == strategy
    if v.all():
        n_eq+=1
    
    if n_eq>=3:
        equil="True"
    return n_eq, equil
    
    
def multiple(iterations,number_graphs,number_cases):
    """
    simulate multiple simulations and gives the ratio factor in the end
    """
    k_array=np.linspace(2,150,number_cases)
    coop_ratio_array=np.zeros(number_graphs) #calculates how many cooperators in the same diagram
    n_coop=np.zeros(number_cases) #calculates how many times for each case there are significant cooperators
    for z in range(0,number_cases):
        ka=int(k_array[z])
        coop_ratio_array=np.zeros(number_graphs)
        for i in range(0,number_graphs):
            graph = nx.watts_strogatz_graph(N, ka, p)
            tmp_G= graph.copy()
            init_cell_states(tmp_G)
            stra=strategy.copy()
            n_eq= 0
            while n_eq!=3:
                strategy_past=stra.copy()
                for j in range(0,iterations):
                    imitate_single_individual(tmp_G, pd,  stra)
                n_eq, equil = equilibrium(tmp_G,strategy_past,stra,n_eq) #calculates how many times the strategy has not changed
            coop_ratio_array[i]=(stra == 2).sum()
            if coop_ratio_array[i]>=10:
                n_coop[z]+=1
            print("number of cooperators per iter.= {}, \n same graph iterations= {}, \n n_coop[{}]= {},\n  average degree k={} \n " .format(coop_ratio_array, i, z, n_coop[z], k_array[z]))

    return n_coop

def plot_single(graph,strategy,iterations,tmp_G):
    try:
        n_eq=0
        init_cell_states(tmp_G)
        imitation(tmp_G,strategy,2)
        pylab.draw()
        pause(0.0001)
        pylab.clf()
        i=0
        while True:
            strategy_past=strategy.copy()
            imitation(tmp_G,strategy,iterations)
            n_eq, equil = equilibrium(graph,strategy_past,strategy,n_eq) #calculates how many times the strategy has not changed
            print(equil)
            pylab.draw()
            pause(0.0001)
            pylab.clf()
            if equil=="True":
                print(i)
            else:
                i+=1
    except KeyboardInterrupt:
        plt.close() 
    
        pass
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    #plt.show()        
            
    
    
N = 200 #number of nodes
k = 4 #mean degree 
p = 0.8 #probability of rewiring  
m = 8 #number of edges to attach from a new node to existing nodes     
iterations = 50 #number of iterations between every time step at the final plotting     
number_graphs = 10 #numbers to simulate each diagram case
number_cases =  10 #number of different graphs for multiple simulations
graph = nx.watts_strogatz_graph(N, k, p)
#graph= nx.barabasi_albert_graph(N,m)
pos = nx.spring_layout(graph)
tmp_G = graph.copy()

hubs_array=hubs(tmp_G)
strategy= init_cell_states(tmp_G)

print(hubs_array)


#n_coop=multiple(iterations,number_graphs,number_cases)
# #x = np.linspace(0,0.6,number_cases)
#x=np.linspace(2,150,number_cases)
#plt.plot(x, n_coop)

plot_single(graph,strategy,iterations,tmp_G)

plt.show()
