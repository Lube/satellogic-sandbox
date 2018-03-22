import sys
import socket
import os
import json
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

import src.lib.network as network

_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_url_path=_dir + '/../dashboard/build')
CORS(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    base_dir = _dir + '/../dashboard/build'
    if(path == ""):
        return send_from_directory(base_dir, 'index.html')
    else:
        fileName = path.split("/")[-1]
        partialFolderPath = path.split("/")[:-1]
        folderPath = os.path.join(base_dir, '/'.join(partialFolderPath))

        if(os.path.exists(os.path.join(folderPath, fileName))):
            return send_from_directory(folderPath, fileName)
        else:
            return send_from_directory(base_dir, 'index.html')

server_address = _dir + '/web_socket'

def connectToTerranBase():
    try:
        web_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        web_socket.connect(server_address)
        return web_socket
    except socket.error as msg:
        print(msg)
        sys.exit(1)

def requestToTerranBaseAndDecodeResponse(command, extra=None):
    request = {}
    request.update({'command': command})

    if (extra is not None):
        request.update(extra)

    web_socket = connectToTerranBase()
    web_socket.sendall(network.encodeForNetwork(request))

    response = network.recv(web_socket)

    return response.get('result')

@app.route("/api/tareas")
def tareas():
    response = requestToTerranBaseAndDecodeResponse('getTareas')
    return jsonify(response)


@app.route("/api/satelites")
def satelites():
    response = requestToTerranBaseAndDecodeResponse('getSatelites')
    return jsonify(response)


@app.route("/api/resultados")
def resultados():
    response = requestToTerranBaseAndDecodeResponse('getResultados')
    return jsonify(response)


@app.route("/api/asignaciones")
def asignaciones():
    response = requestToTerranBaseAndDecodeResponse('getAsignaciones')
    return jsonify(response)


@app.route("/api/tarea", methods=['POST'])
def addTarea():
    response = requestToTerranBaseAndDecodeResponse(
        'addTarea', {'tarea': request.get_json()})
    return jsonify(response)


@app.route("/api/ejecutar_campaña", methods=['POST'])
def ejecutarCampaña():
    response = requestToTerranBaseAndDecodeResponse('startCampaña')
    return jsonify(response)

app.run(port=5000, host='0.0.0.0', debug=False, use_reloader=False, threaded=True)
