# d6617
# The hearts environment, has all the functions and plays the game

# need to be able to call
# env.reset()
# env.step()

# This is the same irrespective of how the agent is built

# observation = (card's played, highest card played, ace?, one?, two?, three?..., queen(12)?, king(13)?)

import numpy as np

def deal_hands(players=4):
    # Deal the cards
    cards = np.arange(1, 53)  # All cards dealt
    np.random.shuffle(cards)
    length = int(52//players)

    hands = np.zeros((players, 4, 14))

    for player in range(players):
        hand = cards[player*length:player*length+length]  # get "your" cards
        for card in hand:
            if card < 14:
                # Heart
                hands[player, 0, card] = 1
            elif card < 27:
                # Clubs
                hands[player, 1, card-13] = 1
            elif card < 40:
                # Spades
                hands[player, 2, card-13-13] = 1
            else:
                # Diamond
                hands[player, 3, card-13-13-13] = 1
        print('Player', player, "'s hand", hands[player])
    return hands

def reduce_hand(hand, suit):
    # Reduce hand to only that suit
    reduced = hand[suit]


class Game():
    def __init__(self, hand):
        print('Hearts engine initlised')

        # List of what cards the model holds
        self.hearts = []  # id of 0
        self.clubs = []  # id of 1
        self.spades = []  # id of 2
        self.diamonds = []  # id of 3

    def reset(self):
        # Reset the game. Need to pass back initinal observation
        pass

    def step(self, action):
        # Step in direction of action.
        # Return new observation, reward, done or not and debug controls
        pass

