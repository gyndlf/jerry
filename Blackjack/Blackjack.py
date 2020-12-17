# d6623
# Class file for Blackjack to run all the necessary algorithms

import numpy as np
import os
import logging

logger = logging.getLogger('jerry.Blackjack')


class Blackjack:
    def __init__(self, eyes):
        logger.info('Loading Blackjack')
        self.base = os.path.dirname(os.path.abspath(__file__))
        self.Q = np.load(os.path.join(self.base, 'q-table.npy'))

        self.eyes = eyes

        logger.debug('Using qtable at %a' % os.path.join(self.base, 'q-table.npy'))

    def usable_ace(self, hand):  # Can we play an ace?
        return 1 in hand and sum(hand) + 10 <= 21

    def sum_hand(self, hand):
        if self.usable_ace(hand):
            return sum(hand) + 10
        return sum(hand)

    def refine_card(self, card):
        # Make sure if it is above 10, it counts as a 10
        if card > 10:
            card = 10
        return card

    def draw_card(self, msg=''):
        # Use the eyes alg to "see" the card
        input(msg)
        return self.refine_card(int(self.eyes.read_value()))  # only want the value not the suit

    def gen_hand(self):
        hand = []
        hand.append(self.draw_card(msg='Whats my first card? : '))
        hand.append(self.draw_card(msg='And my second card? [int(1-10)] : '))
        hand.append(self.draw_card(msg='Whats the dealers card? [int(1-10] : '))
        return hand

    def run_round(self, cards):
        hand = cards[:2]
        dealer_card = cards[2]

        done = False
        while not done:
            action = np.argmax(self.Q[self.sum_hand(hand), dealer_card, int(self.usable_ace(hand)), :])
            # print('Stats of', total, dealer_card, ace)
            logger.debug('Converting q values of %a' % self.Q[self.sum_hand(hand), dealer_card, int(self.usable_ace(hand)), :])
            if action == 0:
                # Stand
                print('I choose to....\nSTAND.')
                done = True
            elif action == 1:
                # Hit me
                print('I choose to....\nHIT.')
                hand.append(self.draw_card(msg='Whats my next card? [int(1-10)] : '))
                if self.sum_hand(hand) > 21:
                    # Game over, I went bust
                    print('Oops, I just lost')
                    done = True
        logger.info('Sum of %a' % self.sum_hand(hand))










