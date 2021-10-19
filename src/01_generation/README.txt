>>generation.py<<
Generate vectors of casettes and reactor configuration and if flag -x is specified create PARCS configuration
files.

System arguments
----------
-p, --prefix STRING : valid prefix for filenames generated in data directory.

-n, --number INTEGER : generate core configurations based on the input file, defaults to vectors.csv.

-x, --parcs : create PARCS configuration folders from generated core configurations.



>>vector_generation.py<<
Vectors generation main function.

System arguments
----------
-p, --prefix STRING : valid prefix for filenames generated in data directory.

-n, --number INTEGER : generate core configurations based on the input file, defaults to vectors.csv.



>>core_generation.py<<
Core configuration main function.

System arguments
----------
-p, --prefix PREFIX : valid prefix for filenames generated in data directory.

-i, --input INPUT : generate core configurations based on the input file, defaults to vectors.csv.

-x, --parcs : create PARCS configuration folders from generated core configurations.



