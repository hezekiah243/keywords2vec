import sys

from collections import defaultdict

import fasttext
from flask import Flask, request, jsonify


model = None

app = Flask(__name__)
x_suggestions_per_keyword = 100
x_max_suggestions = 500

def prepare_input_keywords():
    raw_keywords = (request.args.get('k') or "").split(",")
    return [
        keyword.replace(" ", "_").lower()
        for keyword in raw_keywords
    ]

def prepare_output_keywords(score_keywords):
    return [
        (keyword.replace("_", " ").lower(), score)
        for keyword, score in score_keywords
    ]


@app.route('/keywords/suggestions')
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

def load_model(model_path):
    global model
    global app
    model = fasttext.load_model(model_path)
    return app
