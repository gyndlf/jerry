# d6615
# Solve Blackjack through brute force

import numpy as np
import gym

env = gym.make('Blackjack-v0', natural=True)  # natural meaning that hitting 21 gives 1.5 reward not 1

# Observation = (32 : Current sum,
            #   11: dealer's card,
            #   bool: ace or not
# Action = 2 : Hit or stand (1=hit, 0=stand)


Q = np.zeros((32, 11, 2, 2))  # ie 32*11*2 possibilities, 2 actions at each
print('Q table shape', Q.shape)
print('Q variables', 32*11*2*2)
print('*----*')

lr = 0.01  # learning rate
eps = 0.5  # random exploration
gma = 0.9  # gamma
epis = 10000000  # episodes
decay_rate = 0.9999  # decay rate
rev_list = []  # rewards per episode

# The algorithm
for i in range(epis):
    if i % 50000 == 0:
        print('Running test #', i)
    s = env.reset()  # s = location
    done = False
    rAll = 0
    eps *= decay_rate
    while not done:
        # choose an action
        #print('state of', s)
        total = s[0]  # Current sum
        dealer_card = s[1]  # dealer's card showing
        ace = s[2]  # ace or not
        #print('Q table of', Q[total, dealer_card, int(ace), :])
        if np.random.random() < eps or np.sum(Q[total, dealer_card, int(ace), :]) is 0:
            a = np.random.randint(0, 2)  # random choice
            #print('Random choice')
        else:
            #print('Decided')
            a = np.argmax(Q[total, dealer_card, int(ace), :])  # and some random noise
        # get new state and reward
        #print('ACtion of', a, '(0 for stand, 1 for hit)')
        new_s, reward, done, _ = env.step(a)
        Q[total, dealer_card, int(ace), a] = Q[total, dealer_card, int(ace), a] + \
                                             lr*(reward + gma*np.max(Q[new_s[0], new_s[1], int(new_s[2]), :]) -
                                                  Q[total, dealer_card, int(ace), a])
        #print('Updated q table', Q[total, dealer_card, int(ace), a])
        rAll += reward
        s = new_s
    rev_list.append(rAll)
    #print('Q table of', Q[s[0], s[1], int(s[2]), :])
    #print('*Game Over*  Result', reward, '\n')

print("Reward Sum on all episodes " + str(sum(rev_list)/epis))
print('Sum on last 10% of episodes', sum(rev_list[int(epis*0.9):])/epis)
print('Sum on last 1% of episodes', sum(rev_list[int(epis*0.99):])/epis)
print('Saving...')
#np.save('q-table.npy', Q)
print('Done.')