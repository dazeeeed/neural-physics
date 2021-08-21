import os, sys, time
import io
import pandas as pd
import numpy as np
from utils import check_overwrite
import getopt


class FileReader:
    """
    FileReader class is used for reading results from generated parcs configurations.

    Parameters
    ----------
    n INTEGER : Number of configurations to read from.
    
    headers LIST OF STRING : headers of results.

    data DATAFRAME : data read from the files. 

    """

    def __init__(self, n):
        self.n = n
        self.headers = []
        self.data = pd.DataFrame(np.array([]))

    def read_files(self, configs_path):
        are_headers_read = False
        for i in range(self.n):
            filename = os.path.join("config" + str(i), "WUTBEAVRS-1.dep")
            try:
                with open(os.path.join(configs_path, filename), 'r') as f:
                    lines = f.readlines()[66474:66544]

                    if not are_headers_read:
                        self.headers = [word for word in lines[0].replace('\n', '').split(sep=' ') if word != '']
                        self.headers[4] = 'Pxyz'
                        are_headers_read = True

                    s = io.StringIO(''.join(lines[1:]))

                    pandas_data = pd.read_fwf(s, widths=[3, 3, 8, 9, 6, 8, 6, 6, 8, 6, 7, 7, 7, 6, 8, 7, 10, 7, 7], \
                                              header=None).drop(list(range(5, 18)), axis=1)  # drop (lfa,kz) column
                    self.data = self.data.append(pandas_data)

            except FileNotFoundError:
                print("No such file or directory as " + filename)
                continue

    def get_keff_matrix(self):
        keff = self.data[3].values
        self._keff = np.reshape(keff, (-1, 69))

        return self._keff

    def get_PPF_matrix(self):
        PPF = self.data[4].values
        self._PPF = np.reshape(PPF, (-1, 69))
        return self._PPF

    def save(self, matrix, current_path, filename):
        location_path = os.path.join(current_path, '..', '..', 'data', 'numpy-arrays', filename)
        do_write_matrix = check_overwrite(location_path)
        if do_write_matrix:
            with open(location_path, 'wb') as f:
                np.save(f, matrix)
            print("File saved!")
        else:
            print("Aborting...")
            sys.exit(1)


def main():
    """
    Read results based on FileReader class.

    System arguments
    ----------
    -n, --number INTEGER : number of configurations to read from.

    -p, --prefix STRING : valid prefix for directory with parcs configurations.

    """
    number_of_configs_to_read = 10
    prefix = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'n:p:', \
                                   ["number=", "prefix="])
    except getopt.GetoptError:
        print('Error, check format of arguments...')
        sys.exit(1)

    if len(args) > len(opts):
        print("Wrong arguments! Exiting...")
        sys.exit(1)

    for opt, arg in opts:
        if opt in ('-p', '--prefix'):
            prefix = arg
        elif opt in ('-n', '--number'):
            try:
                number_of_configs_to_read = int(arg)
            except:
                print("Cannot convert to integer. Leaving default number of 1000 vectors.")
                sys.exit(1)

    current_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.abspath(os.path.join(current_path, '..', '..', 'data'))
    configs_path = (os.path.join(data_path, str(prefix) + 'PARCS-configs'))

    fr = FileReader(number_of_configs_to_read)
    fr.read_files(configs_path)
    keff_matrix = fr.get_keff_matrix()
    ppf_matrix = fr.get_PPF_matrix()

    fr.save(keff_matrix, current_path, 'keff.npy')
    fr.save(ppf_matrix, current_path, 'ppf.npy')


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
