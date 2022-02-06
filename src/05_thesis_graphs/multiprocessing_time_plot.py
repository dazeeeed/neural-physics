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
    fig.set_size_inches(7, 2, forward=True)


    colors = ['#3C3C4C', '#965F77', '#B4A0AA', '#D8C2CB', '#FED542', '#FED5C4']

    ax.barh([1, 2], [30.2, 6.38], height=0.7, color=colors[1])
    ax.set_yticks([1, 2])
    ax.invert_yaxis()
    ax.set_yticklabels(labels=("Sekwencyjnie", "Równolegle"))

    ax.set_xlabel("Czas [s]")



    fig.tight_layout()

    name_of_plot = "mean_parallel_vs_sequential_runtime"
    for extension in [".png", ".svg"]:
        plt.savefig(os.path.join(data_path,
                                 'graphics',
                                 name_of_plot + extension), dpi=300)

    plt.show()


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
