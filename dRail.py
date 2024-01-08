from flask import Flask, render_template, request
import pytz
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

ROOT_URL = "https://api.irail.be/"
TZ = pytz.timezone('Europe/Brussels')

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

@app.template_filter('format_time')
def format_time(timestamp):
    """
    Format a UNIX timestamp into a human-readable format.
    
    :param timestamp: The UNIX timestamp.
    :return: Formatted time string.
    """
    return datetime.fromtimestamp(int(timestamp), tz=TZ).strftime('%H:%M')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        liveboard_station = request.form.get('station')
    else:
        liveboard_station = "Schaerbeek"  # Default station

    liveboard_time = datetime.now(TZ) + timedelta(minutes=30)
    liveboard = query_liveboard(liveboard_station, "json", "en", "true", liveboard_time)

    if liveboard:
        return render_template('liveboard.html', departures=liveboard['departures']['departure'], station=liveboard_station)
    else:
        return "<p>Error fetching liveboard data.</p>"

if __name__ == '__main__':
    app.run(debug=True)
