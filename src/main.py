from statistics import mean
import time
import Adafruit_DHT  # Install via `pip install Adafruit_DHT`
import requests

# Constants
SENSOR_TYPE = Adafruit_DHT.DHT22
PIN1 = 7  # GPIO pin connected to the sensor
PIN2 = 11  # GPIO pin connected to the sensor
TEMP_THRESHOLD = 0.0  # Example temperature threshold in Celsius
TIME_THRESHOLD = 1.0  # Example temperature threshold in Celsius
PUSHBULLET_TOKEN = 'your_pushbullet_access_token'

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
    humidity1, temperature1 = Adafruit_DHT.read_retry(SENSOR_TYPE, PIN1)
    humidity2, temperature2 = Adafruit_DHT.read_retry(SENSOR_TYPE, PIN2)
    if temperature1 and temperature2 is not None:
        return temperature1, temperature2
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
        temperature1, temperature2 = read_temperature()
        console.log(f"Temperature 1: {temperature1:.2f}°C, Temperature 2: {temperature2:.2f}°C")
        if (temperature1 > TEMP_THRESHOLD) or (temperature2 > TEMP_THRESHOLD):
            avg_current_temp = mean(temperature1, temperature2)
            max_temp = max(temperature1, temperature2)
            start_time = time.time()
            duration += 1
            # notification needs to be separate from loop and if logic? Otherwise static values (like start_time) will be constantly overwritten
            send_notification(f"Stove has been on since {start_time - 30*60} for at least {TIME_THRESHOLD + duration} minutes! Average current temperature {avg_current_temp:.2f}°C | Max temp reached: {max_temp:.2f}°C")

        if (temperature1 < TEMP_THRESHOLD) and (temperature2 < TEMP_THRESHOLD):
            min_temp = min(temperature1, temperature2)
        # time.sleep(60)  # Check every 60 seconds

if __name__ == "__main__":
    main()