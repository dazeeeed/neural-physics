import pandas as pd
import os, sys
from utils import load_npy, do_files_exist, check_overwrite
import time


def create_cycle_length_dict_with_casette_as_key(cycle_lengths_array):
    cycle_lengths_dict = {}
    for i, value in enumerate(cycle_lengths_array):
        cycle_lengths_dict[i + 1] = cycle_lengths_array[i]

    return cycle_lengths_dict


def main():
    current_path = os.path.abspath('')
    training_data_path = os.path.abspath(os.path.join(current_path, '..', '..', 'data', 'TRAINING_DATA.csv'))
    cycle_lengths_path = os.path.abspath(
        os.path.join(current_path, '..', '..', 'data', 'numpy-arrays', 'one_ten_cycle_lengths.npy'))
    new_training_data_path = os.path.abspath(
        os.path.join(current_path, '..', '..', 'data', 'TRAINING_DATA_CYCLE_LENGTHS_AS_FEATURES.csv'))

    if not do_files_exist(training_data_path, cycle_lengths_path):
        sys.exit(1)

    original_training_data = pd.read_csv(training_data_path)
    cycle_lengths = create_cycle_length_dict_with_casette_as_key(load_npy(cycle_lengths_path))

    new_features = original_training_data.iloc[:, :32].replace(cycle_lengths)
    new_training_data = pd.concat([new_features, original_training_data.iloc[:, 32:]], axis='columns')

    do_write_training_file = check_overwrite(new_training_data_path)

    if do_write_training_file:
        new_training_data.to_csv(new_training_data_path, sep=',', index=False, float_format='%.6f')
        print("File saved!")
    else:
        print("Aborting...")
        sys.exit(1)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))