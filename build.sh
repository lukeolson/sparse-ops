g++-7 -O3 -fopenmp -shared -std=c++11 -fPIC -I /home/lukeo/pybind11/include `python3-config --cflags --ldflags` sparse_bind.cpp -o sparse.so
