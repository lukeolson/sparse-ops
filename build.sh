/usr/local/opt/llvm/bin/clang++ -O3 -shared -std=c++11\
    -fopenmp\
    -fvisibility=hidden\
    -I /usr/local/include/python3.6m\
    -flto\
    `python3-config --cflags --ldflags`\
    sparse_bind.cpp -o sparse.so
