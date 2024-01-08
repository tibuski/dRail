import requests
import json

ROOT_URL= "https://api.irail.be/"

def query_stations(response_format,response_lang):
    
    API_URL = ROOT_URL + "stations"
    
    query_result = requests.get(API_URL, params={'format': response_format, 'lang': response_lang})

    return(query_result)

def query_liveboard(what_to_query,response_format,response_lang,alerts_bool):
    
    API_URL = ROOT_URL + "liveboard"
    
    query_result = requests.get(API_URL, params={'station': what_to_query, 'format': response_format, 'lang': response_lang, 'alerts': alerts_bool})

    return(query_result)

live_station = "Ath"
liveboard = (query_liveboard(live_station, "json", "fr", "true")).json()

for departure in liveboard['departures']:
    for idx in departure.len():
        print(departure[idx])
