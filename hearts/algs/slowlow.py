# d6619
# Start playing really high cards, but as the game progresses become more conservative, then playing
# the highest card that it can play, under the top card currently played

import numpy as np
import logging

logger = logging.getLogger('jerry.algs.slowlow')

class SlowLow():
    def __init__(self, players):
        self.info = 'Algorithm that takes a hand and chooses the highest card under the highest card played'
        self.players = players  # Num of players
        self.num_full_hand = int(52//players)  # sum of a full hand
        self.threshold = 1.0
        self.final_threshold = 0.01  # the wanted result for the threshold after the game
        self.diminisher = np.exp(np.log(self.final_threshold)/self.num_full_hand)  # self.threshold *= self.diminisher each round
        logger.debug('Estimating that %a is a full hand.' % self.num_full_hand)
        logger.debug('Setting diminishing constant to be %a%%.' % self.diminisher)

    def think(self, mode, observation):
        # Takes inputs, returns action
        assert mode == 'limited'

        suit, card = np.where(observation[0,:,:]==1)
        suit = int(suit)
        highest_played_card = int(card)

        logger.debug('Threshold is %a%%' % self.threshold)

        lowest = np.argmax(observation[1, suit])  # Find lowest card
        highest = 0
        sel = 0
        for i, card in enumerate(observation[1, suit]):
            if card == 1 and i > sel and i < highest_played_card:
                # Find the highest card under
                sel = i
            if card == 1 and i > highest:
                # Find the biggest card that you can play
                highest = i

        logger.info('Highest card: %a lowest card: %a highlow card: %a' % (highest,lowest,sel))

        if highest > 0 and np.random.random() < self.threshold:
            choice = (suit, highest)

        elif sel == 0 and lowest == 0:
            choice = self.choose_sub_card(observation[1])
            # There is none of that suit
            # Then choose worst card
        elif sel == 0:
            # Then only a lower card is not possible
            choice = (suit, lowest)
        else:
            choice = (suit, sel)
        logger.info('Choosing lowest card of' + str(choice))
        self.threshold *= self.diminisher
        return choice

    def choose_first_card(self, cards):
        # What card should you play first?
        logger.info('Cards:\n' + str(cards))
        card = 0
        for i in range(14):
            if np.sum(cards[:, i]) > 0:
                # There is a card
                logger.info('(Best card) Choose' + str((np.argmax(cards[:, i]), i)))
                return np.argmax(cards[:, i]), i
        logger.error('Indexing error')
        raise IndexError('Ummmmm')

    def choose_sub_card(self, cards):
        # What card do you throw away? (Worst card?)
        card = 0
        for i in range(13,-1,-1):  # just go backwards
            # print(i, '==>', np.argmax(cards[:, i]))
            if np.sum(cards[:, i]) > 0:
                # There is a card
                logger.info('(Worst card) Choose' + str((np.argmax(cards[:, i]), i)))
                return np.argmax(cards[:, i]), i
        logger.error('Indexing error')
        raise IndexError('Uhhhhh')
