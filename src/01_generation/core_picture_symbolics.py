import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def read_core_config(datapath, filename):
    return pd.read_csv(datapath+'/'+filename, header=None, sep=',').to_numpy()

def main():
    current_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.abspath(os.path.join(current_path, '..', '..', 'data'))
    core_configs = read_core_config(data_path, "EXAMPLE_core_configurations.csv")

    fig, ax1 = plt.subplots(nrows=1, ncols=1)
    a = core_configs[:17,:]

    # ax1.imshow(a, cmap='gnuplot', interpolation='nearest', vmin=0, vmax=31)
    ax1.imshow(a, cmap='gnuplot', vmin=-5, vmax=32)
    for (j,i),label in np.ndenumerate(a):
        ax1.text(i,j,label,ha='center',va='center')

    ax1.set_xticks(np.arange(0, 17, 2))
    ax1.set_yticks(np.arange(0, 17, 2))
    plt.hlines(y=np.arange(0, 17)+0.5, xmin=np.full(17, 0)-0.5, xmax=np.full(17, 17)-0.5, color="black")
    plt.vlines(x=np.arange(0, 17)+0.5, ymin=np.full(17, 0)-0.5, ymax=np.full(17, 17)-0.5, color="black")

    
    plt.show()

    

if __name__ == "__main__":
    main()