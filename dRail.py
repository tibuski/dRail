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
    
@app.route('/text/<station>', methods=['GET'])
def text_liveboard(station):
    liveboard_time = datetime.now(TZ)
    liveboard = query_liveboard(station, "json", "en", "true", liveboard_time)

    if liveboard and 'departures' in liveboard and 'departure' in liveboard['departures']:
        departures = liveboard['departures']['departure']

        # Determine the maximum width of each column
        max_station_length = max(len(d['stationinfo']['name']) for d in departures)
        max_platform_length = max(len(d['platform']) for d in departures)

        response_text = f"Liveboard Departures from {station.title()}:\n\n"
        header = f"{'Time (Delay)':15} {'Station':<{max_station_length}} {'Platform':^{max_platform_length}}\n"
        response_text += header
        response_text += '-' * len(header) + '\n'

        # ANSI color code for red
        red_start = "\033[91m"
        color_end = "\033[0m"

        for d in departures:
            time_str = datetime.fromtimestamp(int(d['time']), tz=TZ).strftime('%H:%M')
            delay = int(d['delay'])
            delay_str = f"{red_start}(+{delay // 60}){color_end}" if delay > 0 else ""
            time_delay_str = f"{time_str} {delay_str}".ljust(15)
            station_str = d['stationinfo']['name'].ljust(max_station_length)
            platform_str = d['platform'].center(max_platform_length)
            response_text += f"{time_delay_str} {station_str} {platform_str}\n"

        return response_text
    else:
        return "Error or no departures available for this station."


if __name__ == '__main__':
    app.run(debug=True)
