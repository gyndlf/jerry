# d7141
#
# Visualise the evolution with some cool plots

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json


def plot_composition(time_dict, stack=False):
    """Plot the species composition over time"""
    df = pd.DataFrame(time_dict)
    df.plot.area(stacked=stack)
    plt.legend(loc='upper left')
    plt.show()


if __name__ == '__main__':
    DATA_FILE = "data.json"

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    plot_composition(data["prop"])


