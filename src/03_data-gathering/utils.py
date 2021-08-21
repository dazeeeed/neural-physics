import os
import sys


def check_overwrite(path_name=None):
    if os.path.exists(path_name):
        print("\n=============================================================================")
        print("File " + str(path_name) + " already exists.")
        print("Are you sure you want to overwrite data? [Y/n]")
        print("=============================================================================")
        try:
            do_write_inp = input("Your choice: ")
            if do_write_inp == "Y":
                return True
            elif do_write_inp in ('n', 'N'):
                return False
            sys.exit(1)
        except:
            print("\nNot specified whether to overwrite. Exiting...")
            sys.exit(1)
    return True


def index_to_days_interpolation(x):
    if x <= 0:
        return 0
    elif 1 <= x < 9:
        return 1 + 20 * (x - 1)
    elif 9 <= x < 40:
        return 151 + 10 * (x - 9)
    else:
        return 461.0 + 5 * (x - 40)
