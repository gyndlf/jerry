# d7137

# The real brains of the creatures; use per generation per round per game per move

import tensorflow as tf
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # ignore warnings.

"""
STRUCTURE
- Allow dynamic structure of creatures (ie chance of them mutating to get another layer)
- But MUST have a normal input of 6x7 and output of softmax 7x1.
"""


def new_wb(dims):
    """Make some new weights and biases"""
    w = []
    b = []
    for layer in range(1, len(dims)):
        w.append(tf.random.uniform((dims[layer], dims[layer-1]), minval=0, maxval=1))
        b.append(tf.random.uniform((dims[layer], 1), minval=0, maxval=1))
    return w, b


class DNA:
    """The DNA of a creature"""
    def __init__(self):
        self.dims = [42, 10, 12, 7]  # Dimensions of layers. Layer 0 is input, layer -1 is output.
        self.weights, self.biases = new_wb(self.dims)

    def forward(self, state):
        a = state.reshape((42,1))
        for l in range(len(self.weights)):  # l is hidden weight layer (or final layer)
            z = tf.math.add(tf.matmul(self.weights[l], a), self.biases[l])
            a = tf.nn.relu(z)  # TODO: Allow customisation of this function
        yh = tf.nn.softmax(a, axis=0)
        return tf.argmax(yh).numpy()


if __name__ == '__main__':
    d = DNA()
    print(d.forward(np.ones((6,7))))

    X = np.zeros((6,7))
    print("Input:\n", X)

    # Reshape to 42
    X = X.reshape((42,1))

    dims = [42, 10, 12]
    weights = [] # w1, w2, ...
    biases = [] # b1, b2, ...

    w1 = tf.random.uniform((dims[1], dims[0]), minval=0, maxval=1)
    b1 = tf.random.uniform((dims[1],1), minval=0, maxval=1)
    #z1 = w1.dot(X) + b1

    z1 = tf.math.add(tf.matmul(w1, X), b1)
    a1 = tf.nn.relu(z1)  # could use nn.relu, nn.leaky_relu (But not default towards this)

    yh = tf.nn.softmax(a1, axis=0)

    pred = tf.argmax(yh)  # Index of column to output

