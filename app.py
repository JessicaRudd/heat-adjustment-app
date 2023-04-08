import os
import requests
import threading
import time
from flask import Flask, render_template, request, jsonify
from heat_index_pace_adjustment import HeatIndexPaceAdjustment
from weather_data import WeatherData

app = Flask(__name__)
cache = {}
expiration_time = 24 * 60 * 60

def remove_expired_entries():
    while True:
        current_time = time.time()
        keys_to_remove = []

        for key, value in cache.items():
            location, date = key.split('-')
            timestamp = value[2]

            if current_time - timestamp > expiration_time:
                keys_to_remove.append(key)

        for key in keys_to_remove:
            del cache[key]
            
        time.sleep(60 * 60) # Sleep for an hour

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        # Get the user's location from the request body
        location = request.json['location']
        date = request.json['datetime']
        key = f"{location}-{date}"

        if key in cache:

            forecast_heat_index, pace_adjustment = cache[key][:2]

        else:

            # # Use the Google Maps API to geocode the location into a latitude and longitude
            # api_key = os.environ['GOOGLE_MAPS_API_KEY']
            # geocode_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={api_key}'
            # response = requests.get(geocode_url)
            # lat = response.json()['results'][0]['geometry']['location']['lat']
            # lon = response.json()['results'][0]['geometry']['location']['lng']

            # # Use the OpenWeatherMap API to get the current weather conditions and forecast for the location
            # api_key = os.environ['OPENWEATHERMAP_API_KEY']
            # weather_url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=current,minutely,daily,alerts&appid={api_key}&units=imperial'
            # response = requests.get(weather_url)
            w = WeatherData(location, date)
            forecast_heat_index, forecast_temp, forecast_humidity = w.get_weather_data()

            # Calculate the pace adjustment using the HeatIndexPaceAdjustment class
            is_elite_runner = request.json.get('is_elite_runner', False)  # default to non-elite runner
            h = HeatIndexPaceAdjustment(forecast_heat_index, is_elite_runner)
            pace_adjustment = h.pace_adjustment()

            cache[key] = (forecast_heat_index, pace_adjustment, time.time())

        # Return the pace adjustment to the user
        # return jsonify({'pace_adjustment': pace_adjustment, 'forecasted_heat_index': forecasted_heat_index})
        return render_template('index.html', location=location, date=date, temp=forecast_temp, humidity=forecast_humidity, heat_index=forecast_heat_index, pace_adjustment=pace_adjustment)
    
    return render_template('index.html')

if __name__ == '__main__':

    t = threading.Thread(target=remove_expired_entries)
    t.start()

    # Start Flask app
    app.run(debug=True)