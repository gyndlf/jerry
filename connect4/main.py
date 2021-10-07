# d7137

# Reinforcement learning to play connect 4

from Board import Board
from Creature import Creature, new_creatures
from Board import Game
import random

# TODO:
#  - Add visual element
#  - Add printing to log file
#  - Add proper debug

NUM_CREATURES = 100       # Multiple of 4
NUM_GENERATIONS = 100

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

assert NUM_CREATURES % 4 == 0
num_groups = NUM_CREATURES // 4
C = new_creatures(NUM_CREATURES)

C_new = []  # The next generation

for generation in range(NUM_GENERATIONS):
    print("Generation", generation)
    # Do the generation
    for g in range(num_groups):  # Creature indexes of g, g+1, g+2 and g+3
        print("Group", g)
        # Run first games
        w1 = Game(C[g], C[g+1]).run()
        w2 = Game(C[g+2], C[g+3]).run()

        # Run playoffs for 1st and 3rd
        first = Game(C[g+w1-1], C[g+w2+1]).run()  # -1 to offset winner being 1,2 but array 0,1
        ids = [g+w1-1, g+w2+1]

        winner = C[ids[first-1]]
        second = C[ids[::-1][first-1]]  # Reverse the order to get the other

        new1 = winner.breed(second)
        new2 = winner.breed(second)

        C_new.extend([winner, second, new1, new2])

    # Move the generation on
    random.shuffle(C_new)
    C = C_new

