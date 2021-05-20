import numpy as np
import pandas as pd
import sys, getopt
import time
import os, io

CORE_SIZE = 17

def generate_vector():
    """Generate random vector of casettes configuration."""
    return np.random.randint(low=1, high=10, size=31)

def generate_vector_data(number_of_vectors=1000):
    """Generate array of random vectors of casettes configuration."""
    return np.array([generate_vector() for _ in range(number_of_vectors)])

def generate_configuration(vector):
    """Generate configuration of reactor core from vector of casettes configuration."""
    core_config = np.zeros((CORE_SIZE,CORE_SIZE), dtype=np.uint8)

    # put random variables from vector into configuration
    core_config[1:9,  8] = vector[:8]
    core_config[1:8,  9] = vector[8:15]
    core_config[1:7, 10] = vector[16:22]
    core_config[1:6, 11] = vector[22:27]
    core_config[2:5, 12] = vector[27:30]
    core_config[2:4, 13] = vector[30:]

    # add reflectors (10) 
    core_config[0, 8:13] = 10
    core_config[1, 12:15] = 10
    core_config[2, 14] = 10

    # flip and rotate to get full the core configuration
    core_config |= np.flip(core_config, axis=1)
    core_config |= np.rot90(core_config) | np.rot90(core_config,2) | np.rot90(core_config,3)

    return core_config
    
def generate_configuration_data(vector_data, number_of_vectors=1000):
    """Create array consisting of reactor core configurations, where vector_data is
    array of random vectors of casettes configuration.
    """
    return np.array([generate_configuration(vector_data[i]) for i in range(number_of_vectors)])

def pretty_print(df):
    """Function used to print numpy array separated by tab without brackets, where df 
    is a pandas dataframe."""
    s = io.StringIO()
    df.to_csv(s, sep='\t', header=False, index=False)
    return s.getvalue()

def create_parcs_config(core_config_array, datapath, number_of_vectors):
    """Create PARCS configuration file.
    Parameters
    ----------
    core_config_array : 
    """
    with open(datapath+"/PARCS-config-default", 'r') as conf:
        config_default_start = ""
        for i in range(5):
            config_default_start += conf.readline()
        for i in range(17):
            conf.readline()
        config_default_end = ''.join(conf.readlines())

    for i in range(number_of_vectors):
        try:
            os.stat(datapath+"/PARCS-configs/config"+str(i))
        except:
            os.mkdir(datapath+"/PARCS-configs/config"+str(i))

        with open(datapath+"/PARCS-configs/config"+str(i)+"/GEOM_GC_ASSY_TYPE_REV2", 'w') as f:
            f.write(config_default_start)
            f.write(pretty_print(pd.DataFrame(core_config_array[i,:,:])))
            
            f.write(config_default_end)




def main():
    """
    Generate vectors of casettes and/or reactor configuration.

    System arguments
    ----------
    -p, --prefix PREFIX : valid prefix for filenames generated in data directory.

    -n, --number NUMBER : integer number of random to generate (default is 1000).

    -v, --vectors-only : do NOT generate casette configuration (reactor core configuration).
    """

    vectors_only = False
    number_of_vectors = 1000
    prefix = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'p:n:v', \
            ["prefix=", "number=", "vectors-only"])
    except getopt.GetoptError:
        print('Error, check format of arguments...')
        sys.exit(1)

    if len(args) > len(opts):
        print("Wrong arguments! Exiting...")
        exit(1)

    for opt, arg in opts:
        if opt in ('-p', '--prefix'):
            prefix = arg
        elif opt in ('-n', '--number'):
            try:
                number_of_vectors = int(arg)
            except:
                print("Cannot convert to integer. Leaving default number of 1000 vectors.")
        elif opt in ('-v', '--vectors-only'):
            vectors_only = True
    
    generation_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.abspath(os.path.join(generation_path, '..', 'data'))
    vector_filename = data_path + '/' + prefix + "vectors.csv"
    core_config_filename = data_path + '/' + prefix + "core_configurations.csv"
    
    try:
        os.stat(data_path)
    except:
        os.mkdir(data_path)

    vector_data = generate_vector_data(number_of_vectors)
    vector_df = pd.DataFrame(vector_data)
    vector_df.to_csv(vector_filename, sep=",", header=False, index=False)

    if not vectors_only:
        core_configs = generate_configuration_data(vector_data, number_of_vectors)
        core_configs_printable = np.reshape(core_configs, (-1,CORE_SIZE))
        core_configs_df = pd.DataFrame(core_configs_printable)
        core_configs_df.to_csv(core_config_filename, sep=",", header=False, index=False)

        create_parcs_config(core_configs, data_path, number_of_vectors)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
    
