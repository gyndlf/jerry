# d7141
#
# Visualise the evolution with some cool plots

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import logging
log = logging.getLogger(__name__)  # Inherits main config


def plot_composition(time_dict, stack=False):
    """Plot the species composition over time"""
    df = pd.DataFrame(time_dict)
    df.plot.area(stacked=stack)
    plt.legend(loc='upper left')
    plt.show()


def plot_board(board, text=True):
    """Plot the board"""
    if text:
        print("+" + "_"*22 + "+")
        for r in board.state:
            l = "| "
            for c in r:
                if c == 0:
                    l += "   "
                else:
                    l += str(c)*2 + ' '
            print(l + "|")
        print("| 1- 2- 3- 4- 5- 6- 7- |")
    else:
        log.error("Plot function of graph is not implemented yet.")


def plot_net(dna):
    """Plot the DNA network associated"""
    # Parallel coordinates? Hardwire?
    ...


if __name__ == '__main__':
    from Network import DNA
    from Board import Board

    DATA_FILE = "data.json"

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    plot_composition(data["prop"])
    d = DNA()
    plot_board(Board())



