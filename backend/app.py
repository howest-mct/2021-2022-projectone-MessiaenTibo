#region **** IMPORTS ****
import json
from turtle import color
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
from subprocess import check_output
from LCD import lcd
import neopixel
lcd = lcd()

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
MagnetContactOne = 17 #was 18 is nu aangepast voor neopixelring
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
Buzzer = 180

# Button
button = 5

# LedCircle
aantalleds = 24
LedCircle = 26
loadingpixel = 0
pixels = neopixel.NeoPixel(board.D18, aantalleds)

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
    #test neopixel
    # pixels = neopixel.NeoPixel(board.D18, aantalleds)
    pixels.fill(0)
    pixels[0] = (28, 28, 28)
    for i in range(23):
         #pixels[i] = (0, 0, 0)
         pixels[i+1] = (28, 28, 28)
         time.sleep(0.04)

    #test neopixel
    LedCircleLoading()


    lcd.lcdInit()
    lcd.clear_screen()
    ips = check_output(['hostname', '--all-ip-addresses']).split()
    lcd.write_message(ips[0].decode())
    print(ips[0].decode())
    # Code voor eventuele tweede IP adress weer te geven
    if len(ips) > 1:
        lcd.clear_screen()
        lcd.write_message(ips[1].decode())
        print(ips[1].decode())
    FindUser()
    Write_HumidityAndTemperature()


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

@app.route(endpoint + "/history/Waterflow/", methods=['GET'])
def historyWaterflow():
    if request.method == "GET":
        data = DataRepository.read_HistoryWaterflow()
        return jsonify(data), 200

@app.route(endpoint + "/history/RoomTemp/", methods=['GET'])
def historyRoomTemp():
    if request.method == "GET":
        data = DataRepository.read_HistoryRoomTemp()
        return jsonify(data), 200

@app.route(endpoint + "/history/WaterUsage/", methods=['GET'])
def historyWaterUsage():
    if request.method == "GET":
        data = DataRepository.read_WaterUsage()
        return jsonify(data), 200

@app.route(endpoint + "/history/TodaysWaterUsage/", methods=['GET'])
def historyTodaysWaterUsage():
    if request.method == "GET":
        data = DataRepository.read_TodaysWaterUsage()
        return jsonify(data), 200

@app.route(endpoint + "/TotalGoal/", methods=['GET'])
def TotalGoal():
    if request.method == "GET":
        data = DataRepository.read_TotalGoal()
        return jsonify(data), 200

@app.route(endpoint + "/MagneticContactUser/<id>", methods=['GET'])
def MagneticContactUserById(id):
    if request.method == "GET":
        data = DataRepository.read_MagneticContact(id)
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
    if(SelectedMagnetContact!=0):
        #DataRepository.update_History(146,2,SelectedMagnetContact, datetime.now() , str(temperature), "Ingelezen temperatuur")
        DataRepository.create_History(2,SelectedMagnetContact, datetime.now() , str(temperature), "Ingelezen water temperatuur")



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

def Read_RoomTemperature():
    temperature_c = 0
    try:
        temperature_c = dhtDevice.temperature
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        #dhtDevice.exit()
    return temperature_c


def Write_HumidityAndTemperature():
    global SelectedMagnetContact
    humidity = Read_Humidity()
    temperature = Read_RoomTemperature()
    #device id = 3 for humidity
    #DataRepository.update_History(147, 3 ,SelectedMagnetContact, datetime.now() , str(humidity), "Ingelezen luchtvochtigheid")
    DataRepository.create_HistoryBadkamer(3, datetime.now() , str(humidity), "Ingelezen luchtvochtigheid")
    DataRepository.create_HistoryBadkamer(4, datetime.now() , str(temperature), "Ingelezen kamer temperatuur")
    print(str(humidity) + "%")
    print(str(temperature) + "°C")
    socketio.emit("B2F_new_data")
    threading.Timer(30,Write_HumidityAndTemperature).start()



# Water Flow Sensor
def Write_Waterflow():
    global SelectedMagnetContact
    waterflow = Read_Waterflow()
    if(SelectedMagnetContact!=0):
        DataRepository.create_History(1, SelectedMagnetContact, datetime.now(), str(waterflow), "Ingelezen waterflow")

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
        socketio.emit("B2F_new_active_user", SelectedMagnetContact)
        Read_data()
    else:
        socketio.emit("B2F_no_active_user")
        if(MagnetContactOneState | MagnetContactTwoState | MagnetContactThreeState | MagnetContactFourState):
            print("There is only 1 user at the same time allowd!")
        else:
            print("There must be at least 1 selected user!")


# Requesting data
def Read_data():
    global SelectedMagnetContact
    if(SelectedMagnetContact!=0):
        Write_WaterTemperature()
        Write_Waterflow()
        socketio.emit("B2F_new_data_id", SelectedMagnetContact)
        threading.Timer(1,Read_data).start()

# loading led circle
def LedCircleLoading():
    global loadingpixel
    pixels.fill(0)
    pixels[loadingpixel] = (28, 28, 28)
    loadingpixel = loadingpixel + 1
    if(loadingpixel >= aantalleds):
        loadingpixel = 0
    threading.Timer(0.2,LedCircleLoading).start()

#endregion



# SOCKET.IO EVENTS
@socketio.on('connect')
def initial_connection():
    print('A new client connect')

@socketio.on('F2B_new_connection')
def New_connection():
    socketio.emit("B2F_new_data")




# START THE APP
if __name__ == '__main__':
    print("backend running")
    setup()
    socketio.run(app, debug=False, host='0.0.0.0')