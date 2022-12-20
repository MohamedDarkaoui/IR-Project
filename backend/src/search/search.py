from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
es = Elasticsearch("https://localhost:9200", http_auth=("viktor", "viktor"), verify_certs=False)

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


def build_fuzzy_search(query, index, fuzziness=2):
    q = Q({
        "match": {
          "text": {
            "query": query,
            "fuzziness": fuzziness,
            "prefix_length": 1
          }
        }
    })
    s = Search(using=es, index=index).query(q)
    return s


def build_exact_search(query, index, match):
    s = Search(using=es, index=index).query(match, text=query)
    return s


def fuzzy_search(query, top_k, index, return_list=True, fuzziness=2):

    s = build_fuzzy_search(query, index, fuzziness).extra(from_=0, size=top_k)
    res = s.execute()
    res_list = res['hits']['hits']
    prompts = [result['_source']['text'] for result in res_list]
    if return_list:
        return prompts
    else:
        return res


def exact_search(query, top_k, index):

    match = "match_phrase"
    s = build_exact_search(query, index, match).extra(from_=0, size=top_k)

    res = s.execute()
    res_list = res['hits']['hits']
    prompts = [result['_source']['text'] for result in res_list]
    # for hit in res:
    #     print(hit.meta.score, hit.text, hit.anger, "\n", hit.links.split(','))
    return prompts


def search_by_emotions(query, top_k, emotions, fuzziness, index, sort_by=None):
    s = build_fuzzy_search(query, index, fuzziness)

    for emotion in emotions:
        arg = {emotion: emotions[emotion]}
        s = s.filter('range', **arg)
    if sort_by is not None:
        s = s.sort({sort_by: {"order": "desc"}})
    s = s.extra(from_=0, size=top_k)
    res = s.execute()
    return res
import json
import pprint
if __name__ == "__main__":
    results = search_by_emotions('clowns smoke weed', 12, em, 0, 'lexica2')
    results = [x for x in results]
    results = [x.to_dict() for x in results]

    results = json.dumps(results)
    pprint.pprint(json.loads(results))
    print("")
    # for hit in results:
    #     print(hit.meta.score, hit.text, hit.anger)
