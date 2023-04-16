import threading
import time
from datetime import datetime
from flask import Flask, render_template, request, make_response, redirect
from heat_index_pace_adjustment import HeatIndexPaceAdjustment
from weather_data import WeatherData
import os
import logging

logging.basicConfig(level=logging.INFO)
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

# @app.route('/', methods=['GET', 'POST'])

@app.route('/', methods=['GET','POST'])    
def index():

    if request.method == 'POST':

        # Get the user's location from the request body
        location = request.form['location']
        date = datetime.fromisoformat(request.form['datetime'])
        key = f"{location}-{date}"

        if key in cache:
            app.logger.info("Getting weather from cache")
            forecast_heat_index, pace_adjustment = cache[key][:2]

        else:
            app.logger.info("Getting new weather data")
            w = WeatherData(location, date)
            forecast_heat_index, forecast_temp, forecast_humidity, dew_point = w.get_weather_data()

            app.logger.info(f"Heat index = {forecast_heat_index}")
            app.logger.info(f"Forecast temp = {forecast_temp}")
            app.logger.info(f"Forecast humidity = {forecast_humidity}")
            app.logger.info(f"Forecast dew point = {dew_point}")

            # Calculate the pace adjustment using the HeatIndexPaceAdjustment class - may use later
            is_elite_runner = request.form.get('is_elite_runner', False)  # default to non-elite runner
            app.logger.info(f"Is Elite Runner? = {is_elite_runner}")

            h = HeatIndexPaceAdjustment(forecast_temp, dew_point, is_elite_runner)
            pace_adjustment = h.pace_adjustment()
            app.logger.info(f"Recommended pace adjustment = {pace_adjustment}")

            cache[key] = (forecast_temp, dew_point, time.time())

        return redirect('/result?pace_adjustment=' + str(pace_adjustment))
    else:
        return render_template('index.html')

@app.route('/result', methods=['GET','POST'])
def result():
    
    pace_adjustment = request.args.get('pace_adjustment')
    response = make_response(render_template('result.html', pace_adjustment=pace_adjustment))
    response.headers['Cache-Control'] = 'no-cache'
    return response

if __name__ == '__main__':

    t = threading.Thread(target=remove_expired_entries)
    t.start()

    # Start Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
