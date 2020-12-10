# Strategy Evolution Code

## Overview
This code was developed to simulate the evolution of cooperative and defecting behaviour in large populations. The project is mainly based on the ideas in the paper [Outbreak of Cooperation](https://arxiv.org/abs/0903.4054) by Helbing and Yu. In the model, members of the population (players) interact with others around them by playing games, and the payoff each player receives depends on the strategy they employ. Players may adjust their strategy over time to maximize their payoff in the long run. We considered two behavioral policies, as outlined in detail in the Helbing paper:
* Imitation: players imitate players in their vicinity with the highest payoff
* Migration: players move to regions in which their strategy would see them achieve the highest payoff.
We are interested to see whether these individual behavioral policies can lead to macroscopic effects, in particular the emergence of cooperative behavior.

## Model
We model the above setting through four objects:
* game
* player
* board
* world

A **game** is a set of rules which defines the interaction between players; it determines the payoff each player receives as a function of the strategies played by all of the players. In the code this is modelled by the Game class.

A **player** is an individual engaging in a game. A player engages in the game with a certain strategy to try to maximize his/her payoff. In the code this is modelled by the Player class.

A **board** is the topology of the world in which the game takes place. It is made up of _cells_, discrete regions which a player can occupy, and which define a player's position. The board also determines the _"play neighborhood"_ of a player, the set of other players with which a player can engage in a game, and the _"migration neighborhood"_, the set of other cells to which a player can migrate in search of a better payoff. In the code this is modelled by the Board class.

A **world** consists of a game, a set of players, and a board, and can be thought of as a "world" in which the simulation takes place. The world governs the behavioral policies of players in response to the outcomes of their game interactions, and evolves accordingly. In this code this is modelled by the World class.

## Installation
First download the code ([master](https://github.com/ya0/Yanninimalhu/archive/master.zip)). Then install the requirements with

```bash
pip install requirements.txt
```
for simulations on a 2D grid. Or

```bash
pip install requirements_network.txt
```
for simulations on a Node Network.

## Running Simulations
Simulations can be carried out as in `simulate.py`. The simulation repeatedly updates the world in a series of rounds. A _round_ is a sequence in which every player plays a game with his/her neighbors and updates his/her strategy and/or position exactly once (in a random order). After each round, the program can optionally display the game board and record statistics.

### World creation
To create a world in which you can run simulations, you must provide a game, players, and the board. (Game types, player types and board types are defined in the files `Game.py` and `Board.py` - for more information see below.) The world will automatically distribute the players randomly across the board.

An example is shown below.

```python
"""
first create a Prisoners Dilemma with parameters
    T: temptacion
    R: reward
    P: punishment
    S: sucker's payoff
"""
game = PrisonersDilemma(T, R, P, S)
""" initiate a grid"""
board = RectangularGrid(grid_height, grid_width)

""" setup players based on the dimension of the grid and
set the to cooperate or defect

 p_cooperation: percentage of cooperating players
"""
num_players = grid_height * grid_width // 2
p_cooperation = 0.5

players = []
for i in range(num_players):
    rand = random.random()
    if rand < p_cooperation:
        players.append(PrisonersDilemmaPlayer(Strategy.cooperate))
    else:
        players.append(PrisonersDilemmaPlayer(Strategy.defect))
"""
Finaly create a world object
    - game: game played between two players during an interaction
    - board: topology of the world
    - players: a list of players in the world

optional arguments:
    - r: probability that a player randomly resets its strategy
    - q: conditional probability that a player resets to cooperate
    - noise1: a boolean indicating whether Noise 1 is present
    - noise2: a boolean indicating whether Noise 2 is present
    - imitation: a boolean indicating whether players perform imitation
    - migration: a boolean indicating whether players perform migration
    - M: the range of the Moore neighborhood around each cell
"""
world = World(game, board, players)
```

### Editing parameters
The file `simulate.py` runs the simulations described in the Helbing paper. The simulation type can be changed by editing the parameters in the `if __name__ == "__main__"` section of the file (e.g. turning on and off noise, adjusting player behavioral policies). The parameter name correspond to those used in the paper.

### Analyzing the simulation with statistics
The simulation also supports recording statistics about the world with an optional SimulationStatistics object. (Simulation statistics types are defined in the files `SimulationStatistics.py` - for more information see below.)

## Extending the Model
The code is designed to be extendable to different games, players, boards, and statistics. To add your own, simply create a new class which inherits from the appropriate base class.
* A new player class should inherit from the class `Player`, to guarantee that it keeps track of the strategy, position (cell), and payoff of the player.
* A new Game class should inherit from the abstract class `Game`, with the simple requirement that it implement the `play` method defining the payoffs resulting from the interaction of two players.
* A new Board class should inherit from the abstract class `Board`. This requires that it implement several functions essential to the operation of the imitation and migration behavioral policies studied here.
* A new SimulationStatistics class should inherit from the abstract class `SimulationStatistics`. This requires that it implement methods to record statistics and print the results, and optionally to determine the end of the simulation based on its own statistical results.
