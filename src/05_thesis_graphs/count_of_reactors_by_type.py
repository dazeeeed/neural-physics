import matplotlib
from matplotlib.font_manager import FontProperties

font = {'family': 'Arial',
        'weight': 'medium',
        'size': 15,
        'style': 'normal'}

matplotlib.rcParams['mathtext.fontset'] = 'custom'
matplotlib.rcParams['mathtext.rm'] = 'Arial'
matplotlib.rcParams['mathtext.it'] = 'Arial'

matplotlib.rc('font', **font)
matplotlib.rc('text', usetex=False)

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import time


def main():
    def absolute_value(val):
        a = np.round(val / 100. * counts.sum(), 0)
        return int(a)

    current_path = os.path.dirname(os.path.realpath("__file__"))
    data_path = os.path.abspath(os.path.join(current_path, '..', '..', 'data'))

    fig, ax = plt.subplots()
    fig.set_size_inches(7, 5, forward=True)

    group_names = ["PWR", "BWR", "PHWR", "LWGR", "GCR", "FBR"]

    counts = pd.Series([305, 62, 48, 12, 11, 3], index=group_names)
    # counts = pd.Series([290.5, 63.1, 24.5, 8.6, 6.1, 1.4], index=group_names)

    explode = (0, 0.02, 0.1, 0.15, 0.3, 0.5)
    colors = ['#3C3C4C', '#965F77', '#B4A0AA', '#D8C2CB', '#FED542', '#FED5C4']

    plt.pie(counts, colors=colors, explode=explode, labels=group_names, autopct=absolute_value)
    plt.axis('equal')
    plt.ylabel('')
    plt.legend(labels=counts.index, loc="best")

    fig.tight_layout()

    name_of_plot = "reactor_count_by_type"
    # name_of_plot = "reactor_electrical_capacity_by_type"
    for extension in [".png", ".svg"]:
        plt.savefig(os.path.join(data_path,
                                 'graphics',
                                 name_of_plot + extension), dpi=300)

    plt.show()


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
