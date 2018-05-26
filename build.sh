/usr/local/bin/g++-8 -O3 -fopenmp -shared -std=c++11 -I /usr/local/Cellar/pybind11/2.1.3/include `python3-config --cflags --ldflags` sparse_bind.cpp -o sparse.so
