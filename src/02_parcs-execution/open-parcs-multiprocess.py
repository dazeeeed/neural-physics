import os, sys, time
import multiprocessing

beavrs_name = 'BEAVRS_20_HFP_MULTI_5_2018.INP'
current_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.abspath(os.path.join(current_path, '..', '..', 'data'))
parcs_program_path = os.path.abspath(os.path.join(data_path, '..', '..', 'PARCS', 'p320mXX.exe'))

def config_path(data_path, i):
    return os.path.abspath(os.path.join(data_path, 'PARCS-configs', 'config' + str(i)))

def worker():
    os.system(" ".join([parcs_program_path, 'BEAVRS_20_HFP_MULTI_5_2018.INP']))

def main():

    # =============================================================
    # First argument needs to be starting number of configuration.
    # Second argument is a number of the last - 1 config being used.
    # =============================================================

    if len(sys.argv) != 3:
        print("Wrong arguments. Exiting...")
        sys.exit(1)

    jobs = []
    for i in range( int(sys.argv[1]), int(sys.argv[2]) ):
        os.chdir(config_path(data_path, i))
        p = multiprocessing.Process(target=worker)
        jobs.append(p)
        p.start()
        
if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
