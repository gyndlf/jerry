# d7137
# Funtions to do with creatures
import logging
from Network import DNA

MUTATION_RATE = 0.02  # % of weights the get a small mutation (How common)
MUTATION_SIZE = 1  # How big the mutations are. (Standard deviation)

log = logging.getLogger(__name__)  # Inherits main config

def new_creatures(num=100):
    """Make 100 new creatures"""
    c = []
    for i in range(num):
        c.append(Creature())
    return c


def classify(c):
    """Classify the creature: What is its species?"""
    ...


class Creature:
    """An autonomous player of Connect 4 by its DNA"""
    def __init__(self, d=None):
        if d is not None:
            self.dna = d
        else:
            self.dna = DNA()  # Get some random DNA

    def breed(self, other, weigh=True):
        """Return a new creature with mixed DNA"""
        d = self.dna.merge(other.dna, weigh=weigh)  # Get the mixed DNA (Is weighted towards self)
        return Creature(d)

    def next_move(self, board, me):
        """Make its next move based on the board"""
        brd = board.state.copy()
        if me == 1:
            # I am player 1
            brd[brd == 2] = -1
            # brd[brd == 1] = 1 No need to change anything
        elif me == 2:
            # I am player 2
            brd[brd == 1] = -1
            brd[brd == 2] = 1
        else:
            raise Exception("Unknown player.")

        move = self.dna.forward(brd)
        return move

    def mutate(self):
        """Add some little mutations to the creature"""
        # Done by adding a normal distributed random matrix of small values onto the weights.
        # TODO: Make mutation rate dynamic (Slow down as generations increase)
        # TODO: Add mutations to network shape (maybe also activation functions)
        self.dna.noise(MUTATION_RATE, MUTATION_SIZE)