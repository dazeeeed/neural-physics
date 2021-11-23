import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import time

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

def main():
    current_path = os.path.dirname(os.path.realpath("__file__"))
    data_path = os.path.abspath(os.path.join(current_path, '..', '..', 'data'))

    data = pd.read_csv(os.path.join(data_path, "prediction", "prediction.csv"), sep='\t')
    fig, ax = plt.subplots()

    label_range = range(4, 69, 2)
    labels = ["keff_max", "keff1", "keff2", "keff3"] + \
             ["keff" + str(i) for i in label_range] + \
             ["cycle_length_in_days"]

    what_to_plot = labels[-1]
    # what_to_plot = labels[1:-1]

    days = []
    days.append(index_to_days_map.get(1))
    days.append(index_to_days_map.get(2))
    days.append(index_to_days_map.get(3))
    for i in label_range:
        days.append(index_to_days_map.get(i))

    # # UNCOMMENT BELOW FOR PLOT OF SPECIFIC VALUE
    data_real = data[what_to_plot + "_real"]
    data_pred = data[what_to_plot + "_pred"]

    ax.scatter(data_real, data_pred, marker='o', s=3)
    ax.plot([min(data_real), max(data_real)], [min(data_real), max(data_real)], color='black')


    err_absolute = np.abs(data_real - data_pred)
    err_relative = np.abs(data_real - data_pred) / data_real * 100

    err_absolute_mean = np.mean(err_absolute)
    err_relative_mean = np.abs(np.mean(err_relative))

    print("Error abs  | Error rel %")
    print("--------------------------")
    print(f"    {err_absolute_mean:.3f}  | {err_relative_mean:.3f} %")

    # # UNCOMMENT BELOW FOR PLOT OF KEFF PROGRESS
    # data_real = data.get([label+'_real' for label in what_to_plot]).iloc[0, :].to_numpy()
    # data_pred = data.get([label+'_pred' for label in what_to_plot]).iloc[0, :].to_numpy()

    # ax.plot(days, data_real, label="Real", lw=4, ls='--')
    # ax.plot(days, data_pred, label="Predicted", lw=2, ls='-')
    # ax.set_xlabel("Days")
    # ax.set_ylabel("Reactivity")
    # ax.legend()




    ax.tick_params(direction="in")
    plt.show()


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))