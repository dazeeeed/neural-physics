import getopt
import os
import sys
import time

import core_generation as cg
import vector_generation as vg
from overwrite import check_overwrite

CORE_SIZE = 17


def main():
    """
    Generate vectors of cassettes and/or reactor configuration.

    System arguments
    ----------
    -p, --prefix STRING : valid prefix for filenames generated in data directory.

    -n, --number INTEGER : generate core configurations based on the input file, defaults to vectors.csv.

    -x, --parcs : create PARCS configuration folders from generated core configurations.
    """

    generation_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.abspath(os.path.join(generation_path, '../..', 'data'))
    try:
        os.stat(data_path)
    except:
        os.mkdir(data_path)

    vectors = vg.Vectors(1000)
    cc = cg.CoreConfiguration(data_path=data_path)

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'p:n:x', ["prefix=", "number=", "--parcs"])
    except getopt.GetoptError:
        print('Error, check format of arguments...')
        sys.exit(1)

    if len(args) > len(opts):
        print("Wrong arguments! Exiting...")
        sys.exit(1)

    for opt, arg in opts:
        if opt in ('-p', '--prefix'):
            vectors.prefix = arg
            cc.prefix = arg
        elif opt in ('-n', '--number'):
            try:
                vectors.n = int(arg)
            except:
                print("Cannot convert to integer. Leaving default number of 1000 vectors.")
                sys.exit(1)
        elif opt in ('-x', '--parcs'):
            cc.parcs = True

    vectors.filepath = data_path + '/' + vectors.prefix + "vectors.csv"
    do_write_vectors = check_overwrite(vectors.filepath)

    if do_write_vectors:
        vectors.save(separator=',')
        print("File saved!")
    else:
        print("Aborting...")
        sys.exit(1)

    try:
        cc.read_vector_data(vectors.filepath)
    except:
        print("File consisting of vectors does not exist or some problems occurred.\n" + \
              "Check your input files. Exiting...")
        sys.exit(1)

    cc.generate_configuration_data()
    cc.core_config_filepath = data_path + '/' + cc.prefix + "core_configurations.csv"

    do_write_cores = check_overwrite(cc.core_config_filepath)

    if do_write_cores:
        cc.print_core_config_data()
        print("File " + cc.prefix + "core_configurations.csv saved!")
    else:
        print("Aborting...")
        sys.exit(1)

    if cc.parcs:
        cc.create_parcs_config(data_path)
        print("PARCS folders created.")


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
