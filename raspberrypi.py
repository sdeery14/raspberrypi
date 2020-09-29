from picamera import PiCamera
import time
import board
import adafruit_dht
import requests
from datetime import datetime
import pytz

camera = PiCamera()
camera.rotation = 180

dhtDevice = adafruit_dht.DHT22(board.D14)

camera.start_preview()
 
while True:
    try:
        camera.capture('image.jpg')
        temperature = dhtDevice.temperature * (9 / 5) + 32
        humidity = dhtDevice.humidity
        now = datetime.now(pytz.timezone('America/New_York'))
        sensor_reading = {
            "taken": now,
            "temp": temperature,
            "humidity": humidity
        }
        url = "https://seandeery-portfolio-api.com/sensor_readings/"

        try:
            response = requests.post(url, data = sensor_reading, files = {'image': open('image.jpg', 'rb')})
            return response
        except Exception as error:
            raise error
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)

camera.stop_preview()
