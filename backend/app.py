from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, date

# Start app
app = Flask(__name__)
CORS(app)



# Custom endpoint
endpoint = '/api/v1'


# ROUTES





# START THE APP
if __name__ == '__main__':
 socketio.run(app, debug=True, host='0.0.0.0') 
