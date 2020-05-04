# d6610
# First start of a project to get card (hearts/ scum) playing robot
# Followed from https://adventuresinmachinelearning.com/reinforcement-learning-tutorial-python-keras/

import gym
import numpy as np

env = gym.make('NChain-v0')

# Pause the environment here to test it

# step(1) is a step to the left. Guarentteed 2 points
# However each step right (step(0)) about 4 gives 10 points.
# Sometimes the direction is randomally flipped losing progress
# Get the most points with 1,000 moves

# Naive policy - Choose the action giving the previous biggest reward
# Prediction: Wont ever reach 4
def naive_sum_reward_agent(env, num_episodes=500):
    # Table to hold our summated rewards for each action
    r_table = np.zeros((5,2))  # 5 states, 2 actions
    for g in range(num_episodes):
        s = env.reset()  # Get starting pos
        done = False
        while not done:  # Stops cause of the env
            if np.sum(r_table[s, :]) == 0:
                # Make a random selection as everything is 0
                a = np.random.randint(0,2)
            else:
                # Select the action with the highest reward
                a = np.argmax(r_table[s, :])
            new_s, r, done, debug = env.step(a)
            r_table[s, a] += r  # Add the reward in
            s = new_s
    return r_table


def q_delayed_gratification_reward_agent(env, num_episodes=500, gamma=0.95, lr=0.8):
    # Table to hold our summated rewards for each action
    q_table = np.zeros((5, 2))  # 5 states, 2 actions
    for g in range(num_episodes):
        s = env.reset()  # Get starting pos
        done = False
        while not done:  # Stops cause of the env
            if np.sum(q_table[s, :]) == 0:
                # Make a random selection as everything is 0
                a = np.random.randint(0, 2)
            else:
                # Select the action with the highest reward
                a = np.argmax(q_table[s, :])
            new_s, r, done, debug = env.step(a)
            q_table[s, a] += r + lr*(gamma*np.max(q_table[new_s, :]) - q_table[s, a])
            s = new_s
    return q_table

def eps_q_learn_agent(env, num_episodes=500, gamma=0.95, lr=0.8, eps=0.5, decay_factor=0.999):
    # Table to hold our summated rewards for each action
    q_table = np.zeros((5, 2))  # 5 states, 2 actions
    for g in range(num_episodes):
        s = env.reset()  # Get starting pos
        eps *= decay_factor
        done = False
        while not done:  # Stops cause of the env
            if np.random.random() < eps or np.sum(q_table[s, :]) is 0:
                # Make a random selection
                a = np.random.randint(0, 2)
            else:
                # Select the action with the highest reward
                a = np.argmax(q_table[s, :])
            new_s, r, done, debug = env.step(a)
            q_table[s, a] += r + lr*(gamma*np.max(q_table[new_s, :]) - q_table[s, a])
            s = new_s
    return q_table

#rewards = naive_sum_reward_agent(env)

#output = eps_q_learn_agent(env)
#print(output)

def run_game(table, env):
    s = env.reset()
    tot_reward = 0
    done = False
    while not done:
        a = np.argmax(table[s, :])
        s, r, done, _ = env.step(a)
        tot_reward += r
    return tot_reward

def test_methods(env, num_iterations=10):
    winner = np.zeros((3,))
    for g in range(num_iterations):
        m0_table = naive_sum_reward_agent(env, 500)
        m1_table = q_delayed_gratification_reward_agent(env, 500)
        m2_table = eps_q_learn_agent(env, 500)
        m0 = run_game(m0_table, env)
        m1 = run_game(m1_table, env)
        m2 = run_game(m2_table, env)
        w = np.argmax(np.array([m0, m1, m2]))
        winner[w] += 1
        print("Game {} of {}".format(g + 1, num_iterations))
    return winner

win = test_methods(env)
print(win)
