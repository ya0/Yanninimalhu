# Strategy Evolution Code

## Overview
This code was developed to simulate the evolution of cooperative and defecting behaviour in large populations. The project is mainly based on the Ideas in the paper [Outbreak of Cooperation](https://arxiv.org/abs/0903.4054) by Helbing and Yu.  In the model, members of the population (players) interact with others around them by playing games, and the payoff each player receives depends on the strategy they employ. Players may adjust their strategy over time to maximize their payoff in the long run. We considered two behavioural policies, as outlined in detail in this Helbing paper <link>:
* Imitation: players imitate players in their vicinity with the highest payoff
* Migration: players move to regions in which their strategy would see them achieve the highest payoff.
We are interested to see whether these individual behavioural policies can lead to macroscopic effects, in particular the emergence of cooperative behaviour.


## Installation
First download the code ([master](https://github.com/ya0/Yanninimalhu/archive/master.zip)). Then install the requirements with

```bash
pip intall -r requirements.txt
```
for simulations on a 2D grid. Or 

```bash
pip intall -r requirements_network.txt
```
for simulations on a Node Network.

## Example
To see a basic example of a simulation on a 2D grid you can run `simulation.py` on the console
```bash
python simulation.py
```
or use a IDE to run the file.
A window will open showing a grid with two types of agents. The blue ones always cooperate and the red ones defect. This is a scenario described in the paper mentioned above where these agents try to find the best place for themselves in a Moore neighborhood of distance 5 and imitate their best performing neighbors. Also, noise is activated. After the simulation has run for 30 seconds you will get a statistical overview of the percentage of cooperators and defectors.

## Model
We model the above setting through four objects:
* game
* player
* board
* world

A **game** is a set of rules which defines the interaction between players; it determines the payoff each player receives as a function of the strategies played by all of the players. In the code this is modelled by the Game class.

A **player** is an individual engaging in a game. A player engages in the game with a certain strategy to try to maximize his/her payoff. In the code this is modelled by the Player class.

A **board** is the topology of the world in which the game takes place. It is made up of _cells_, discrete regions which a player can occupy, and defining a player's position. The board also determines the _neighbourhood_ of a player - the set of other players with which a player can engage in a game. In the code this is modelled by the Board class.

A **world** consists of a game, a set of players, and a board, and can be thought of as a "world" in which the simulation takes place. The world governs the behavioural policies of players in response to the outcomes of their game interaction, and evolves accordingly. In this code this is modelled by the World class.

## Running Simulations
All simulations can be carried out by running the script `simulate.py`. The simulation repeatedly updates the world in a series of rounds. A _round_ is a sequence in which every player plays a game with his/her neighbors and updates his/her strategy and/or position exactly once (in a random order). After each round, the program can optionally display the game board and record statistics.

### World creation
To create a world in which you can run simulations, you must provide a game, players, and the board. (Game types, player types and board types are defined in the files `Game.py` and `Board.py` - for more information see below.) The world will automatically distribute the players randomly across the board.

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
The simulation type can be changed by editing the parameters in the `if __name__ == "__main__"` section of the file `simulate.py`. As much as possible I've used the same names for parameters as those which appear in the Helbing paper.

### Analyzing the simulation with statistics
The simulation also supports recording statistics about the world with an optional SimulationStatistics object. (Simulation statistics types are defined in the files `SimulationStatistics.py` - for more information see below.)

## Extending the Model
I've done my best to write the code to be extendable to different games, players, boards, and statistics. To add your own, simply create a new class which inherits from the appropriate base class.
* A new player class should inherit from the class `Player`, to guarantee that it keeps track of the strategy, position (cell), and payoff of the player.
* A new Game class should inherit from the abstract class `Game`, with the simple requirement that it implement the `play` method defining the payoffs resulting from the interaction of two players.
* A new Board class should inherit from the abstract class `Board`. This requires that it implement several functions essential to the operation of the imitation and migration behavioural policies studied here.
* A new SimulationStatistics class should inherit from the abstract class `SimulationStatistics`. This requires that it implement methods to record statistics and print the results, and optionally to determine the end of the simulation based on its own statistical results.
