import random
import sys
import json
import os
import uuid

import src.lib.network as network

OPERATIONAL_STATUS = "OPERATIONAL"
WAITING_FOR_ASSIGNMENT_STATUS = "WAITING FOR ASSIGNMENT"
WORKING_ON_ASSIGNMENT_STATUS = "WORKING ON ASSIGNMENT"
WAITING_TO_SEND_RESULTS_STATUS = "WAITING TO SEND RESULTS"

_dir = os.path.dirname(os.path.abspath(__file__))
possible_names = json.load(open(_dir + "/ship_names.json", "r"))


class Satelite:
    def __init__(self, nombre, success_rate, loop):
        self.loop = loop
        self.status = OPERATIONAL_STATUS
        self.nombre = random.choice(
            possible_names) if nombre is None else nombre
        self.success_rate = 0.9 if (success_rate is None or success_rate > 1
                                    or success_rate < 0) else success_rate

        self.id = str(uuid.uuid4())
        self.responseHandlerDispatcher = {
            'registro': self.handleResponseRegistro,
            'requestAssignments': self.handleResponseRequestAssignments,
            'submitResults': self.handleResponseResultsDelivered
        }

    def getCurrentAction(self):
        actionsByStatus = {
            OPERATIONAL_STATUS: self.registerToTerranBase,
            WAITING_FOR_ASSIGNMENT_STATUS: self.sendAssignmentRequest,
            WAITING_TO_SEND_RESULTS_STATUS: self.sendResults
        }

        return actionsByStatus.get(self.status, None)

    def sendToTerranBase(self, sock, request):
        self.loop.sock_sendall(sock, network.encodeForNetwork(request))

    def registerToTerranBase(self, sock):
        return self.sendToTerranBase(
            sock, {
                'id': self.id,
                'command': 'registro',
                'nombre': self.nombre,
                'success_rate': self.success_rate
            })

    def sendAssignmentRequest(self, sock):
        return self.sendToTerranBase(sock, {
            'id': self.id,
            'command': 'requestAssignments',
            'nombre': self.nombre
        })

    def sendResults(self, sock):
        self.status = WAITING_FOR_ASSIGNMENT_STATUS
        return self.sendToTerranBase(
            sock, {
                'id': self.id,
                'command': 'submitResults',
                'nombre': self.nombre,
                'results': self.results
            })

    def disconnectFromBase(self, sock):
        return self.sendToTerranBase(sock, {
            'id': self.id,
            'command': 'desconexion',
            'nombre': self.nombre
        })

    def resetConnection(self):
        self.status = OPERATIONAL_STATUS

    def handleResponse(self, response):
        self.responseHandlerDispatcher.get(response.get('command'))(response)

    def handleResponseRegistro(self, response):
        print("Contacto exitoso con base terrestre!")
        self.status = WAITING_FOR_ASSIGNMENT_STATUS

    def handleResponseRequestAssignments(self, response):
        if response.get('result') is not None:
            self.status = WORKING_ON_ASSIGNMENT_STATUS

            tareas = response.get('result')

            self.results = [{
                'nombre': tarea.get('nombre'),
                'resultado': self.executeTarea(tarea)
            } for tarea in tareas]

            self.status = WAITING_TO_SEND_RESULTS_STATUS

    def executeTarea(self, tarea):
        if random.random() < self.success_rate:
            return tarea.get('payoff')
        else:
            return 0

    def handleResponseResultsDelivered(self, response):
        if response.get('result'):
            self.status = WAITING_FOR_ASSIGNMENT_STATUS
