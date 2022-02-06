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
import seaborn as sns


def main():
    current_path = os.path.dirname(os.path.realpath("__file__"))
    data_path = os.path.abspath(os.path.join(current_path, '..', '..', 'data'))

    training_filename = 'TRAINING_DATA_RHO.csv'
    training_data_path = os.path.abspath(
        os.path.join(current_path, '..', '..', 'data', training_filename))
    csv_data = pd.read_csv(training_data_path)

    csv_dataset = csv_data.copy()
    csv_data.head()

    train_dataset = csv_dataset.sample(frac=0.8, random_state=0)
    test_dataset = csv_dataset.drop(train_dataset.index)
    # train_dataset.describe().transpose()
    train_dataset.describe().iloc[:, [0, 31, 32, 33, 102, 103, 104, 105, 106]].transpose()
    #%%

    # sns.pairplot(csv_dataset[['keff_start', 'keff_max', 'ppf_start', 'cycle_length_in_days']], diag_kind='kde')
    plot = sns.pairplot(train_dataset[['rho_start', 'rho_max', 'rho69', 'cycle_length_in_days']], diag_kind='kde')
    fig = plot.fig
    fig.savefig("pairplot.png")

    for extension in [".png", ".svg"]:
        plt.savefig(os.path.join(data_path,
                                 'graphics',
                                 "data_pairplot" + extension), dpi=300)

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))