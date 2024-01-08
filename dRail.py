import pytz
import requests
from datetime import datetime, timedelta

ROOT_URL = "https://api.irail.be/"
TZ = pytz.timezone('Europe/Brussels')

liveboard_station = "Schaerbeek"
liveboard_time = datetime.now(TZ) + timedelta(minutes=30)

def query_liveboard(station, response_format, lang, alerts, time):
    """
    Query the liveboard API for train departure information.
    
    :param station: The station to query.
    :param response_format: The response format (e.g., 'json').
    :param lang: The response language.
    :param alerts: Whether to include alerts.
    :param time: The time to query for.
    :return: The API response.
    """
    api_url = f"{ROOT_URL}liveboard"
    try:
        response = requests.get(api_url, params={
            'station': station, 
            'format': response_format, 
            'lang': lang, 
            'alerts': alerts,
            'time': time.strftime("%H%M")
        })
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error querying the liveboard API: {e}")
        return None

liveboard = query_liveboard(liveboard_station, "json", "en", "true", liveboard_time)

if liveboard:
    print(f"{'Time (Delay)':<22} {'Station':<25} {'Platform':<}")
    print("===========================================================")

    departures = liveboard['departures']
    for departure in departures['departure']:
        departure_time = datetime.fromtimestamp(int(departure['time']), tz=TZ)
        departure_delay = f"(+{int(departure['delay']) // 60})"
        departure_platform = departure['platform']

        print(f"{departure_time.strftime('%H:%M')} {departure_delay:<15}  {departure['station']:<25} {departure_platform:>6}")

    print("===========================================================")
