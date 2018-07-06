This is an example of wrapping sparse kernels from `scipy.sparse` with bindthem: https://github.com/lukeolson/bindthem


## Requirements

This script uses

- OpenMP
- omp_thread_count
- scipy
- tqdm

## How to use

0. Modify `setup.py` with your (openmp supported) compiler

1. Build the sparse library

```
python setup.py build_ext --inplace
```

2. Run the benchmark

```
python benchmark --scipy --openmp
```

See `run.sh` for a full run.


## Notes

- You need OpenMP support in your compiler.  On a mac, `brew install llvm libomp` will work
- Put the path for your compiler in `setup.py`

## Example Output

THis uses `analyze-data.ipynb`
