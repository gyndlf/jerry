# d6623
# Run the software play-game but on an actual system

# d6615
# Now that the q-table has been calculated, games can be simulated. Here this occurs

import numpy as np
Q = np.load('q-table.npy')

# Need to populate these three variables to make a decision

print('JackAttak 3000.')
print('Cards are from 1-10 (Pictures = 10, ace=1)')
print('Ace can be used as 11 or 1, but please enter as just 1')
print('This code assumes you have a human dealer too')

print('qtable shape of', Q.shape)

def draw_card(msg='Whats my card? [int(1-10)] : '):
    new_card = int(input(msg))
    return new_card

def usable_ace(hand):  # Can we play an ace?
     return 1 in hand and sum(hand) + 10 <= 21

def sum_hand(hand):
    if usable_ace(hand):
        return sum(hand) + 10
    return sum(hand)

while True:
    done = False
    hand = []
    hand.append(draw_card('Whats my first card? [int(1-10] : '))
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




