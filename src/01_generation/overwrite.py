import sys, os


def check_overwrite(path_name=None):
    if os.path.exists(path_name):
        print("\n==============================================")
        print("File " + str(path_name) + " already exists.")
        print("Are you sure you want to overwrite data? [Y/n]")
        print("if not, use --prefix= flag on the next run.")
        print("==============================================")
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
