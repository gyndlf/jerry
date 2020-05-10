# d6623
# Run the software play-game but on an actual system
import numpy as np
import os
Q = np.load('q-table.npy')

from cards.eyes import Eyes
eyes = Eyes()
print('qtable shape of', Q.shape)

def draw_card(msg=''):
    input(msg)
    return int(eyes.read())

def usable_ace(hand):  # Can we play an ace?
     return 1 in hand and sum(hand) + 10 <= 21

def sum_hand(hand):
    if usable_ace(hand):
        return sum(hand) + 10
    return sum(hand)


print('Press enter once the appropriate card has been inserted.')
while True:
    done = False
    hand = []
    hand.append(draw_card('Whats my first card? : '))
    hand.append(draw_card('And my second card? [int(1-10)] : '))
    dealer_card = draw_card('Whats the dealers card? [int(1-10] : ')

    while not done:
        action = np.argmax(Q[sum_hand(hand), dealer_card, int(usable_ace(hand)), :])
        #print('Stats of', total, dealer_card, ace)
        print('Converting q values of ', Q[sum_hand(hand), dealer_card, int(usable_ace(hand)), :])
        if action == 0:
            # Stand
            print('I choose to....\nSTAND.')
            done = True
        elif action == 1:
            # Hit me
            print('I choose to....\nHIT.')
            hand.append(draw_card('Whats my next card? [int(1-10)] : '))
            if sum_hand(hand) > 21:
                # Game over, I went bust
                print('Oops I just lost')
                done = True
    print('Sum of', sum_hand(hand))
    print()




