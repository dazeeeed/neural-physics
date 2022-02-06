import matplotlib

matplotlib.rcParams.update({'font.size': 15})
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import time
import scipy
from scipy import stats

index_to_days_map = {
    0: 0.0,
    1: 1.0,
    2: 21.0,
    3: 41.0,
    4: 61.0,
    5: 81.0,
    6: 101.0,
    7: 121.0,
    8: 141.0,
    9: 151.0,
    10: 161.0,
    11: 171.0,
    12: 181.0,
    13: 191.0,
    14: 201.0,
    15: 211.0,
    16: 221.0,
    17: 231.0,
    18: 241.0,
    19: 251.0,
    20: 261.0,
    21: 271.0,
    22: 281.0,
    23: 291.0,
    24: 301.0,
    25: 311.0,
    26: 321.0,
    27: 331.0,
    28: 341.0,
    29: 351.0,
    30: 361.0,
    31: 371.0,
    32: 381.0,
    33: 391.0,
    34: 401.0,
    35: 411.0,
    36: 421.0,
    37: 431.0,
    38: 441.0,
    39: 451.0,
    40: 461.0,
    41: 466.0,
    42: 471.0,
    43: 476.0,
    44: 481.0,
    45: 486.0,
    46: 491.0,
    47: 496.0,
    48: 501.0,
    49: 506.0,
    50: 511.0,
    51: 516.0,
    52: 521.0,
    53: 526.0,
    54: 531.0,
    55: 536.0,
    56: 541.0,
    57: 546.0,
    58: 551.0,
    59: 556.0,
    60: 561.0,
    61: 566.0,
    62: 571.0,
    63: 576.0,
    64: 581.0,
    65: 586.0,
    66: 591.0,
    67: 596.0,
    68: 601.0}


class Error:
    def __init__(self, data_real, data_pred):
        self._data_real = data_real
        self._data_pred = data_pred

    def calc_mean_absolute(self):
        return np.mean(np.abs(self._data_real - self._data_pred))

    def calc_mean_relative(self):
        err_relative = np.abs(self._data_real - self._data_pred) / self._data_real * 100
        return np.abs(np.mean(err_relative))

    def calc_smape(self):
        """Symmetric mean absolute percentage error"""
        return 100 * np.mean(
            np.abs(self._data_pred - self._data_real) / (np.abs(self._data_real) + np.abs(self._data_pred)))

    def print(self):
        print("Error abs  | Error rel %\n--------------------------")
        print(f"    {self.get_absolute():.3f}  | {self.get_percentage():.3f} %")

    def get_absolute(self):
        return self.calc_mean_absolute()

    def get_percentage(self):
        # return self.calc_smape()
        return self.calc_mean_relative()


def main():
    current_path = os.path.dirname(os.path.realpath("__file__"))
    data_path = os.path.abspath(os.path.join(current_path, '..', '..', 'data'))

    data = pd.read_csv(os.path.join(data_path, "prediction", "prediction.csv"), sep='\t')
    fig, ax = plt.subplots()
    fig.set_size_inches(10, 7, forward=True)

    label_range = range(4, 69, 2)
    labels = ["rho_max", "rho1", "rho2", "rho3"] + \
             ["rho" + str(i) for i in range(4, 69, 2)] + \
             ["cycle_length_in_days"]

    days = [index_to_days_map.get(1), index_to_days_map.get(2), index_to_days_map.get(3)]
    for i in label_range:
        days.append(index_to_days_map.get(i))

    # # UNCOMMENT BELOW FOR PLOT OF SPECIFIC VALUE
    # what_to_plot = labels[-1]
    # data_real = data[what_to_plot + "_real"]
    # data_pred = data[what_to_plot + "_pred"]
    # ax.scatter(data_real, data_pred, marker='o', s=3, label="Prediction")
    # ax.plot([min(data_real), max(data_real)], [min(data_real), max(data_real)], color='black', label="Real")
    # # ax.set_xlabel("Real cycle length [days]")
    # # ax.set_ylabel("Predicted cycle length [days]")
    # # ax.set_xlabel("Real reactivity")
    # # ax.set_ylabel("Predicted reactivity")
    # # plt.title("Reactivity at the start of the fuel cycle")
    # ax.set_xlabel("Wartość rzeczywista")
    # ax.set_ylabel("Wartość przewidywana")
    # plt.title("Długość cyklu pracy")
    # ax.grid(True, ls=':')
    #
    # print("Pearson correlation: ", np.corrcoef(data_real, data_pred))

    # # UNCOMMENT BELOW FOR PLOT OF RHO PROGRESS
    # what_to_plot = labels[1:-1]
    # data_real = data.get([label + '_real' for label in what_to_plot]).iloc[0, :].to_numpy()
    # data_pred = data.get([label + '_pred' for label in what_to_plot]).iloc[0, :].to_numpy()
    #
    # ax.plot(days, data_real, label="Dane rzeczywiste", lw=4, ls='--', color='tab:blue')
    # ax.plot(days, data_pred, label="Przewidywanie", lw=2, ls='-', color='tab:orange')
    #
    # stddev_pred = np.std(data.get([label + '_real' for label in what_to_plot]).iloc[:, :].to_numpy(), axis=0)
    # ax.fill_between(days, data_pred-stddev_pred, data_pred+stddev_pred, alpha=0.3, color='tab:orange')
    #
    # # ENG
    # # ax.set_xlabel("Days")
    # # ax.set_ylabel("Reactivity")
    # # plt.title("Progression of reactivity prediction")
    # # PL
    # ax.set_xlabel("Dzień")
    # ax.set_ylabel("Reaktywność")
    # plt.title("Przewidywanie progresji reaktywności w czasie")
    # ax.grid(True, ls=':')
    # ax.legend()

    # # UNCOMMENT BELOW FOR HISTOGRAM
    what_to_plot = labels[-1]
    data_real = data[what_to_plot + "_real"]
    data_pred = data[what_to_plot + "_pred"]
    # ax.set_xlabel("Cycle length [days]")
    # ax.set_ylabel("Density")
    ax.set_xlabel("Długość cyklu pracy [dni]")
    ax.set_ylabel("Gęstość prawdopodobieństwa")
    _, bins_real, _ = ax.hist(data_real, bins=30, density=True, label="Dane rzeczywiste", alpha=0.3, color="orange")
    _, bins_pred, _ = ax.hist(data_pred, bins=30, density=True, label="Przewidywanie", alpha=0.3, color="dodgerblue")
    ax.legend()
    ax.grid(True, ls=':')
    # plt.title("Length of fuel cycle")

    mu_real, sigma_real = stats.norm.fit(data_real)
    best_fit_line_real = stats.norm.pdf(bins_real, mu_real, sigma_real)
    mu_pred, sigma_pred = stats.norm.fit(data_pred)
    best_fit_line_pred = stats.norm.pdf(bins_pred, mu_pred, sigma_pred)

    ax.plot(bins_real, best_fit_line_real, linewidth=3, color="orange")
    ax.plot(bins_pred, best_fit_line_pred, linewidth=3, color="dodgerblue")
    fig.text(0.17,
             0.83,
             rf"Real: $\mu=${mu_real:.2f} $\sigma$={sigma_real:.2f}" + "\n"
                                                                       rf"Predicted: $\mu=${mu_pred:.2f} $\sigma$={sigma_pred:.2f}",
             style='italic',
             fontsize=15,
             bbox={'facecolor': 'grey', 'alpha': 0.1, 'pad': 10})

    error = Error(data_real, data_pred)
    error.print()

    # fig.text(0.65,
    #          0.175,
    #          f'Mean absolute error: {error.get_absolute():.4f}\nMean relative error: {error.get_percentage():.2f}%',
    #          style='italic',
    #          fontsize=15,
    #          bbox={'facecolor': 'grey', 'alpha': 0.1, 'pad': 10})

    fig.tight_layout()
    ax.tick_params(direction="in")

    # name_of_plot = "reactivity_start"
    # for extension in [".png", ".svg"]:
    #     plt.savefig(os.path.join(data_path,
    #                              'graphics',
    #                              name_of_plot + extension), dpi=300)
    plt.show()


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
