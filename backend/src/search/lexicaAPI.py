import requests


def lexicaSearch(query):
    url = 'https://lexica.art/api/v1/search?q='+query
    response = requests.get(url)
    prompts = []
    if response.status_code == 200:
        data = response.json()
        for image in data['images']:
            prompt = image['prompt']
            prompts.append(prompt)
    return prompts

