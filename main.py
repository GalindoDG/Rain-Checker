# If you want to use this, you must provide your own keys for twilio, key for open weather map, and to/from phone numbers

import requests
import os
from twilio.rest import Client

# Twilio API for SMS
account_sid = "AC5f8c05efd29e2379eaf8ceb929d59568"
auth_token = "YOUR TWILIO AUTH TOKEN"

# Open Weather Map API
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = "YOUR OWM KEY"

MY_LAT = 33.771709
MY_LONG = -118.181313

weather_params = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": api_key,
    "exclude": "current,minutely,daily",
    "units": "imperial",
}

response = requests.get(OWM_Endpoint, weather_params)
response.raise_for_status()
weather_data = response.json()

will_rain = False

# Slices the hourly weather data for first 12 hours of the JSON data pulled, this is a list
weather_slice = weather_data["hourly"][:12]

# This pulls the weather 'id' code for the sliced list, the id tells us the weather condition
for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

# if we get a rainy weather id, twilio app sends us a text
if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It's going to rain. Bring an umbrella dummy.",
        from_='YOUR FROM NUMBER',
        to='YOUR TO NUMBER'
    )

    print(message.status)



