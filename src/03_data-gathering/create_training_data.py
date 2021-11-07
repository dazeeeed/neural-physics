import getopt
import os
import sys
import time

import numpy as np
import pandas as pd
from utils import check_overwrite, do_files_exist, load_npy


def create_big_array(vector_data, keff_matrix, ppf_matrix, cycle_lengths):
    """
    Concatenate matrices into one 2D array, where each row consists of vector_data row, first element of row in
    keff_matrix, maximum value of row in keff_matrix, keff_matrix row, first element of row in ppf_matrix,
    maximum value of row in ppf_matrix, last value of ppf_matrix row, and length of the cycle (where keff descend
    below 1).

    Parameters
    ----------
    vector_data : pandas.DataFrame
    keff_matrix : pandas.DataFrame
    ppf_matrix : pandas.DataFrame
    cycle_lengths : pandas.DataFrame

    Returns
    -------
    concatenated_array : pandas.DataFrame
    """
    return pd.concat([vector_data, keff_matrix[0], keff_matrix.max(axis=1), keff_matrix,
                      ppf_matrix[0], ppf_matrix.max(axis=1), ppf_matrix.iloc[:, -1], cycle_lengths], axis='columns')


def main():
    current_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.abspath(os.path.join(current_path, '..', '..', 'data'))

    headers = [
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
        "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32",
        "keff_start", "keff_max",
        "keff1", "keff2", "keff3", "keff4", "keff5", "keff6", "keff7", "keff8", "keff9", "keff10", "keff11", "keff12",
        "keff13", "keff14", "keff15",
        "keff16", "keff17", "keff18", "keff19", "keff20", "keff21", "keff22", "keff23", "keff24", "keff25", "keff26",
        "keff27", "keff28", "keff29", "keff30",
        "keff31", "keff32", "keff33", "keff34", "keff35", "keff36", "keff37", "keff38", "keff39", "keff40", "keff41",
        "keff42", "keff43", "keff44", "keff45",
        "keff46", "keff47", "keff48", "keff49", "keff50", "keff51", "keff52", "keff53", "keff54", "keff55", "keff56",
        "keff57", "keff58", "keff59", "keff60",
        "keff61", "keff62", "keff63", "keff64", "keff65", "keff66", "keff67", "keff68", "keff69",
        "ppf_start", "ppf_max", "ppf_end",
        "cycle_length_in_days"
    ]
    prefix = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'p:', ["prefix="])
    except getopt.GetoptError:
        print('Error, check format of arguments...')
        sys.exit(1)

    if len(args) > len(opts):
        print("Wrong arguments! Exiting...")
        sys.exit(1)

    for opt, arg in opts:
        if opt in ('-p', '--prefix'):
            prefix = arg

    if not do_files_exist(prefix + 'vectors.csv', prefix + 'keff.npy', prefix + 'ppf.npy',
                                     prefix + 'cycle_lengths.npy'):
        sys.exit(1)

    vector_data = pd.read_csv(os.path.join(data_path, prefix + 'vectors.csv'), sep=',', header=None)
    keff_matrix = pd.DataFrame(load_npy(os.path.join(data_path, 'numpy-arrays', prefix + 'keff.npy')))
    ppf_matrix = pd.DataFrame(load_npy(os.path.join(data_path, 'numpy-arrays', prefix + 'ppf.npy')))
    cycle_lengths = pd.DataFrame(load_npy(os.path.join(data_path, 'numpy-arrays', prefix + 'cycle_lengths.npy')))

    big_array = create_big_array(vector_data, keff_matrix, ppf_matrix, cycle_lengths)
    big_array.columns = headers

    training_file_datapath = os.path.join(data_path, prefix + 'TRAINING_DATA.csv')
    do_write_training_file = check_overwrite(training_file_datapath)

    if do_write_training_file:
        big_array.to_csv(training_file_datapath, sep=',', index=False, float_format='%.6f')
        print("File saved!")
    else:
        print("Aborting...")
        sys.exit(1)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
