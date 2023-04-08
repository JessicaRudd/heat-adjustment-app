import os
import requests


class WeatherData:

    """
    Uses Google Maps API to get geocoded location and then uses location to get weather forecast from openweathermap api
    """

    def __init__(self,location, date):
        """
        Initializes the HeatIndexPaceAdjustment object with the maximum temperature, humidity, and whether the runner is elite.

        :param max_temp: Maximum temperature in Celsius.
        :param humidity: Relative humidity as a percentage.
        :param is_elite: True if the runner is elite, False otherwise.
        """
        self.location = location
        self.date = date

     
    def _get_geocode_location(self):
        # Use the Google Maps API to geocode the location into a latitude and longitude
                api_key = os.environ['GOOGLE_MAPS_API_KEY']
                geocode_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={self.location}&key={api_key}'
                response = requests.get(geocode_url)
                lat = response.json()['results'][0]['geometry']['location']['lat']
                lon = response.json()['results'][0]['geometry']['location']['lng']
                
                return lat, lon
            

    def get_weather_data(self):
        api_key = os.environ.get("OPENWEATHER_API")

        lat, lon = self._get_geocode_location()
        dt = int(self.date.timestamp())
        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,daily&appid={api_key}&units=imperial"
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
            return None