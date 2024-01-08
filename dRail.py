
import pytz
import requests
from datetime import datetime, timedelta

ROOT_URL = "https://api.irail.be/"
TZ = pytz.timezone('Europe/Brussels')

def query_liveboard(what_to_query,response_format,response_lang,alerts_bool,time_to_query):
    
    API_URL = ROOT_URL + "liveboard"
    
    query_result = requests.get(
        API_URL,
        params={
            'station': what_to_query, 
            'format': response_format, 
            'lang': response_lang, 
            'alerts': alerts_bool,
            'time': time_to_query
            }
        )

    return(query_result)

live_station = "Schaerbeek"
# Current time + 30 minutes
liveboardTime = (datetime.now() + timedelta(minutes=30)).strftime("%H%M")

liveboard = (query_liveboard(live_station, "json", "en", "true", liveboardTime)).json()
departures = liveboard['departures']


print(f"{'Time (Delay)' :<22} {'Station' :<25} {'Platform' :<}")
print("===========================================================")

for idx in departures['departure']:
    
    departureTime = datetime.fromtimestamp(int(idx['time']),tz=TZ)
    departureDelay = "(+"+str(round(int((idx['delay']))/60))+")"
    departurePlatform = idx['platform']

    print(f"{departureTime.strftime('%H:%M')} {departureDelay:<15}  {idx['station']:<25} {departurePlatform:>6}")
print("===========================================================")