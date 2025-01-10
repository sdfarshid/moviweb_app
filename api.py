import json
import requests
from exceptions.APIError import FetchingError
from config import OMD_API_KEY


def call_api(title):
    api_url = 'http://www.omdbapi.com/?apikey={}&t={}'.format(OMD_API_KEY, title)
    return requests.get(api_url)


def process_fetching_data_from_API(title) -> dict:

    response = call_api(title)
    if response.status_code == requests.codes.ok:
        result_data = response.json()
        if not isinstance(result_data, dict) or len(result_data) == 0:
            raise ValueError(f"Invalid data for the movie '{title}'.")
        return result_data
    else:
        raise FetchingError(f"Error {response.status_code}: {response.text}")


