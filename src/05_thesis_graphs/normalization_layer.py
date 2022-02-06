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

    current_path = os.path.dirname(os.path.realpath("__file__"))
    data_path = os.path.abspath(os.path.join(current_path, '..', '..', 'data'))

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
    fig.set_size_inches(7, 2, forward=True)

    colors = ['#3C3C4C', '#965F77', '#B4A0AA', '#D8C2CB', '#FED542', '#FED5C4']
    before = [188.447, 507.877, 505.236, 391.189, 507.877, 347.487, 505.236, 391.189, 549.372,
            347.487, 391.189, 535.588, 507.877, 507.877, 535.588, 507.877, 347.487, 507.877,
            549.372, 505.236, 188.447, 549.372, 488.564, 507.877, 188.447, 188.447, 347.487,
            391.189, 488.564, 549.372, 505.236, 347.487]
    after = [-2.089,  0.704,  0.694, -0.302,  0.706, -0.699,  0.683, -0.305,  1.085, -0.683,
             -0.312,  0.957,  0.728,  0.719,  0.964,  0.721, -0.71 ,  0.697,  1.081,  0.689,
             -2.085,  1.086,  0.538,  0.712, -2.052, -2.07 , -0.679, -0.296,  0.545,  1.076,
              0.686, -0.675]

    ax1.hist(before, density=True)
    ax2.hist(after, density=True)



    fig.tight_layout()

    # name_of_plot = "normalization"
    # for extension in [".png", ".svg"]:
    #     plt.savefig(os.path.join(data_path,
    #                              'graphics',
    #                              name_of_plot + extension), dpi=300)

    plt.show()


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
