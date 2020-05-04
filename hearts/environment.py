# d6617
# The hearts environment, has all the functions and plays the game

# need to be able to call
# env.reset()
# env.step()

# This is the same irrespective of how the agent is built

# observation = (card's played, highest card played, my cards)

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
        print('Player', player, "'s hand\n", hands[player])
    return hands


def reduce_hand(hand, suit):
    # Reduce hand to only that suit
    return hand[suit]


class Simulator():
    def __init__(self, players):
        print('Hearts engine initlised')

        self.hands = deal_hands(players)  # all cards
        self.current_hands = self.hands  # only cards left
        self.players = players

        # List of what cards the model holds
        self.hearts = 0
        self.clubs = 1
        self.spades = 2
        self.diamonds = 3

    def load_algorithms(self, algorithms):
        assert algorithms.__len__() == self.players  # Make sure right number is entered
        self.algs = algorithms  # These will be the models

    def reset(self):
        # Reset the game. Need to pass back initinal observation
        pass

    def init_state(self, player):
        # Can choose any card... but choosing a suit is harder.
        suit, card = self.algs[player].choose_first_card(self.current_hands[player])
        return suit, card

    def gen_state(self, played, turn, suit):
        # Played is cards played, turn is player's turn
        num_cards = len(played)
        highest_card = max(played)
        cards = self.current_hands[turn, suit]
        return (num_cards, highest_card, cards)

    def step(self, action):
        # Step in direction of action.
        # Return new observation, reward, done or not and debug controls
        pass

