import pandas as pd
import time
from essential_generators import DocumentGenerator
from backend.src.search.search import fuzzy_search, exact_search
from backend.src.search.lexicaAPI import lexicaSearch


sample = pd.read_csv('backend/promptsSample.csv')
nrPrompts = 0
avgPrecision = 0

for index, row in sample.iterrows():
    generator = DocumentGenerator()
    query = row['text']
    print(query)
    lexicaResults = lexicaSearch(query)
    relevantResults = []
    for result in lexicaResults:
        r = exact_search(result, 10, "lexica2")
        if len(r) >= 1:
            relevantResults.append(r[0])
    k = 10
    nrRelevant = len(relevantResults)
    time.sleep(5)
    if nrRelevant == 0:
        continue
    newQuery = relevantResults[0]
    retrievedResults = fuzzy_search(newQuery, k, "lexica2")
    intersection = set()
    for res in relevantResults:
        if res in retrievedResults:
            intersection.add(res)
    precision = len(intersection) / k
    avgPrecision += precision
    nrPrompts += 1
    print(precision)
    time.sleep(5)

print("nrPrompts: ", nrPrompts)
avgPrecision /= nrPrompts
print("average precision: ", avgPrecision)



