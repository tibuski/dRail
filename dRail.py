import requests
import json

ROOT_URL= "https://api.irail.be/"

def query_irail(what_to_query,response_format,response_lang):
    # PAPERLESS CONSTANTS
    API_URL = ROOT_URL + what_to_query
    
    # Make a GET request to the API to retrieve documents with the specific tag
    query_result = requests.get(API_URL, params={'format': response_format, 'lang': response_lang})

    return(query_result)

stations = (query_irail("stations", "json", "fr")).json()

for id in stations['station']:
        print(id['name'])