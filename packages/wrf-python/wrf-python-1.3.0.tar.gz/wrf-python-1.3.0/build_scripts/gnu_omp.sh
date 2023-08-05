#!/bin/bash

cd ../fortran/build_help
gfortran -o sizes -fopenmp omp_sizes.f90
python sub_sizes.py

cd ..
gfortran -E ompgen.F90 -fopenmp -cpp -o omp.f90
#f2py *.f90 -m _wrffortran -h wrffortran.pyf --overwrite-signature
cd ..

python setup.py clean --all
python setup.py config_fc --f90flags="-mtune=generic -fopenmp" build_ext --libraries="gomp" build
pip install .

