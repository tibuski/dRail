from flask import Flask, render_template, request
import pytz
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

ROOT_URL = "https://api.irail.be/"
TZ = pytz.timezone('Europe/Brussels')
TIME_DELTA = 15

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

    liveboard_time = datetime.now(TZ) + timedelta(minutes=TIME_DELTA)
    liveboard = query_liveboard(liveboard_station, "json", "en", "true", liveboard_time)

    if liveboard:
        return render_template('liveboard.html', departures=liveboard['departures']['departure'], station=liveboard_station, timedelta=TIME_DELTA)
    else:
        return "<p>Error fetching liveboard data.</p>"
    
@app.route('/text/<station>', methods=['GET'])
def text_liveboard(station):
    liveboard_time = datetime.now(TZ)
    liveboard = query_liveboard(station, "json", "en", "true", liveboard_time)

    if liveboard and 'departures' in liveboard and 'departure' in liveboard['departures']:
        departures = liveboard['departures']['departure']

        # Calculate the maximum length for the station column
        max_station_length = int(max(len(d['stationinfo']['name']) for d in departures))+6
        platform_length = 8 # Fixed width for platform column
        delay_column_width = 3  # Fixed width for delay column
        time_column_lenght = 9  # Fixed width for time column
        print(max_station_length, platform_length)

        response_text = f"\n\nLiveboard Departures from {station.title()}:\n\n"
        header = f"{' Time':^{time_column_lenght}}{'Delay':^{delay_column_width}}{'Station':^{max_station_length}}{'Platform':^{platform_length}}\n"
        response_text += header
        response_text += '-' * len(header) + '\n'

        # ANSI color code for red
        red_start = "\033[91m"
        green_start = "\033[92m"
        color_end = "\033[0m"

        for d in departures:
            time_str = datetime.fromtimestamp(int(d['time']), tz=TZ).strftime('%H:%M')
            
            delay = int(d['delay']) // 60
            delay = f"{delay:>{delay_column_width}}"
            delay_str = f"{red_start}{delay}{color_end}" if int(delay) > 0 else f"{green_start}{delay}{color_end}"
                       
            station_str = d['stationinfo']['name']
            platform_str = d['platform']

            response_text += f"{time_str:^{time_column_lenght}}{delay_str}{station_str:^{max_station_length}}{platform_str:>{platform_length}}\n"

            print(response_text)

        return response_text
    else:
        return "Error or no departures available for this station."

# Rest of the Flask app remains the same...

if __name__ == '__main__':
    app.run(debug=True)
