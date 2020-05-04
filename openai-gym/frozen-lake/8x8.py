# d6615
# https://towardsdatascience.com/reinforcement-learning-with-openai-d445c2c687d2
# Frozen lake walker ??

import gym
import numpy as np

# Load environment and make q structure
env = gym.make('FrozenLake8x8-v0')
Q = np.zeros([env.observation_space.n, env.action_space.n])  # (64, 4) ie 64 locations, 4 actions at each
print('Q table shape', Q.shape)

eta = .628  # random walk start
gma = .9  # decay rate
epis = 10000  # episodes
rev_list = []  # rewards per episode calculated

# The algorithm
for i in range(epis):
    s = env.reset()  # s = location
    done = False
    rAll = 0
    while not done:
        env.render()
        # choose an action
        a = np.argmax(Q[s,:] + np.random.randn(1, env.action_space.n)*(1./(i+1)))  # and some random noise
        # get new state and reward
        new_s, reward, done, _ = env.step(a)
        Q[s,a] = Q[s,a] + eta*(reward + gma*np.max(Q[new_s,:]) - Q[s,a])
        rAll += reward
        s = new_s
    rev_list.append(rAll)
    env.render()

print("Reward Sum on all episodes " + str(sum(rev_list)/epis))
print("Final Values Q-Table")
print(Q)

# Testing it out
s = env.reset()  # s = location
done = False
j = 0  # total steps to take?
while j < 199:
    env.render()
    j += 1
    # choose an action
    a = np.argmax(Q[s,:])  # and some random noise
    # get new state and reward
    new_s, reward, done, _ = env.step(a)
    s = new_s
    if done:
        print('Yay!')
        break
env.render()
