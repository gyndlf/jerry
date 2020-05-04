# d6615
# Solve blackjack through brute force

import numpy as np
import gym

env = gym.make('Blackjack-v0')

# Observation = (32 : Current sum,
            #   11: dealer's card,
            #   bool: ace or not
# Action = 2 : Hit or stand (1=hit, 0=stand)


Q = np.load('q-table.npy')
print('Q table shape', Q.shape)
print('Q variables', 32*11*2*2)
print('*----*')

epis = 100  # episodes
rev_list = []  # rewards per episode

# The algorithm
for i in range(epis):
    s = env.reset()  # s = location
    done = False
    rAll = 0
    while not done:
        # choose an action
        print('state of', s)
        total = s[0]  # Current sum
        dealer_card = s[1]  # dealer's card showing
        ace = s[2]  # ace or not
        print('Q table of', Q[total, dealer_card, int(ace), :])
        a = np.argmax(Q[total, dealer_card, int(ace), :])
        # get new state and reward
        print('ACtion of', a, '(0 for stand, 1 for hit)')
        new_s, reward, done, _ = env.step(a)
        rAll += reward
        s = new_s
    rev_list.append(rAll)
    print('*Game Over*  Result', reward, '\n')

print("Reward Sum on all episodes " + str(sum(rev_list)/epis))
print('Sum on last 10% of episodes', sum(rev_list[int(epis*0.9):])/epis)
print('Sum on last 1% of episodes', sum(rev_list[int(epis*0.99):])/epis)
