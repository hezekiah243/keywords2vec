import sys

from collections import defaultdict

import fasttext
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from annoy import AnnoyIndex


tree = None
dim = None
all_keywords = []
all_keywords_index = {}


app = Flask(__name__)
CORS(app)
x_suggestions_per_keyword = 100
x_max_suggestions = 500


def prepare_input_keywords():
    raw_keywords = (request.args.get('k') or "").split(",")
    return [
        keyword.strip().replace(" ", "_").lower()
        for keyword in raw_keywords
    ]

def prepare_output_keywords(score_keywords):
    return [
        (keyword.replace("_", " ").lower(), score)
        for keyword, score in score_keywords
    ]


@app.route('/keywords/similars')
def get_suggestion():
    all_suggestions = defaultdict(lambda: defaultdict(float))
    keywords = prepare_input_keywords()
    for keyword in keywords:
        if keyword in all_keywords:
            for suggestion_index, score_0 in zip(*tree.get_nns_by_item(all_keywords_index[keyword], x_suggestions_per_keyword, include_distances=True)):
                suggestion = all_keywords[suggestion_index]
                score = 1 - score_0
                if suggestion not in keywords:
                    all_suggestions[suggestion]["max"] = max(score, all_suggestions[suggestion]["max"])
                    all_suggestions[suggestion]["sum"] += score

    return jsonify(
        prepare_output_keywords(
            sorted(list(all_suggestions.items()), key=lambda x: -x[1]["max"])
        )[0:x_max_suggestions]
    )


@app.route('/keywords/autocomplete')
def get_keywords_autocomplete():
    top_n = 25
    keyword = prepare_input_keywords()[0]
    found = 0
    found_keywords = []
    for index, keyword_in_all in enumerate(all_keywords):
        if keyword in keyword_in_all:
            found += 1
            found_keywords.append(keyword_in_all.replace("_", " "))

        if found > top_n:
            break
    return jsonify(found_keywords)

@app.route('/keywords/ping')
def get_ping():
    return jsonify({"message": "pong"})


@app.route('/')
def home():
    return send_from_directory('.', "index.html")

def load_trees():
    dim = int(open("tree_dim.txt").read())
    tree = AnnoyIndex(dim, 'angular')
    tree.load('tree.ann')
    labels = [label.rstrip("\r\n") for label in open("tree_labels.txt").readlines()]
    all_keywords_index = {}
    for i, label in enumerate(labels):
        all_keywords_index[label] = i
    return dim, tree, labels, all_keywords_index


def prepare_server():
    global tree
    global app
    global dim
    global all_keywords
    global all_keywords_index
    dim, tree, all_keywords, all_keywords_index = load_trees()

    return app

