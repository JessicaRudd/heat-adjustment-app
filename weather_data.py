import os
import requests
from datetime import datetime
import time
import logging

logging.basicConfig(level=logging.INFO)

class WeatherData:

    """
    Uses Google Maps API to get geocoded location and then uses location to get weather forecast from openweathermap api
    """

    def __init__(self,location, date):
        """
        Initializes the HeatIndexPaceAdjustment object with the maximum temperature, humidity, and whether the runner is elite.

        :param location: Location as a string zip, address, city, coordinates
        :param date: iso format date string
        """
        self.location = location
        self.date = date

     
    def _get_geocode_location(self):
        # Use the Google Maps API to geocode the location into a latitude and longitude
                api_key = os.environ['GOOGLE_MAPS_API_KEY']
                geocode_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={self.location}&key={api_key}'
                response = requests.get(geocode_url)

                lat = response.json()['results'][0]["geometry"]["location"]["lat"]
                lon = response.json()['results'][0]["geometry"]["location"]["lng"]
                
                return lat, lon
            

    def get_weather_data(self):
        api_key = os.environ.get("OPENWEATHERMAP_API_KEY")
        lat, lon = self._get_geocode_location()
        # dt = time.mktime(datetime.strptime(self.date, "%Y-%m-%dT%H:%M:%S+%f").timetuple())
        dt = datetime.fromisoformat(str(self.date)).timetuple()
        dt = time.mktime(dt)

        url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=current,minutely,daily,alerts&appid={api_key}&units=imperial'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            hourly_data = data["hourly"]
            closest_time_diff = float("inf")
            closest_data = None
            for hourly_datum in hourly_data:
                hourly_dt = hourly_datum["dt"]
                time_diff = abs(dt - hourly_dt)
                if time_diff < closest_time_diff:
                    closest_time_diff = time_diff
                    closest_data = hourly_datum
            feels_like = closest_data["feels_like"]
            temp = closest_data["temp"]
            humidity = closest_data["humidity"]

            return feels_like, temp, humidity
        else:
            logging.info(f"API call failure. Response code {response.status_code}")
            return None, None, None
        
if __name__ == '__main__':

    import json
     
    w = WeatherData("Atlanta", "2023-04-17T21:11:21")
    # lat, lon = w._get_geocode_location()
    # print(lat, lon)

    feels_like, temp, humidity = w.get_weather_data()

    print(feels_like, temp, humidity)