from statistics import mean
from enum import Enum
import time
import Adafruit_DHT  # Install via `pip install Adafruit_DHT`
import requests


class SensorType(Enum):
    DHT11 = Adafruit_DHT.DHT11
    DHT22 = Adafruit_DHT.DHT22
    AM2302 = Adafruit_DHT.AM2302

# Constants
SENSOR_TYPE = SensorType.DHT22.value
SENSOR1 = 2 # GPIO pin connected to the sensor
SENSOR2 = 3 # GPIO pin connected to the sensor
TEMP_THRESHOLD = 40.0  # Example temperature threshold in Celsius
TIME_THRESHOLD = 1.0  # Example temperature threshold in Celsius
PUSHBULLET_TOKEN = 'your_pushbullet_access_token'


# Make separate classes for each part of this except for the main script
def send_notification(message):
    """Send a notification to your phone using Pushbullet."""
    url = 'https://api.pushbullet.com/v2/pushes'
    headers = {
        'Access-Token': PUSHBULLET_TOKEN,
        'Content-Type': 'application/json'
    }
    data = {
        'type': 'note',
        'title': 'Temperature Alert',
        'body': message
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print("Notification sent!")
    else:
        print(f"Failed to send notification: {response.status_code}")

def read_temperature():
    """Read temperature from the sensor."""

    sensorArray = [SENSOR1, SENSOR2]
    resultList = []

    for i in range(len(sensorArray)):
        (humidity, temperature) = Adafruit_DHT.read_retry(SENSOR_TYPE, sensorArray[i])

        if humidity is not None and temperature is not None:
            resultList.append({
                "sensor": sensorArray[i],
                "humidity": humidity,
                "temperature": temperature
            })
        else:
            print(f"Failed to read from sensor {sensorArray[i]}.")

    if resultList: # len(resultList) > 0: # uncommented solution takes advantage of python's truthy evaluation for lists
        return resultList
    else:
        print("Failed to read temperature. Retrying...")
        return None

def main():
    max_temp = 0
    avg_current_temp = 0
    min_temp = 0
    start_time = 0
    duration = 0
    while True:
        resultList = read_temperature()
        for i in range(len(resultList)):
            print(f"Sensor: {resultList[i]["sensor"]}, Temperature: {resultList[i]["temperature"]:.2f}°C, Humidity: {resultList[i]["humidity"]:.2f}%")

        # if (temperature1 > TEMP_THRESHOLD) or (temperature2 > TEMP_THRESHOLD):
        #     avg_current_temp = mean(temperature1, temperature2)
        #     max_temp = max(temperature1, temperature2)
        #     start_time = time.time()
        #     duration += 1
        #     # notification needs to be separate from loop and if logic? Otherwise static values (like start_time) will be constantly overwritten
        #     # send_notification(f"Stove has been on since {start_time - 30*60} for at least {TIME_THRESHOLD + duration} minutes! Average current temperature {avg_current_temp:.2f}°C | Max temp reached: {max_temp:.2f}°C")
        #     printf(f"Stove has been on since {start_time - 30*60} for at least {TIME_THRESHOLD + duration} minutes! Average current temperature {avg_current_temp:.2f}°C | Max temp reached: {max_temp:.2f}°C")

        # if (temperature1 < TEMP_THRESHOLD) and (temperature2 < TEMP_THRESHOLD):
        #     min_temp = min(temperature1, temperature2)
        # time.sleep(60)  # Check every 60 seconds

if __name__ == "__main__":
    main()