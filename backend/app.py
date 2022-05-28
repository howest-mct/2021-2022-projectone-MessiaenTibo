#region **** IMPORTS ****
import json
from flask_socketio import SocketIO, emit, send
from pkg_resources import require
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, date
import time
import threading
from RPi import GPIO
import adafruit_dht
import board
#endregion


#region **** INIT ****
# Start app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False, engineio_logger=False, ping_timeout=1)
CORS(app)

# Custom endpoint
endpoint = '/api/v1'

# OneWire (GPIO 4)
sensor_file_name = '/sys/bus/w1/devices/28-22cf61000900/w1_slave'

# MagnetContacts
MagnetContactOne = 18
MagnetContactTwo = 23
MagnetContactThree = 24
MagnetContactFour = 25

MagnetContactOneState = False
MagnetContactTwoState = False
MagnetContactThreeState = False
MagnetContactFourState = False

# Humidity sensor
dhtDevice = adafruit_dht.DHT11(board.D12, use_pulseio=False)

# Buzzer
Buzzer = 18

# Button
button = 5

# LedCircle
LedCircle = 26

# Water Flow Sensor
WaterFlowSensor = 21

#endregion



#region **** SETUP ****
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MagnetContactOne, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(MagnetContactTwo, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(MagnetContactThree, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(MagnetContactFour, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.add_event_detect(MagnetContactOne, GPIO.RISING, FindUser, bouncetime=200)
    GPIO.add_event_detect(MagnetContactTwo, GPIO.RISING, FindUser, bouncetime=200)
    GPIO.add_event_detect(MagnetContactThree, GPIO.RISING, FindUser, bouncetime=200)
    GPIO.add_event_detect(MagnetContactFour, GPIO.RISING, FindUser, bouncetime=200)
    # # print(DHTtemp)
    # print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(DHTtemp, DHThumidity))
    FindUser()


#region **** ROUTES ****
@app.route('/')
def hallo():
    print('start')
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

@app.route(endpoint + '/devices/', methods=['GET'])
def devices():
    if request.method == 'GET':
        data = DataRepository.read_Device()
        return jsonify(data), 200

@app.route(endpoint + '/historiek/', methods=['GET','POST'])
def historiek():
    if request.method == 'GET':
        data = DataRepository.read_Historiek()
        return jsonify(data), 200
    elif request.method == 'POST':
        pass


@app.route(endpoint + '/temperatuur/', methods=['GET','PUT'])
def temperatuur():
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass

@app.route(endpoint + "/history//", methods=['GET'])
def historiekId():
    if request.method == "GET":
        data = DataRepository.read_historyId()
        return jsonify(data), 200

#endregion





#region **** METHODS ****
# OneWire
def read_temperature():
    temperature = ''
    sensor_file = open(sensor_file_name,'r')
    for line in sensor_file:
        if 't=' in line: 
            temperature = line[29] + line[30] + "." + line[31]+ line[32]+ line[33]
    print(temperature)
    return temperature

def Write_WaterTemperature():
    temperature = read_temperature()
    DataRepository.update_temp(88,2,1, datetime.now() , str(temperature), "Ingelezen temperatuur")



# Humidity Sensor
def Read_Humidity():
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        #dhtDevice.exit()


# Water Flow Sensor


# Find User
def FindUser(x=0):
    SelectedMagnetContact = 0
    MagnetContactOneState = GPIO.input(MagnetContactOne)
    MagnetContactTwoState = GPIO.input(MagnetContactTwo)
    MagnetContactThreeState = GPIO.input(MagnetContactThree)
    MagnetContactFourState = GPIO.input(MagnetContactFour)
    if(((MagnetContactOneState ^ MagnetContactTwoState) ^ (MagnetContactThreeState ^ MagnetContactFourState)) & ((MagnetContactOneState & MagnetContactTwoState != 1) & (MagnetContactThreeState & MagnetContactFourState != 1))):
        if(MagnetContactOneState):
            SelectedMagnetContact = 1
        elif(MagnetContactTwoState):
            SelectedMagnetContact = 2
        elif(MagnetContactThreeState):
            SelectedMagnetContact = 3
        elif(MagnetContactFourState):
            SelectedMagnetContact = 4
        print("User {} is selected".format(SelectedMagnetContact))
        Read_data()
    else:
        if(MagnetContactOneState | MagnetContactTwoState | MagnetContactThreeState | MagnetContactFourState):
            print("There is only 1 user at the same time allowd!")
        else:
            print("There must be at least 1 selected user!")
        threading.Timer(1,FindUser).start()
    # print(MagnetContactOneState)
    # print(MagnetContactTwoState)
    # print(MagnetContactThreeState)
    # print(MagnetContactFourState)


# Requesting data
def Read_data():
    read_temperature()
    Read_Humidity()
    threading.Timer(10,Read_data).start()


#endregion



# START THE APP
if __name__ == '__main__':
    print("backend running")
    setup()
    socketio.run(app, debug=False, host='0.0.0.0')