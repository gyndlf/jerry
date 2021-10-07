# d7137

# Reinforcement learning to play connect 4
import logging
import logging.config
logging.config.fileConfig("logging.conf")
log = logging.getLogger(__name__)

from Board import Board
from Creature import Creature, new_creatures
from Board import Game
import random

# TODO:
#  - Add visual element

NUM_CREATURES = 100       # Multiple of 4
NUM_GENERATIONS = 50

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
      - 3rd and 4th place are eliminated
      - 1st and 2nd breed twice with weights of 66% 1, 33% 2
 - Repeat for another round.
"""

assert NUM_CREATURES % 4 == 0
num_groups = NUM_CREATURES // 4
C = new_creatures(NUM_CREATURES)

C_new = []  # The next generation

for generation in range(NUM_GENERATIONS):
    logging.info(f"Generation {generation}")
    # Do the generation
    for g in range(num_groups):  # Creature indexes of g, g+1, g+2 and g+3
        #print("Group", g)
        # Run first games
        w1 = Game(C[g], C[g+1]).run()
        w2 = Game(C[g+2], C[g+3]).run()

        if w1 is not None and w2 is not None:
            # Run playoffs for 1st and 3rd
            first = Game(C[g+w1-1], C[g+w2+1]).run()  # -1 to offset winner being 1,2 but array 0,1
            if first is not None:
                ids = [g+w1-1, g+w2+1]

                winner = C[ids[first-1]]
                second = C[ids[::-1][first-1]]  # Reverse the order to get the other

                new1 = winner.breed(second)
                new2 = winner.breed(second)
                C_new.extend([winner, second, new1, new2])
            else:
                # Tie in finale
                new1 = C[g+w1-1].breed(C[g+w2+1], weigh=False)
                new2 = C[g+w2+1].breed(C[g+w1-1], weigh=False)
                C_new.extend([C[g+w1-1], C[g+w2+1], new1, new2])
        elif w1 is None and w2 is None:
            # Two ties. Just pass them on
            C_new.extend([C[g], C[g+1], C[g+2], C[g+3]])
        elif w1 is None:
            # First game was tie
            new = C[g+w2+1].breed(C[g])  # Choose the first (Both should have similar genetics)
            C_new.extend([C[g], C[g+1], C[g+w2+1], new])
        elif w2 is None:
            # Second game was tie; Opposite to above
            new = C[g+w1-1].breed(C[g+2])  # Choose the first (Both should have similar genetics)
            C_new.extend([C[g+2], C[g+3], C[g+w1-1], new])
        else:
            # I have no idea. Should never get here
            raise Exception("Umm... How did you get here")

    # Move the generation on
    random.shuffle(C_new)
    C = C_new
    C_new = []

