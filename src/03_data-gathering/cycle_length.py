import time, os
import numpy as np
from utils import check_overwrite, index_to_days_interpolation
import sys
import getopt

class CycleLength:
    def __init__(self):
        self._do_write_cycle_matrix = True
        self.keff_matrix = []
        self.cycle_length_matrix = []
        self.index_to_days_map = {
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

    def load_matrix(self, keff_matrix_npy):
        with open(os.path.join('..', '..', 'data', 'numpy-arrays', keff_matrix_npy), 'rb') as f:
            self.keff_matrix = np.load(f)

    def calculate_lengths(self):
        for cycle in self.keff_matrix:
            # The trick here is to skip first two iterations as they are in ascending order and aren't
            # descending monotonically
            sorted_arr = np.sort(cycle[2:])
            # np.searchsorted returns number for ascending order so in our case substract this number
            # from 67 (length of sorted array without two first elements), add two first elements and subtract
            # one as we want length of cycle not index of array where we should insert 1. 
            cycle_length = 67 - np.searchsorted(sorted_arr, 1) + 2 - 1
            # interpolation between two cycle_lengths for more accurate cycle length
            if (cycle_length <= len(cycle) - 1):
                cycle_length = cycle_length - 1.0 / (cycle[cycle_length] - cycle[cycle_length + 1]) \
                               * (1 - cycle[cycle_length])

            self.cycle_length_matrix.append(index_to_days_interpolation(cycle_length))
        print(self.cycle_length_matrix)

    def save_lengths(self, npy_location):
        self._do_write_cycle_matrix = check_overwrite(npy_location)
        if self._do_write_cycle_matrix:
            with open(npy_location, 'wb') as f:
                np.save(f, self.cycle_length_matrix)
            print("File saved!")
        else:
            print("Aborting...")
            sys.exit(1)


def main():
    current_path = os.path.dirname(os.path.realpath(__file__))
    matrix_path = os.path.abspath(os.path.join(current_path, '..', '..', 'data', 'numpy-arrays'))
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

    cl = CycleLength()
    cl.load_matrix(os.path.join(matrix_path, prefix + 'keff.npy'))
    cl.calculate_lengths()
    cl.save_lengths(os.path.join(matrix_path, prefix + 'cycle_lengths.npy'))


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
