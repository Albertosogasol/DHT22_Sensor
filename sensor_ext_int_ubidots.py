#Este código sirve para enviar la información tanto a UbiDots como a Thinkspeak

#Importacion de librerías
import sys
from urllib.request import urlopen 
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import requests

# Write API Key ThingSpeak.com
miWriteAPIKey_int = "YourAPIKey"
miWriteAPIKey_ext = "YourAPIKey"

#Ubidots Token
TOKEN="YourToken"
DEVICE_LABEL="Sensor_DHT22"

# Número GPIO de conexión del sensor dht22 a RaspberryPi
raspiNumGPIO_int = "22"
raspiNumGPIO_ext = "17"

#FUNCIONES PRINCIPALES
def getSensorData_int():
   RH, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, raspiNumGPIO_int)
   return ("{:.2f}".format(RH), "{:.2f}".format(T))
   
def getSensorData_ext():
   RH, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, raspiNumGPIO_ext)
   return ("{:.2f}".format(RH), "{:.2f}".format(T))

def getSensorData_Double():
    RH_int, T_int = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, raspiNumGPIO_int)
    RH_ext, T_ext = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, raspiNumGPIO_ext)
    return (float("{:.2f}".format(RH_int)), float("{:.2f}".format(T_int)), float("{:.2f}".format(RH_ext)), float("{:.2f}".format(T_ext)))

def build_payload(variable_1, variable_2, variable_3, variable_4):
    value_1,value_2, value_3, value_4 = getSensorData_Double()
    payload = {variable_1: value_1,
             variable_2: value_2,
             variable_3: value_3,
             variable_4: value_4}
    return payload

def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True

def main():
   print('Iniciando...')
   baseURL_int = 'https://api.thingspeak.com/update?api_key=%s' % miWriteAPIKey_int
   baseURL_ext = 'https://api.thingspeak.com/update?api_key=%s' % miWriteAPIKey_ext
   while True:
       try:     
           #Lectura sensor interior
           #RH_int, T_int = getSensorData_int()
           #f_int = urlopen(baseURL_int + "&field1=%s&field2=%s" % (RH_int, T_int))
           #f_int.close()
           #time.sleep(2)
           #Lectura sensor exterior
           #RH_ext, T_ext = getSensorData_ext()
           #f_ext = urlopen(baseURL_ext + "&field1=%s&field2=%s" % (RH_ext, T_ext))
           #f_ext.close()
           #Lectura UbiDots
           payload = build_payload("Humedad_Interior", "Temperatura_Interior", "Humedad_Exterior", "Temperatura_Exterior")
           post_request(payload)
           sleep(5)
       except:
           print('Terminado.')
           break
if __name__ == '__main__':
    main()