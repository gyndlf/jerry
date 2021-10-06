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
    def __init__(self):
        self.dna = DNA()

    def breed(self, other):
        """Return a new creature with mixed DNA"""
        ...

    def next_move(self, board):
        """Make its next move based on the board"""
        move = self.dna.forward(board.state)
        return move