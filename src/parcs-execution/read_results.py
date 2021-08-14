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
            filename = os.path.join("config" + str(i), "WUTBEAVRS-1.dep")
            try:
                with open(os.path.join(configs_path, filename), 'r') as f:           
                    lines = f.readlines()[66474:66544]
                    
                    if not are_headers_read:
                        self.headers = [word for word in lines[0].replace('\n', '').split(sep=' ') if word != '']
                        self.headers[4] = 'Pxyz'
                        are_headers_read = True

                    s = io.StringIO(''.join(lines[1:]))

                    pandas_data = pd.read_fwf(s, widths=[3,3,8,9,6,8,6,6,8,6,7,7,7,6,8,7,10,7,7], \
                        header=None).drop(list(range(5,18)), axis=1)    # drop (lfa,kz) column
                    self.data = self.data.append(pandas_data) 
                       
            except FileNotFoundError:
                print("No such file or directory as " + filename)
                continue
    
    def get_keff_matrix(self):
        keff = self.data[3].values
        self._keff = np.reshape(keff, (-1,69))
        # print(self._keff)
        
        # str_ = ""
        # for elem in self._keff[0]:
        #     str_ += str(elem) + ',' 
        # print(str_)
        return self._keff


    def get_PPF_matrix(self):
        PPF = self.data[4].values
        self._PPF = np.reshape(PPF, (-1,69))
        return self._PPF

    # def get_cycle_length_matrix(self):
    #     # Skip two first elements from keff matrix for one configuration because they ascend
    #     for keff_

    def save(self, matrix, filename):
        with open(os.path.join('..', '..', 'data', 'numpy-arrays', filename), 'wb') as f:
            np.save(f, matrix) 
            

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
    keff_matrix = fr.get_keff_matrix()
    ppf_matrix = fr.get_PPF_matrix()
    # fr.get_cycle_length_matrix()
    fr.save(keff_matrix, 'keff.npy')
    

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
    