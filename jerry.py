# d6623
# This is the main controlling python file. Everything should be used only in class form

print('Jerry v1.0')
print('"I would never lose to a machine" - Felonius Gru')

from blackjack.blackjack import Blackjack
from cards.eyes import Eyes

blackjack = Blackjack()
eyes = Eyes()

while True:
    # Get the inputed cards
    cards = blackjack.gen_hand(eyes)
    blackjack.run_round(eyes, cards)
    print('')
