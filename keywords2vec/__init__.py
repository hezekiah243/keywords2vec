import os
import gzip
from glob import glob
# from argparse import ArgumentParser
# from collections import Counter
from functools import partial
# from time import time  # To time our operations

import fasttext

from keywords2vec.utils import parallel, open_file, chunk_of_text
from keywords2vec.tokenizer import tokenize


# import gensim


def tokenize_file(
    input_path, output_path="tokenized.tx", lang="en",
    sample_size=-1, lines_chunks=-1, n_cpus=-1
):
    tokenize_wrapper = partial(tokenize, lang=lang, text_output=True)

    index = 0

    with open(output_path, "wt") as _output:
        for file_path in glob(input_path):
            print("processing file:", file_path)
            # We are going to split the text in chunks to show some progress.
            new_index, text_chunks, break_by_sample = get_file_chunks(index, file_path, lines_chunks, sample_size)
            index = new_index
            results = parallel(tokenize_wrapper, text_chunks, n_cpus)
            _output.write(
                ("\n".join(results) + "\n").replace(" ", "_").replace("!", " ")
            )
            if break_by_sample:
                break
    return output_path

# #tokenize_text(path=,text=,output="",lang=,sample_size=,lines_chunks=,n_cpus=-1)
# #generate_vectors(tokenized_path, sep=" ", vector_size, min_count, epochs, n_cpus= )


def get_file_chunks(start_index, filepath, lines_chunk, sample_size):
    _file = open_file(filepath, 'rt')
    texts = []
    break_by_sample = False
    while True:
        next_n_lines = list(chunk_of_text(_file, lines_chunk))
        texts.append("\n".join(next_n_lines) + "\n")
        if not next_n_lines:
            break
        start_index += lines_chunk
        if sample_size > 0 and start_index >= sample_size:
            break_by_sample = True
            break
    _file.close()
    return (start_index, texts, break_by_sample)


def train_model(input_filename):
    model = fasttext.train_unsupervised(input_filename, model='skipgram', maxn=0, dim=100, ws=5)
    return model
