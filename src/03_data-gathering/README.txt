>>read_results.py<<
Read specified number of results from the configurations which are in the folder called: prefix+'PARCS-configs' 
and save them to prefix+'FILENAME.npy' numpy arrays.

System arguments
----------
-p, --prefix STRING : valid prefix for filenames generated in data directory.

-n, --number INTEGER : generate core configurations based on the input file, defaults to vectors.csv.



>>cycle_length.py<<
Create numpy array with name prefix+'cycle_lengths.npy' consisting of cycle lengths for each cycle.

System arguments
----------
-p, --prefix STRING : valid prefix for filenames generated in data directory.



>>create_training_data.py<<
Create .csv file ready for training the neural network.

System arguments
----------
-p, --prefix PREFIX : valid prefix for filenames used and generated in data directory.


>>replace_values_in_1_to_32_column.py<<
Create .csv file ready for training the neural network with replaced values in 1-32 columns with specified values.

System arguments
----------
-p, --prefix PREFIX : valid prefix for filenames used and generated in data directory.