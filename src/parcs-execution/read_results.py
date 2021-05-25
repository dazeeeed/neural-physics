import os, sys, time
import re, io
import pandas as pd
import numpy as np

class FileReader():
    def __init__(self, n):
        self.sum_lines = []
        self.n = n
        self.headers = []
        self.data = pd.DataFrame(np.array([]))

    def read_files(self, configs_path):
        are_headers_read = False
        for i in range(self.n):
            filename = 'config'+str(i)+'/WUTBEAVRS-1.dep'
            try:
                with open(os.path.join(configs_path, filename), 'r') as f: 
                    lines = f.readlines()
                    if not are_headers_read:
                        self.headers = [word for word in lines[66474].replace('\n', '').split(sep=' ') if word != '']
                        self.headers[4] = 'Pxyz'
                        are_headers_read = True

                    s = io.StringIO(''.join(lines[66475:66544]))
                    self.data.append( pd.read_fwf(s, widths=[3,3,8,9,6,8,6,6,8,6,7,7,7,6,8,7,10,7,7], \
                        header=None).drop(5, axis=1) ) # drop (lfa,kz) column

            except FileNotFoundError:
                print("No such file or directory as " + filename)
                continue




def main():
    if len(sys.argv) == 1:
        prefix = ''
    elif len(sys.argv) == 2:
        prefix = sys.argv[1]
    else:
        print("Wrong arguments! Exiting...")
        sys.exit(1)

    current_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.abspath(os.path.join(current_path, '..', '..', 'data'))
    configs_path = (os.path.join(data_path, str(prefix) + 'PARCS-configs'))
    
    fr = FileReader(2)
    fr.read_files(configs_path)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))