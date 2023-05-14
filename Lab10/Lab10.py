import time
import sys
from Adafruit_IO import Client, MQTTClient, Feed

ADAFRUIT_IO_KEY = 'aio_Csss54OrDImVy5K0Kazj0ofFEDxy'
ADAFRUIT_IO_USERNAME = 'SCHadrian19'
FEED_ID = 'sensor1'

def connected(client):
    print('Subscribing to Feed {0}'.format(FEED_ID))
    client.subscribe(FEED_ID)

def disconnected(client):
    sys.exit(1)

def message(client, feed_id, payload):
    print('Feed {0} received new value: {1}'.format(feed_id, payload))

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

try:
    sensor_feed = aio.feeds('sensor2')
except:
    sensor_feed = Feed(name='sensor2')
    sensor_feed = aio.create_feed(sensor_feed)

run_count = 0

client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message

client.connect()

while True:
    print('sending count: ', run_count)
    run_count += 1
    aio.send_data('sensor2', run_count)
    time.sleep(3)
    client.loop()
    