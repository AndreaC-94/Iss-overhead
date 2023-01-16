import requests
from datetime import datetime
import time

MY_LAT = 37.389091
MY_LNG = -5.984459


# Checking the iss position
def iss_check():
    inner_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    inner_response.raise_for_status()
    return [float(inner_response.json()["iss_position"]["latitude"]),
            float(inner_response.json()["iss_position"]["longitude"])]


# Checking the sun position
parameters = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0
}

response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
sun_position = [int(response.json()["results"]["sunrise"].split("T")[1][:2]),
                int(response.json()["results"]["sunset"].split("T")[1][:2])]

# Check if it's night
hour = int(str(datetime.now()).split(" ")[1][:2])


def is_sun_up():
    if sun_position[0] <= hour <= sun_position[1]:
        return True
    return False


def iss_is_near():
    iss_position = iss_check()
    if abs(iss_position[0] - abs(MY_LAT)) <= 5 and abs(iss_position[1] - abs(MY_LNG)) <= 5:
        if not is_sun_up():
            print("Look in the sky, iss is right above you!!!")
        else:
            print("Iss is above you, but it's too hard to see with the sun up")
    else:
        print("The iss is too far away from you")


while True:
    iss_is_near()
    time.sleep(10)
