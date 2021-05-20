import numpy as np
import pandas as pd
import os, io
import sys, getopt
import shutil
from overwrite import check_overwrite

CORE_SIZE = 17

class CoreConfiguration():

    def __init__(self, data_path): 
        self.vector_filename = "vectors.csv"
        self.core_config_filepath = "core_configs.csv"
        self.vector_path = data_path + '/' + self.vector_filename
        self.prefix = ''
        self.geom_filename = "GEOM_FC_ASSY_TYPE_REV2"
        self.parcs = False

    def read_vector_data(self, vector_path):
        """Read file containing vectors."""
        self.vector_path = vector_path
        self.vector_data = pd.read_csv(self.vector_path, sep=',', header=None).values
        self.vector_data_len = len(self.vector_data)

    def generate_configuration(self, vector):
        """Generate configuration of reactor core from single vector of casettes configuration."""
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

    def generate_configuration_data(self):
        """Create array consisting of reactor core configurations, where vector_data is
        array of random vectors of casettes configuration.
        """
        self.core_config_data = np.array([self.generate_configuration(self.vector_data[i]) \
            for i in range(self.vector_data_len)])

    def print_core_config_data(self):
        """Generating .csv file with core configurations"""
        core_configs_printable = np.reshape(self.core_config_data, (-1,CORE_SIZE))
        core_configs_df = pd.DataFrame(core_configs_printable)
        core_configs_df.to_csv(self.core_config_filepath, sep=",", header=False, index=False)

    def pretty_print(self, df):
        """Function used to print numpy array separated by tab without brackets."""
        s = io.StringIO()
        df.to_csv(s, sep='\t', header=False, index=False)
        return s.getvalue()

    def create_parcs_config(self, datapath):
        """Create PARCS configuration file. Datapath is location of data folder."""
        with open(datapath+"/"+self.geom_filename, 'r') as conf:
            config_default_start = ""
            for i in range(5):
                config_default_start += conf.readline()
            for i in range(17):
                conf.readline()
            config_default_end = ''.join(conf.readlines())

        parcs_configs_path = datapath+"/"+self.prefix+"PARCS-configs"

        try:
            os.stat(parcs_configs_path)
        except:
            os.mkdir(parcs_configs_path)

        for i in range(self.vector_data_len):
            try:
                os.stat(parcs_configs_path + "/config"+str(i))
            except:
                os.mkdir(parcs_configs_path + "/config"+str(i))

            shutil.copy(datapath+"/BEAVRS_20_HFP_MULTI_5_2018.INP", parcs_configs_path + "/config"+str(i))            

            with open(parcs_configs_path + "/config" + str(i) + "/" + self.geom_filename, 'w') as f:
                f.write(config_default_start)
                f.write(self.pretty_print(pd.DataFrame(self.core_config_data[i,:,:])))                
                f.write(config_default_end)

if __name__ == '__main__':
    """Core configuration main function.
    System arguments
    ----------
    -p, --prefix PREFIX : valid prefix for filenames generated in data directory.

    -i, --input INPUT : generate core configurations based on the input file, defaults to vectors.csv.

    -x, --parcs : create PARCS configuration folders from generated core configurations.
    """
    do_write = True
    input_not_specified = True

    generation_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.abspath(os.path.join(generation_path, '../..', 'data'))
    try:
        os.stat(data_path)
    except:
        os.mkdir(data_path)

    cc = CoreConfiguration(data_path=data_path)

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'p:i:x', \
            ["prefix=", "input=","parcs"])
    except getopt.GetoptError:
        print('Error, check format of arguments...')
        sys.exit(1)
        
    if len(args) > len(opts):
        print("Wrong arguments! Exiting...")
        sys.exit(1)

    for opt, arg in opts:
        if opt in ('-p', '--prefix'):
            cc.prefix = arg
        elif opt in ('-i', '--input'):
            cc.vector_filename = arg
            input_not_specified = False
        elif opt in ('-x', '--parcs'):
            cc.parcs = True

    try:
        cc.read_vector_data(data_path + '/' + cc.vector_filename)
    except:
        print("File consisting of vectors does not exist or some problems occurred.\n"+ \
            "Check your input files. Exiting...")
        sys.exit(1)

    if input_not_specified:
        print("Input not specified. Using default vectors.csv file...")

    cc.generate_configuration_data()
    cc.core_config_filepath = data_path + '/' + cc.prefix + "core_configurations.csv"
    
    do_write = check_overwrite(cc.core_config_filepath)

    if do_write:
        cc.print_core_config_data()
        print("File "+ cc.prefix + "core_configurations.csv saved!")
    else:
        print("Aborting...")
        sys.exit(1)
    
    if cc.parcs:
        cc.create_parcs_config(data_path)
        print("PARCS configuration folders created.")
    
          