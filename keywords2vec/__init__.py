import os
import gzip
from glob import glob
# from argparse import ArgumentParser
# from collections import Counter
from functools import partial
# from time import time  # To time our operations

from keywords2vec.utils import parallel, open_file, chunk_of_text
from keywords2vec.tokenizer import tokenize


# import gensim



def tokenize_text(
    input_path=None, output_path="tokenized.txt", sep="!", lang="en",
    sample_size=-1, lines_chunks=-1, n_cpus=-1
):
    tokenize_wrapper = partial(tokenize, lang=lang)

    os.environ["TOKENIZER_LANG"] = lang
    index = 0
    with gzip.open(output_path, "wt") as _output:
        for file_path in glob(input_path):
            print("processing file:", file_path)
            # We are going to split the text in chunks to show some progress.
            new_index, text_chunks, break_by_sample = get_file_chunks(index, file_path, lines_chunks, sample_size)
            index = new_index
            results = parallel(tokenize_wrapper, text_chunks, n_cpus)
            _output.write("\n".join(results) + "\n")
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


# def main():
#     parser = ArgumentParser()
#     parser.add_argument(
#         "-i", "--input-file", dest="input_filename",
#         required=True, help="the input text file", metavar="INPUT_FILE"
#     )
#     parser.add_argument(
#         "-o", "--output-directory", dest="experiment_path",
#         required=True, help="the target directory for the outputs",
#         metavar="DIRECTORY"
#     )
#     # parser.add_argument(
#     #     "-c", "--column-numbers", dest="column_numbers",
#     #     required=False, help="The text columns of the file. Allowed multiple, separed by comma (starting from 0)",
#     #     metavar="COLUM_NUMBERS", default="0", type=str
#     # )
#     # parser.add_argument(
#     #     "-d", "--delimiter", dest="delimiter", required=False,
#     #     help="the column delimiter", metavar="DELIMITER", default="\t"
#     # )
#     # parser.add_argument(
#     #     "-n", "--name", dest="name",
#     #     required=False, help="name of the experiment",
#     #     metavar="NAME", default="experiment_1"
#     # )
#     parser.add_argument(
#         "-s", "--sample", dest="sample_size",
#         required=False,
#         help="if you wanted to process a sample of the lines. By default -1 (all)",
#         metavar="SIZE", default="-1", type=int
#     )
#     parser.add_argument(
#         "-v", "--verbose",
#         dest="verbose", default=True,
#         help="don't print status messages to stdout"
#     )
#     parser.add_argument(
#         "-l", "--lines-chunks", dest="lines_chunks",
#         required=False, help="size of the lines chunks, to use as progress update (-1 auto)",
#         metavar="LINES_CHUNKS", default="-1", type=int
#     )
#     # parser.add_argument(
#     #     "-a", "--additional-stopwords", dest="additional_stopwords",
#     #     required=False,
#     #     help="Stopwords must be separated by comma",
#     #     metavar="STOPWORDS", default="", type=str
#     # )
#     parser.add_argument(
#         "--word2vec_size", dest="word2vec_size",
#         required=False,
#         help="Word2vec vector size",
#         metavar="WORD2VEC_SIZE", default="300", type=int
#     )
#     parser.add_argument(
#         "--lang", dest="lang",
#         required=False,
#         help="Language",
#         metavar="lang", default="en", type=str
#     )
#     parser.add_argument(
#         "--word2vec_window", dest="word2vec_window",
#         required=False,
#         help="Word2vec window size",
#         metavar="WORD2VEC_WINDOW", default="3", type=int
#     )
#     parser.add_argument(
#         "--word2vec_count", dest="word2vec_count",
#         required=False,
#         help="Word2vec min keyword count",
#         metavar="WORD2VEC_MIN_COUNT", default="3", type=int
#     )
#     parser.add_argument(
#         "--word2vec_epochs", dest="word2vec_epochs",
#         required=False,
#         help="Word2vec epochs number",
#         metavar="WORD2VEC_EPOCHS", default="10", type=int
#     )
#     parser.add_argument(
#         "--workers", dest="workers",
#         required=False,
#         help="Total numbers of CPU workers",
#         metavar="CPU_WORKERS", default="-1", type=int
#     )
#     parser.add_argument(
#         "--tokenize-only", dest="tokenize_only",
#         required=False,
#         help="If you wanted to only tokenize the text",
#         action='store_true'
#     )

#     args = parser.parse_args()
#     if not os.path.exists(args.experiment_path):
#         os.makedirs(args.experiment_path)
#     if args.workers < 0:
#         args.workers = num_cpus()
#     if args.lines_chunks == -1:
#         if args.sample_size > 8000:
#             args.lines_chunks = args.sample_size / (30 * args.workers)
#         else:
#             args.lines_chunks = 500

#     step = 1
#     log("Step%s: Tokenizing" % step, args.verbose)
#     # tokenized_path = os.path.join(args.experiment_path, "tokenized.txt.gz")
#     # if not os.path.exists(tokenized_path):
#     tokenized_path = tokenize_text(args)
#     # else:
#     #     log("File already exists", args.verbose)
#     step += 1
#     if args.tokenize_only:
#         print("")
#         print("tokenized_path:", tokenized_path)
#         return

#     log("Step%s: Reading keywords" % step, args.verbose)
#     documents_keywords = read_documents(tokenized_path)
#     step += 1

#     log("Step%s: Calculate frequency" % step, args.verbose)
#     counter = calculate_keywords_frequency(documents_keywords)
#     step += 1

#     log("Step%s: Save counter" % step, args.verbose)
#     save_counter(counter, args)
#     step += 1

#     log("Step%s: Generate word2vec model" % step, args.verbose)
#     keywords_vectors = generate_word2vec_model(documents_keywords, args)
#     step += 1

#     log("Step%s: Save vectors" % step, args.verbose)
#     save_vectors(keywords_vectors, args)
#     step += 1





# def num_cpus():
#     """Get number of cpus."""
#     try:
#         return len(os.sched_getaffinity(0))
#     except AttributeError:
#         return os.cpu_count()
# # end


# def tokenize_text(args):
#     """We try to separate the text, according to the following rules.
#     We are goint to use the stopwords to separate the different expression,
#     and in that way identify keywords, as an alternative to use ngrams.
#     Example (! is used as separator of the keywords):
#         - input: "Timing of replacement therapy for acute renal failure after cardiac surgery"
#         - output: "timing!replacement therapy!acute renal failure!cardiac surgery"
#     Another example:
#         - input: "Acute renal failure (ARF) following cardiac surgery remains a significant cause of mortality. The aim of this study is to compare early and intensive use of continuous veno-venous hemodiafiltration (CVVHDF) with conservative usage of CVVHDF in patients with ARF after cardiac surgery."
#         - output: "acute renal failure!arf!following cardiac surgery remains!significant cause!mortality!aim!study!compare early!intensive!continuous veno-venous hemodiafiltration!cvvhdf!conservative usage!cvvhdf!patients!arf!cardiac surgery"
#     """
#     if not args.__contains__("tokenized_path"):
#         tokenized_path = os.path.join(args.experiment_path, "tokenized.txt.gz")
#     else:
#         tokenized_path = args.tokenized_path
#     os.environ["TOKENIZER_LANG"] = args.lang
#     index = 0
#     with gzip.open(tokenized_path, "wt") as _output:
#         for file_path in glob(args.input_filename):
#             print("processing file:", file_path)
#             # We are going to split the text in chunks to show some progress.
#             new_index, text_chunks, break_by_sample = get_file_chunks(index, file_path, args.lines_chunks, args)
#             index = new_index
#             results = parallel(tokenize_chunk, text_chunks, args.workers)
#             # results = []
#             # for text_chunk in text_chunks:
#             #     text_ = tokenize_chunk(text_chunk, 0)
#             #     results.append(text_)

#             _output.write("\n".join(results) + "\n")
#             if break_by_sample:
#                 break

#     return tokenized_path











# def log(line, verbose=True, inline=False):
#     end = "\n"
#     if verbose:
#         if inline:
#             end = "\r"
#         print(line, end=end)


# # Read tokenized data
# def read_documents(tokenized_path):
#     documents_keywords = []
#     index = 0
#     for line in open_file(tokenized_path, "rt"):
#         documents_keywords.append(line[0:-1].split("!"))
#         index += 1
#     return documents_keywords


# # Calculate words frequency
# def calculate_keywords_frequency(documents_keywords):
#     return Counter([
#         keyword
#         for keywords in documents_keywords
#         for keyword in keywords
#     ])


# def generate_word2vec_model(documents_keywords, args):
#     total_documents = len(documents_keywords)
#     model = gensim.models.Word2Vec(
#         documents_keywords, size=args.word2vec_size, window=args.word2vec_window,
#         min_count=args.word2vec_count, workers=args.workers
#     )
#     if args.verbose:
#         import logging
#         t = time()

#         logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt='%H:%M:%S', level=logging.INFO)

#     model.train(
#         documents_keywords,
#         total_examples=total_documents,
#         epochs=args.word2vec_epochs,
#         report_delay=1
#     )
#     if args.verbose:
#         print('Time to train the model: {} mins'.format(round((time() - t) / 60, 2)))
#     return model.wv


# # Save the vectors
# def save_vectors(keywords_vectors, args):
#     store_model_path = os.path.join(args.experiment_path, "word2vec.vec")
#     keywords_vectors.save(store_model_path)
#     return store_model_path


# def save_counter(counter, args):
#     counter_store_path = os.path.join(args.experiment_path, "keywords_counter.tsv.gz")
#     with gzip.open(counter_store_path, 'wt') as _file:
#         for term, total in counter.most_common():
#             _file.write("%s\t%s\n" % (term, total))
#     return counter_store_path

# if __name__ == '__main__':
#     main()
