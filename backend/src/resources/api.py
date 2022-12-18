from flask_restful import Resource, reqparse
from flask import request
from backend.src.search.search import search_by_emotions, fuzzy_search
import json

em = {
    "admiration": {'gte': 0, 'lte': 1},
    "amusement": {'gte': 0, 'lte': 1},
    "anger": {'gte': 0.1, 'lte': 1},
    "annoyance": {'gte': 0, 'lte': 1},
    "approval": {'gte': 0, 'lte': 1},
    "caring": {'gte': 0, 'lte': 1},
    "confusion": {'gte': 0, 'lte': 1},
    "curiosity": {'gte': 0, 'lte': 1},
    "desire": {'gte': 0, 'lte': 1},
    "disappointment": {'gte': 0, 'lte': 1},
    "disapproval": {'gte': 0, 'lte': 1},
    "disgust": {'gte': 0, 'lte': 1},
    "embarrassment": {'gte': 0, 'lte': 1},
    "excitement": {'gte': 0, 'lte': 1},
    "fear": {'gte': 0, 'lte': 1},
    "gratitude": {'gte': 0, 'lte': 1},
    "grief": {'gte': 0, 'lte': 1},
    "joy": {'gte': 0, 'lte': 1},
    "love": {'gte': 0, 'lte': 1},
    "nervousness": {'gte': 0, 'lte': 1},
    "optimism": {'gte': 0, 'lte': 1},
    "pride": {'gte': 0, 'lte': 1},
    "realization": {'gte': 0, 'lte': 1},
    "relief": {'gte': 0, 'lte': 1},
    "remorse": {'gte': 0, 'lte': 1},
    "sadness": {'gte': 0, 'lte': 1},
    "surprise": {'gte': 0, 'lte': 1},
    "neutral": {'gte': 0, 'lte': 1}
}
"""
    - Search by prompt                                      SearchByPrompt
    - Search by prompt and emotion order by emotion         SearchByEmotionOrdered
    - Search by prompt and emotion (not order)              SearchByEmotionUnordered
"""
def init(api):
    api.add_resource(SearchByPrompt, "/api/normalsearch")
    #api.add_resource(SearchByEmotionOrdered, "/api/emotionsearch")



class SearchByPrompt(Resource):
    def get(self):
        """
        Search by prompt
        ---
        description: "Search relevant prompts and corresponding images only by prompts"
        parameters:
          - in: query
            name: query
            description: prompt that you want to search
        responses:
          200:
            description: Accepted
        """

        query = request.args.get('query')
        fuzziness = 2
        res = fuzzy_search(query, 10, 'lexica2', False, fuzziness)
        results = [x for x in res]
        results = [x.to_dict() for x in results]
        results = json.dumps(results)
        return results, 200


class SearchByEmotionOrdered(Resource):
    def get(self):
        """
        Search by prompt
        ---
        description: "Search relevant prompts and corresponding images only by prompts"
        parameters:
          - in: query
            name: query
            description: prompt that you want to search
        responses:
          200:
            description: Accepted
        """

        query = request.args.get('query')
        emotion = request.args.get('emotion')
        sort_by = request.args.get('sort_by')
        res = search_by_emotions(query, 10, em, 2, 'lexica2', emotion)
        results = [x for x in res]
        results = [x.to_dict() for x in results]
        results = json.dumps(results)
        return results, 200