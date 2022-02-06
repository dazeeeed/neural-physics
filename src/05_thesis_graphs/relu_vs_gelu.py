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
from scipy.special import erf


def main():
    current_path = os.path.dirname(os.path.realpath("__file__"))
    data_path = os.path.abspath(os.path.join(current_path, '..', '..', 'data'))

    fig, ax = plt.subplots()
    fig.set_size_inches(4, 3, forward=True)

    colors = ['#3C3C4C', '#965F77', '#B4A0AA', '#D8C2CB', '#FED542', '#FED5C4']

    x = np.linspace(-3, 3, 100)

    def relu(x):
        return [max(0, i) for i in x]

    def gelu(x):
        return x * 0.5 * (1+erf(x/np.sqrt(2)))

    ax.plot(x, relu(x),  label="ReLU")
    ax.plot(x, gelu(x),  label="GELU")

    fig.tight_layout()
    ax.set_xticks(np.arange(-3, 4))
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend()
    ax.grid(True, ls=':')
    ax.tick_params(direction="in")

    name_of_plot = "relu_vs_gelu"
    for extension in [".png", ".svg"]:
        plt.savefig(os.path.join(data_path,
                                 'graphics',
                                 name_of_plot + extension), dpi=300)
    plt.show()


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
