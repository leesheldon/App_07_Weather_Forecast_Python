import os
import requests

API_KEY = os.getenv("Python_Weather_API_KEY")


def get_data(place, forecast_days=None):
    # To get temperature in Celsius --> &units=metric
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={place}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    filtered_data = data["list"]

    # It is 8. Because we are using 5 Day / 3-Hour Forecast API.
    # It forecast with a 3-hour step. 24 hours / 3 = 8
    nr_values = 8 * forecast_days

    filtered_data = filtered_data[:nr_values]

    return filtered_data


if __name__ == "__main__":
    print(get_data(place="Berlin", forecast_days=3))
