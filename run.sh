#!/usr/bin/zsh

export OMP_PLACES=cores
export OMP_PROC_BIND=close
export OMP_DISPLAY_ENV=true

MYTIME=$(date +"data-%Y-%m-%d-%T")
OMP_NUM_THREADS=1 python3 benchmark.py --scipy --ref --omp --save $MYTIME

unset OMP_DISPLAY_ENV
for i in {1..24}
    OMP_NUM_THREADS=$i python3 benchmark.py --omp --save $MYTIME
