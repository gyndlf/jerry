# d7137

# Reinforcement learning to play connect 4

from Board import Board
from Creature import Creature, new_creatures
from Board import Game

# TODO:
#  - Create the individual "creatures" to play the game
#  - Build the environment for them to play in
#  - Make them compete
#  - Add visual element

NUM_CREATURES = 100
NUM_GENERATIONS = 10

"""
----- Conventions -----
Board:
 - Is a 6x7 numpy array. 
 - 1 if you have placed there, -1 if the opponent has, 0 if neither.
 - Found in Board.state
 
Creature
 - Has a network at Creature.DNA
 - Accepts a board an returns a normalised 7x1 vector of where it will place. 
 - Most likely valid choice is chosen.
 
Rounds
 - In each round all of the players are randomly grouped in 4s
 - They play a tournament game to rank 1,2,3,4
      - 4th place is eliminated
      - 1,2,3 chosen with a change of: 100% 1, 60% 2, 40% 3
      - (2 chosen per group to keep population constant).
 - Each group member chosen is paried with another group member to breed
 - Repeat for another round.
"""

C = new_creatures(NUM_CREATURES)
for generation in range(NUM_GENERATIONS):
    # Do the generation
    ...
