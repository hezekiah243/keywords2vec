import sys

from collections import defaultdict

import fasttext
from flask import Flask, request, jsonify, send_from_directory
from whoosh.index import open_dir
from whoosh.qparser import QueryParser


model = None
ix = None

app = Flask(__name__)
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
        if keyword in model:
            for (score, suggestion) in model.get_nearest_neighbors(keyword, x_suggestions_per_keyword):
                if suggestion not in keywords:
                    all_suggestions[suggestion]["max"] = max(score, all_suggestions[suggestion]["max"])
                    all_suggestions[suggestion]["sum"] += score

    return jsonify(
        prepare_output_keywords(
            sorted(list(all_suggestions.items()), key=lambda x: -x[1]["max"])
        )[0:x_max_suggestions]
    )

def load_index(index_path):
    ix = open_dir(index_path, readonly=True)
    return ix

@app.route('/keywords/autocomplete')
def get_keywords_autocomplete():
    top_n = 25
    keyword = prepare_input_keywords()[0]
    with ix.searcher() as searcher:
        query = QueryParser("label", ix.schema).parse(keyword)
        results = searcher.search(query, limit=top_n, sortedby="pos")
        return jsonify([result.get("label").replace("_", " ") for result in results])

@app.route('/')
def home():
    return send_from_directory('.', "index.html")

def prepare_server(model_path, index_path):
    global model
    global app
    global ix
    ix = load_index(index_path)
    model = fasttext.load_model(model_path)
    return app

