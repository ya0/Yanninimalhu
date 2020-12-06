# Strategy Evolution Code

## Overview
This code was developed to simulate the evolution of cooperative and defecting behaviour in large populations. In the model, members of the population (players) interact with others around them by playing games, and the payoff each player receives depends on the strategy they employ. Players may adjust their strategy over time to maximize their payoff in the long run. We considered two behavioural policies, as outlined in detail in this Helbing paper <link>:
* Imitation: players imitate players in their vicinity with the highest payoff
* Migration: players move to regions in which their strategy would see them achieve the highest payoff.
We are interested to see whether these individual behavioural policies can lead to macroscopic effects, in particular the emergence of cooperative behaviour.

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
All simulations can be run from the file `simulate.py` by editing the parameters in the `if __name__ == "__main__"` section and running the script `simulate.py`.
Many parameters are self-explanatory, and as much as possible I've uesd the terms defined in the Helbing paper.
In essence you need to define a game, a board and a list of players. (Existing game types, board types and player types are defined in Game.py and Board.py, but feel free add other interesting ones you have in mind (see below)).
These are used to create a world, which will automatically distribute the players randomly across the board, and which will be able to evolve by performing a round of updates. A _round_ is a sequence in which every player plays a game with his/her neighbors and updates his/her strategy and/or position exactly once (in a random order). The simulation works by instructing the world to repeatedly perform these rounds.

## Extending the Model
I've done my best to write the code to be extendable to different games, players, and boards. To add your own, simply create a new class which inherits from the appropriate base class.
* A new player class should inherit from the class `Player`, to guarantee that it keeps track of the strategy, position (cell), and payoff of the player.
* A new Game class should inherit from the abstract class `Game`, with the simple requirement that it implement the `play` method defining the payoffs resulting from the interaction of two players.
* A new Board class should inherit from the abstract class `Board`. This requires that it implement several functions essential to the operation of the imitation and migration behavioural policies studied here.
