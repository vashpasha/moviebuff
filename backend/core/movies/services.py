import requests
from django.conf import settings


def get_movie(movie_id):
    url = settings.OMDB_BASE_URL
    params = {
        'i': movie_id, 
        'apikey': settings.OMDB_API_KEY
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def search_movie(query):
    url = settings.OMDB_BASE_URL
    params = {
        'apikey': settings.OMDB_API_KEY,
        's': query,
        'type': 'movie'
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['Response'] == 'True':
            return data['Search']
    return None