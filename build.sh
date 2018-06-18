g++-8 -O3 -fopenmp -shared -std=c++11\
    -I /usr/local/include/python3.6m\
    `python3-config --cflags --ldflags`\
    sparse_bind.cpp -o sparse.so
