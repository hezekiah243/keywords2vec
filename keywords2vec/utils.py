import gzip
import os

from fastprogress.fastprogress import progress_bar
from concurrent.futures import ProcessPoolExecutor, as_completed


# BEGIN From fastai
def parallel(func, arr, max_workers=None):
    with ProcessPoolExecutor(max_workers=max_workers) as ex:
        futures = [ex.submit(func, o, i) for i, o in enumerate(arr)]
        results = []
        for f in progress_bar(as_completed(futures), total=len(arr)):
            results.append(f.result())
        return results
# END From fastai


def open_file(filepath, options):
    if filepath[-3:] == ".gz":
        return gzip.open(filepath, options)
    return open(filepath, options)


def chunk_of_text(_file, chunk_size):
    index = 0
    while True:
        line = _file.readline()
        if not line:
            break
        for sentence in line.split("."):
            if sentence.strip():
                yield sentence.strip()
        if index >= chunk_size:
            break
        index += 1


def num_cpus(n_cpus):
    try:
        return len(os.sched_getaffinity(0))
    except AttributeError:
        return os.cpu_count()
    if n_cpus > 0:
        return n_cpus
    """Get number of cpus."""
# end
