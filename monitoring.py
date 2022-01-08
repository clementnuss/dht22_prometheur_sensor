
from prometheus_client import Gauge, start_http_server, REGISTRY
import logging
import threading

from dht_reader import dht_reading_loop


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # unregister the default collectors. source: https://github.com/prometheus/client_python/issues/414
    for coll in list(REGISTRY._collector_to_names.keys()):
        REGISTRY.unregister(coll)
    
    temperature = Gauge(name='temperature', documentation='The temperature (C) returned by the DHT22 sensor')
    humidity = Gauge(name='humidity', documentation='The humidity percentage returned by the DHT22 sensor')

    temp_thread = threading.Thread(
        target=dht_reading_loop,
        args= (temperature, humidity, ))
    logging.info(f"starting the temperature reading thread.")
    temp_thread.start()
 
    start_http_server(port=9100)
