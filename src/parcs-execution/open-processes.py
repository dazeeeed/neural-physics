import subprocess, os


if __name__ == '__main__':
    parcs_execution_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.abspath(os.path.join(parcs_execution_path, '../..', 'data'))
    parcs_program_path = os.path.abspath(os.path.join(data_path, '../..', 'PARCS'))

    # start all programs
    processes = [subprocess.Popen(parcs_program_path + "/p320mXX.exe") for _ in range(2)]
    # wait
    for process in processes:
        process.wait()