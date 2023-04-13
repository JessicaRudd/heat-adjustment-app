import threading
import time
from datetime import datetime
from flask import Flask, render_template, request
from heat_index_pace_adjustment import HeatIndexPaceAdjustment
from weather_data import WeatherData
import os
import logging

logger = logging.root.getChild("app.py")

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
        location = request.form['location']
        date = datetime.fromisoformat(request.form['datetime'])
        key = f"{location}-{date}"

        if key in cache:

            forecast_heat_index, pace_adjustment = cache[key][:2]

        else:

            w = WeatherData(location, date)
            forecast_heat_index, forecast_temp, forecast_humidity = w.get_weather_data()

            logger.info(f"Heat index = {forecast_heat_index}")
            logger.info(f"Forecast temp = {forecast_temp}")
            logger.info(f"Forecast humidity = {forecast_humidity}")

            # Calculate the pace adjustment using the HeatIndexPaceAdjustment class
            is_elite_runner = request.form.get('is_elite_runner', False)  # default to non-elite runner
            logger.info(f"Is Elite Runner? = {is_elite_runner}")

            h = HeatIndexPaceAdjustment(forecast_heat_index, is_elite_runner)
            pace_adjustment = h.pace_adjustment()
            logger.info(f"Recommended pace adjustment = {pace_adjustment}")

            cache[key] = (forecast_heat_index, pace_adjustment, time.time())

        # Return the pace adjustment to the user
        # return jsonify({'pace_adjustment': pace_adjustment, 'forecasted_heat_index': forecasted_heat_index})
        return render_template('index.html', location=location, date=date, temp=int(forecast_temp), humidity=forecast_humidity, heat_index=forecast_heat_index, pace_adjustment=pace_adjustment)
    
    return render_template('index.html')

if __name__ == '__main__':

    t = threading.Thread(target=remove_expired_entries)
    t.start()

    # Start Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
