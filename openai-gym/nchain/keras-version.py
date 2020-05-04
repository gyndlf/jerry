# d6614
# same as environ, but a neural network. is it any better??
# Followed from https://adventuresinmachinelearning.com/reinforcement-learning-tutorial-python-keras/

import gym
import numpy as np
from keras.models import Sequential
from keras import layers

env = gym.make('NChain-v0')

model = Sequential()
model.add(layers.InputLayer(batch_input_shape=(1, 5)))  # difference between normal dense layer? must not have weights
model.add(layers.Dense(10, activation='sigmoid'))
model.add(layers.Dense(2, activation='linear'))
model.compile(loss='mse',  # mean squared error
              optimizer='adam',  # adam optimizer (something new) https://arxiv.org/abs/1412.6980
              metrics=['mae'])  # mean absolute error
model.summary()

# Now solve the q learning
num_episodes = 100
y = 0.95
eps = 0.5  # to allow random exploration
decay_factor = 0.999
r_avg_list = []

for i in range(num_episodes):
    s = env.reset()
    eps *= decay_factor
    if i % 5 is 0:  # factor of 100
        print("Episode {} of {}".format(i + 1, num_episodes))
    done = False
    r_sum = 0
    while not done:
        if np.random.random() < eps:  # Below the threshold, make a random choice
            a = np.random.randint(0, 2)
        else:
            a = np.argmax(model.predict(np.identity(5)[s:s+1]))  # identity to generate the onehot input
        new_s, r, done, _ = env.step(a)
        target = r + y * np.max(model.predict(np.identity(5)[new_s:new_s+1]))  # the next reward
        target_vec = model.predict(np.identity(5)[s:s+1])[0]
        target_vec[a] = target  # only q value corresponding is touched
        model.fit(np.identity(5)[s:s+1], target_vec.reshape(-1, 2),
                  epochs=1,
                  verbose=0)
        s = new_s
        r_sum += r

    r_avg_list.append(r_sum / 1000)



