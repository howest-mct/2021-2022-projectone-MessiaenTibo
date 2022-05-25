import json
from flask_socketio import SocketIO, emit, send
#from importlib_metadata import method_cache
from pkg_resources import require
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, date
import threading
# Start app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False, engineio_logger=False, ping_timeout=1)
CORS(app)
# init sensors
sensor_file_name = '/sys/bus/w1/devices/28-22cf61000900/w1_slave'



# Custom endpoint
endpoint = '/api/v1'


# ROUTES
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

# Schakeling
def Inlezen_temperatuur():
    tekst = ''
    sensor_file = open(sensor_file_name,'r')
    for line in sensor_file:
        if 't=' in line: 
            tekst = line[29] + line[30] + "." + line[31]+ line[32]+ line[33]
        print(tekst)

    #DataRepository.create_temp(2,1, datetime.now() , tekst, "Ingelezen temperatuur")
    threading.Timer(1,Inlezen_temperatuur).start()
  
        


# START THE APP
if __name__ == '__main__':
    Inlezen_temperatuur()
    # socketio.run(app, debug=True, host='0.0.0.0')
    print("backend running")
    socketio.run(app, debug=False, host='0.0.0.0')