# d7141
#
# Visualise the evolution with some cool plots

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import logging
log = logging.getLogger(__name__)  # Inherits main config
import Database


def plot_composition(stack=False, save=False):  # TODO: Change so that species that exist for 1 generation don't show
    """Plot the species composition over time"""
    data = Database.retrieve_compositions()
    df = pd.DataFrame(data)
    fig = plt.figure(figsize=(12,8))
    df.plot.area(stacked=stack)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15),
          ncol=4, fancybox=True, shadow=True)
    plt.xlabel("Generation (num)")
    plt.ylabel("Frequency (%)")
    if save:
        plt.savefig("plots/composition.png")
    else:
        plt.show()


def plot_times(save=False):
    """Plot how long the training is taking"""
    data = Database.retrieve_history()
    times = []
    for snap in data:
        times.append(snap[1])
    fig = plt.figure()
    plt.plot(times)
    plt.xlabel("Generation (num)")
    plt.ylabel("Time (sec)")
    plt.title("Training timing")
    if save:
        plt.savefig("plots/times.png")
    else:
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
    plot_composition(save=True)
    plot_times(save=True)




