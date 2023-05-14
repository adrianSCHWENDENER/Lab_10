import time
import serial
from Adafruit_IO import Client, Feed, Data, RequestError

espera = 0

# Configuración del puerto serial
PORT = 'COM6'
BAUD_RATE = 9600
ser = serial.Serial(PORT, BAUD_RATE)

# Valores de Adafruit
ADAFRUIT_IO_KEY = 'aio_Csss54OrDImVy5K0Kazj0ofFEDxy'
ADAFRUIT_IO_USERNAME = 'SCHadrian19'

# Crear una instancia para el REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Intentar conectar con el feed "Sensor1"
try:
    temperatura = aio.feeds('sensor1')
except RequestError:
    feed = Feed(name="temperatura")
    temperatura = aio.create_feed(feed)

# Intentar conectar con el feed "Sensor2"
try:
    luminosidad = aio.feeds('sensor2')
except RequestError:
    feed = Feed(name="luminosidad")
    luminosidad = aio.create_feed(feed)

while True:
    # Recibir datos de ADAFRUIT
    adafruit_data = aio.receive(luminosidad.key).value
    print(adafruit_data)
    
    # Enviar valores seriales
    ser.write(str(adafruit_data).encode())
    
    # Leer valores seriales
    while ser.in_waiting:
        serial_data = ser.read(1).decode()
        print(serial_data) 

        espera += 1
    
    # Mandar datos a ADAFRUIT
    if espera > 3:
        aio.send_data(temperatura.key, int(serial_data))
        espera = 0

    # Esperar 3 segundos antes de volver a repetir
    #time.sleep(3)
