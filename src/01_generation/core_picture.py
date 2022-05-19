import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def read_core_config(datapath, filename):
    return pd.read_csv(datapath + '/' + filename, header=None, sep=',').to_numpy()


def main():
    current_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.abspath(os.path.join(current_path, '..', '..', 'data'))
    core_configs = read_core_config(data_path, "core_configurations.csv")

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
    a = core_configs[:17, :]
    b = core_configs[17:34, :]

    ax1.imshow(a, cmap='gnuplot', interpolation='nearest', vmin=0, vmax=10)
    ax2.imshow(b, cmap='gnuplot', interpolation='nearest', vmin=0, vmax=10)
    for (j, i), label in np.ndenumerate(a):
        ax1.text(i, j, label, ha='center', va='center')
        ax2.text(i, j, label, ha='center', va='center')

    ax1.set_xticks(np.arange(0, 17, 2))
    ax1.set_yticks(np.arange(0, 17, 2))
    ax2.set_xticks(np.arange(0, 17, 2))
    ax2.set_yticks(np.arange(0, 17, 2))
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()