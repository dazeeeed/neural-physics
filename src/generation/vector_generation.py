import numpy as np
import pandas as pd
import sys, getopt
import os, time
from overwrite import check_overwrite

class Vectors():
    def __init__(self, number_of_vectors):
        self.n = number_of_vectors
        self.prefix = ''
        self.filepath = 'vectors.csv'
        self.separator = ','

    def generate_vector(self):
        """Generate random vector of casettes configuration."""
        return np.random.randint(low=1, high=10, size=32)

    def generate_vector_data(self):
        """Generate array of random vectors of casettes configuration."""
        return np.array([self.generate_vector() for _ in range(self.n)])

    def save(self, separator):
        "Save the .csv file located in /data folder."
        self.separator = separator
        self.vector_data = self.generate_vector_data()
        self.vector_df = pd.DataFrame(self.vector_data)
        self.vector_df.to_csv(self.filepath, sep=self.separator, header=False, index=False)

def main():
    """Vectors generation main function.
    System arguments
    ----------
    -p, --prefix STRING : valid prefix for filenames generated in data directory.

    -n, --number INTEGER : generate core configurations based on the input number, defaults to vectors.csv.

    """
    do_write = True
    generation_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.abspath(os.path.join(generation_path, '../..', 'data'))
    try:
        os.stat(data_path)
    except:
        os.mkdir(data_path)

    vectors = Vectors(1000)
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'p:n:', \
            ["prefix=", "number="])
    except getopt.GetoptError:
        print('Error, check format of arguments...')
        sys.exit(1)
        
    if len(args) > len(opts):
        print("Wrong arguments! Exiting...")
        sys.exit(1)

    for opt, arg in opts:
        if opt in ('-p', '--prefix'):
            vectors.prefix = arg
        elif opt in ('-n', '--number'):
            try:
                vectors.n = int(arg)
            except:
                print("Cannot convert to integer. Leaving default number of 1000 vectors.")
                sys.exit(1)

    vectors.filepath = data_path + '/' + vectors.prefix + "vectors.csv"

    do_write = check_overwrite(vectors.filepath)
    
    if do_write:
        vectors.save(separator=',')
        print("File saved!")
    else:
        print("Aborting...")
        sys.exit(1)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
    

