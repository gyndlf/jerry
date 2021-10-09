# d7137
# Funtions to do with creatures
import logging
import numpy as np
from Network import DNA

MUTATION_RATE = 0.02  # % of weights the get a small mutation (How common)
MUTATION_SIZE = 1  # How big the mutations are. (Standard deviation)

LAYER_PROBA = 0.001  # Chance for a new layer to be added
NODE_PROBA = 0.01  # Chance for a node to be added (or removed)


log = logging.getLogger(__name__)  # Inherits main config


def new_creatures(num=100):
    """Make 100 new creatures"""
    cs = []
    for i in range(num):
        cs.append(Creature())
    return cs


def classify(c):
    """Classify the creature: What is its species?"""
    # Done by comparing the hidden layers in DNA
    hidden = c.dna.dims[1:-2]  # Make the last one a number for coolness sake
    name = ""
    for s in hidden:
        name += chr((s % 26)+65)
    return name + str(c.dna.dims[-2])


class Creature:
    """An autonomous player of Connect 4 by its DNA"""
    def __init__(self, d=None):
        if d is not None:
            self.dna = d
        else:
            self.dna = DNA()  # Get some random DNA

    @property
    def species(self):
        """Attribute of class of self"""
        return classify(self)

    def breed(self, other, weigh=True):
        """Return a new creature with mixed DNA"""
        if self.species == other.species:
            # logging.warning(f"{self.species}+{other.species}")
            d = self.dna.merge(other.dna, weigh=weigh)  # Get the mixed DNA (Is weighted towards self)
            return Creature(d)
        else:
            return self.copy()  # TODO: Return new mutated creature if unable to breed

    def copy(self):
        """Return a new copy of the creature: Unlinked"""
        return Creature(self.dna.copy())

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

        if np.random.rand() < NODE_PROBA:
            # Add or remove a new node from the network
            old = self.species
            self.dna.change_node()
            log.info(f"New species! ({old}->{self.species})")


if __name__ == '__main__':
    c = Creature()
    print(classify(c))