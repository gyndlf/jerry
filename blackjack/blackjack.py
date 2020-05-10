# d6623
# Class file for blackjack to run all the necessary algorithms

import numpy as np
import os

class Blackjack:
    def __init__(self):
        self.base = os.path.dirname(os.path.abspath(__file__))
        self.Q = np.load(os.path.join(self.base, 'q-table.npy'))

        print('qtable shape of', self.Q.shape)

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

    def draw_card(self, eyes, msg=''):
        # Use the eyes alg to "see" the card
        input(msg)
        return self.refine_card(int(eyes.read()))

    def gen_hand(self, eyes):
        hand = []
        hand.append(self.draw_card(eyes, msg='Whats my first card? : '))
        hand.append(self.draw_card(eyes, msg='And my second card? [int(1-10)] : '))
        hand.append(self.draw_card(eyes, msg='Whats the dealers card? [int(1-10] : '))
        return hand

    def run_round(self, eyes, cards):
        print('Press enter once the appropriate card has been inserted.')
        hand = cards[:2]
        dealer_card = cards[2]

        done = False
        while not done:
            action = np.argmax(self.Q[self.sum_hand(hand), dealer_card, int(self.usable_ace(hand)), :])
            # print('Stats of', total, dealer_card, ace)
            print('Converting q values of ', self.Q[self.sum_hand(hand), dealer_card, int(self.usable_ace(hand)), :])
            if action == 0:
                # Stand
                print('I choose to....\nSTAND.')
                done = True
            elif action == 1:
                # Hit me
                print('I choose to....\nHIT.')
                hand.append(self.draw_card(eyes, msg='Whats my next card? [int(1-10)] : '))
                if self.sum_hand(hand) > 21:
                    # Game over, I went bust
                    print('Oops I just lost')
                    done = True
        print('Sum of', self.sum_hand(hand))










