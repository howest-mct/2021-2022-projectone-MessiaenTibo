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

SelectedMagnetContact = 0

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
start_counter = 0
WaterFlowPulsen = 0

#endregion



#region **** SETUP ****
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MagnetContactOne, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(MagnetContactTwo, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(MagnetContactThree, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(MagnetContactFour, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(WaterFlowSensor, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.add_event_detect(MagnetContactOne, GPIO.BOTH, FindUser, bouncetime=200)
    GPIO.add_event_detect(MagnetContactTwo, GPIO.BOTH, FindUser, bouncetime=200)
    GPIO.add_event_detect(MagnetContactThree, GPIO.BOTH, FindUser, bouncetime=200)
    GPIO.add_event_detect(MagnetContactFour, GPIO.BOTH, FindUser, bouncetime=200)
    GPIO.add_event_detect(WaterFlowSensor, GPIO.FALLING, callback=countPulse)
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
        data = DataRepository.read_History()
        return jsonify(data), 200
    elif request.method == 'POST':
        pass


@app.route(endpoint + '/temperatuur/', methods=['GET','PUT'])
def temperatuur():
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass

@app.route(endpoint + "/history/WaterTemp/", methods=['GET'])
def historykWaterTemp():
    if request.method == "GET":
        data = DataRepository.read_HistoryWaterTemp()
        return jsonify(data), 200

@app.route(endpoint + "/history/Humidity/", methods=['GET'])
def historyHumidity():
    if request.method == "GET":
        data = DataRepository.read_HistoryHumidity()
        return jsonify(data), 200

@app.route(endpoint + "/history/waterflow/", methods=['GET'])
def historyWaterflow():
    if request.method == "GET":
        data = DataRepository.read_HistoryWaterflow()
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
    global SelectedMagnetContact
    temperature = read_temperature()
    #device id = 2 for watertemp
    print("selectedMagnetcontact")
    print(SelectedMagnetContact)
    #DataRepository.create_History(2,SelectedMagnetContact, datetime.now() , str(temperature), "Ingelezen temperatuur")
    if(SelectedMagnetContact!=0):
        DataRepository.update_History(146,2,SelectedMagnetContact, datetime.now() , str(temperature), "Ingelezen temperatuur")



# Humidity Sensor
def Read_Humidity():
    humidity = 0
    try:
        # Print the values to the serial port
        # temperature_c = dhtDevice.temperature
        # temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        # print(
        #     "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
        #         temperature_f, temperature_c, humidity
        #     )
        # )
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        #dhtDevice.exit()
    return humidity


def Write_Humidity():
    global SelectedMagnetContact
    humidity = Read_Humidity()
    #device id = 3 for humidity
    #DataRepository.create_History(3,SelectedMagnetContact, datetime.now() , str(humidity), "Ingelezen luchtvochtigheid")
    if(SelectedMagnetContact!=0):
        DataRepository.update_History(147, 3 ,SelectedMagnetContact, datetime.now() , str(humidity), "Ingelezen luchtvochtigheid")



# Water Flow Sensor
def Write_Waterflow():
    global SelectedMagnetContact
    waterflow = Read_Waterflow()
    if(SelectedMagnetContact!=0):
        DataRepository.create_History(1,SelectedMagnetContact, datetime.now(), str(waterflow), "Ingelezen waterflow")

def Read_Waterflow():
    global start_counter
    global WaterFlowPulsen
    start_counter = 1
    time.sleep(1)
    start_counter = 0
    flow = (WaterFlowPulsen / 7.5*1000/60) # Pulse frequency (Hz) = 7.5Q, Q is flow rate in L/min.
    print("The flow is: %.3f ml/sec" % (flow))
    #publish.single("/Garden.Pi/WaterFlow", flow, hostname=MQTT_SERVER)
    WaterFlowPulsen = 0
    #time.sleep(1)
    return flow

def countPulse(pin):
   global WaterFlowPulsen
   if start_counter == 1:
      WaterFlowPulsen = WaterFlowPulsen+1


# Find User
def FindUser(x=0):
    global SelectedMagnetContact
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
    # print(MagnetContactOneState)
    # print(MagnetContactTwoState)
    # print(MagnetContactThreeState)
    # print(MagnetContactFourState)


# Requesting data
def Read_data():
    global SelectedMagnetContact
    if(SelectedMagnetContact!=0):
        Write_WaterTemperature()
        Write_Humidity()
        Write_Waterflow()
        threading.Timer(1,Read_data).start()


#endregion



# START THE APP
if __name__ == '__main__':
    print("backend running")
    setup()
    socketio.run(app, debug=False, host='0.0.0.0')