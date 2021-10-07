# d7137
# Funtions to do with creatures

from Network import DNA


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

    def next_move(self, board):
        """Make its next move based on the board"""
        # TODO: Change the board so that 1 is always you, -1 is always opponent
        move = self.dna.forward(board.state)
        return move

    def mutate(self):
        """Add some little mutations to the creature"""
        # TODO: Add mutations. Both of random data and network shape (maybe also activation functions)
        ...