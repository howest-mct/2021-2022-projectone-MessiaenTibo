from flask_socketio import SocketIO, emit, send
#from importlib_metadata import method_cache
from pkg_resources import require
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, date
# Start app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Secret!aBcdXyZ' #(1)

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)
# init sensors
sensor_file_name = '/sys/bus/w1/devices/28-22cf61000900/w1_slave'



# Custom endpoint
endpoint = '/api/v1'


# ROUTES


# Schakeling
def Inlezen_temperatuur():
    try:
        tekst = ''
        while True:
            sensor_file = open(sensor_file_name,'r')
            for line in sensor_file:
                if 't=' in line: 
                    tekst = line[29] + line[30] + "." + line[31]+ line[32]+ line[33]
                print(tekst)
    except KeyboardInterrupt:
        print("error")
    finally:
        sensor_file.close()


# START THE APP
if __name__ == '__main__':
    #socketio.run(app, debug=True, host='0.0.0.0')
    pass