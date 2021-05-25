import subprocess, os, time, sys

def config_path(data_path, i):
    return os.path.abspath(os.path.join(data_path, 'PARCS-configs', 'config' + str(i)))

def main():
    beavrs_name = 'BEAVRS_20_HFP_MULTI_5_2018.INP'
    current_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.abspath(os.path.join(current_path, '..', '..', 'data'))
    parcs_program_path = os.path.abspath(os.path.join(data_path, '..', '..', 'PARCS', 'p320mXX.exe'))

    # start all programs
    processes = []

    if len(sys.argv) != 2:
        print("Wrong arguments. Exiting...")
        sys.exit(1)

    for i in range( int(sys.argv[1]) ):
        os.chdir(config_path(data_path, i))
        processes.append(subprocess.Popen([parcs_program_path, 'BEAVRS_20_HFP_MULTI_5_2018.INP'], bufsize=-1))
        
    # wait
    for process in processes:
        process.wait()


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))