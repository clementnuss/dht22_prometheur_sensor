import logging
import time
import board
import adafruit_dht
from prometheus_client import Gauge

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D4)

def dht_reading_loop(temperature: Gauge, humidity: Gauge):

    while True:
        try:
            temperature_c = dhtDevice.temperature
            humidity_pcnt = dhtDevice.humidity
            logging.debug(f"Temp: {temperature_c:.1f} C    Humidity: {humidity_pcnt}%")

            temperature.set(temperature_c)
            humidity.set(humidity_pcnt)

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            logging.error(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error

        time.sleep(2.0)
