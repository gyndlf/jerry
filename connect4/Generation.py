# d7137

# Reinforcement learning to play connect 4
import logging
log = logging.getLogger(__name__)

from Board import Board
from Creature import Creature, new_creatures
from Board import Game
import random
from collections import defaultdict
import json
import Database

# TODO:
#  - Add visual element
#  - Change network to convolution to detect patterns

SAVE_EVERY_GEN = 10  # Save every 10 generations

DATA_FILE = "data.json"

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


def run_group(creatures, id):
    """Run the tournament of each group (return new breed of 1-> 4)"""
    # Run first games
    w1 = Game(creatures[id], creatures[id + 1]).run()
    w2 = Game(creatures[id + 2], creatures[id + 3]).run()

    if w1 is not None and w2 is not None:
        # Run playoffs for 1st and 3rd
        first = Game(creatures[id + w1 - 1], creatures[id + w2 + 1]).run()  # -1 to offset winner being 1,2 but array 0,1
        if first is not None:
            ids = [id + w1 - 1, id + w2 + 1]

            winner = creatures[ids[first - 1]]
            second = creatures[ids[::-1][first - 1]]  # Reverse the order to get the other

            new1 = winner.breed(second)
            new2 = winner.breed(second)
            return [winner, second, new1, new2]
        else:
            # Tie in finale
            new1 = creatures[id + w1 - 1].breed(creatures[id + w2 + 1], weigh=False)
            new2 = creatures[id + w2 + 1].breed(creatures[id + w1 - 1], weigh=False)
            return [creatures[id + w1 - 1], creatures[id + w2 + 1], new1, new2]
    elif w1 is None and w2 is None:
        # Two ties. Just pass them on
        return [creatures[id], creatures[id + 1], creatures[id + 2], creatures[id + 3]]
    elif w1 is None:
        # First game was tie
        new = creatures[id + w2 + 1].breed(creatures[id])  # Choose the first (Both should have similar genetics)
        return [creatures[id], creatures[id + 1], creatures[id + w2 + 1], new]
    elif w2 is None:
        # Second game was tie; Opposite to above
        new = creatures[id + w1 - 1].breed(creatures[id + 2])  # Choose the first (Both should have similar genetics)
        return [creatures[id + 2], creatures[id + 3], creatures[id + w1 - 1], new]
    else:
        # I have no idea. Should never get here
        raise Exception("Umm... How did you get here")


def run_generations(C, gens, genstart=0):
    """Run 'gens' generations for creatures C"""
    num = len(C)
    assert num % 4 == 0
    num_groups = num // 4

    data = {"prop": []}  # Time series cool stuff

    for generation in range(genstart+1, gens+1):
        winners = []  # Leave as are
        born = []  # Likewise leave as are
        mutate = []  # Mutate
        log.info(f"Generation {generation}")
        # Do the generation
        for grp in range(num_groups):  # Creature indexes of g, g+1, g+2 and g+3
            log.debug(f"Group {grp}")
            winner, second, born1, born2 = run_group(C, grp)
            winners.append(winner)
            mutate.append(second)
            born.extend([born1, born2])

        for c in mutate:
            c.mutate()  # Mutate all the creatures

        species = defaultdict(int)  # Dict of generation species makeup
        for creat in winners + born + mutate:
            species[creat.species] += 1

        p = {k: v / num for k, v in species.items()}
        data["prop"].append(p)
        log.info(p)
        # Move the generation on
        C = winners + born + mutate
        random.shuffle(C)

        if generation % SAVE_EVERY_GEN == 0:
            # Save the stuff.
            Database.save_creatures(C, generation)

    # Save the data
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
