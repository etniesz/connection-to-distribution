import logging
import json
from flask import Flask, request
from flask_socketio import SocketIO, Namespace
import datetime
from threading import Thread
from time import sleep

format = "%(asctime)s - %(process)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

async_mode = 'eventlet'
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode=async_mode, logger=False, engineio_logger=False, max_http_buffer_size=1e8)

# config
config = json.load(open('config.json'))

# view
@app.route('/')
def index():
    return 'Hello, World!'

# server Socket
class conected(Namespace):
    def on_connect(self):
        logging.info(f"Connect sid: {request.sid}")

    def on_report(self, data):
        socketio.emit('distribution', data, namespace='/audioSeg')
    
    def on_disconnect(self):
        logging.info(f"Disconnect sid: {request.sid}")  

socketio.on_namespace(conected("/conected"))

# salida de datos a todos los subcriptores

class audioSegDistribution(Namespace):
    def on_connect(self):
        logging.info(f"Connect audioSeg sid: {request.sid}")

    def on_report(self, data):
        socketio.emit('distribution', data, namespace='/featureExtrac')

    def on_disconnect(self):
        logging.info(f"Disconnect audioSeg sid: {request.sid}")  

socketio.on_namespace(audioSegDistribution("/audioSeg"))

class featureExtraction(Namespace):
    def on_connect(self):
        logging.info(f"Connect featureExtrac sid: {request.sid}")

    def on_disconnect(self):
        logging.info(f"Disconnect featureExtrac sid: {request.sid}")  

socketio.on_namespace(featureExtraction("/featureExtrac"))



# Lanzar servicio
    
if __name__ == '__main__':
    logging.info(f"Server start")
    socketio.run(app, debug=config["server"]["mode"], port=config["server"]["port"], host=config["server"]["ip"], log_output=False)

