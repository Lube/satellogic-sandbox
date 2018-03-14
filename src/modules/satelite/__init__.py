import random
import sys

import src.lib.network as network

OPERATIONAL_STATUS = "OPERATIONAL"
WAITING_FOR_ASSIGNMENT_STATUS = "WAITING FOR ASSIGNMENT"
WORKING_ON_ASSIGNMENT_STATUS = "WORKING ON ASSIGNMENT"
WAITING_TO_SEND_RESULTS_STATUS = "WAITING TO SEND RESULTS"

possible_names = [
    "They Told Me To Call It This", "Not Actually A Spaceship",
    "Yes, Actually This Is A Spaceship", "The Pi Is A Lie",
    "Not The Spaceship You Are Looking For", "Milk And Two Sugars",
    "May Contain Traces Of Zombies", "Awaiting Nominal Designation",
    "Babylon 6", "Glowbug", "Property Of The Imperial Navy", "Between Bars",
    "Made Of Lego", "Blame The Internet", "If Found, Please Return To Earth",
    "Under The Thumb", "Pointing The Way", "The Impudent Finger",
    "Better Than A Ring", "Wrapped Around Pinky", "Probably An Antique"
]


class Satelite:
    def __init__(self, nombre, success_rate):
        self.status = OPERATIONAL_STATUS
        self.nombre = random.choice(
            possible_names) if nombre is None else nombre
        self.success_rate = 0.9 if (success_rate is None or success_rate > 1
                                    or success_rate < 0) else success_rate

        self.responseHandlerDispatcher = {
            'registro': self.handleResponseRegistro,
            'requestAssignments': self.handleResponseRequestAssignments,
            'submitResults': self.handleResponseResultsDelivered
        }

    def registerToTerranBase(self, sock):
        sock.sendall(
            network.encodeForNetwork({
                'command': 'registro',
                'nombre': self.nombre,
                'success_rate': self.success_rate
            }))

    def sendAssignmentRequest(self, sock):
        sock.sendall(
            network.encodeForNetwork({
                'command': 'requestAssignments',
                'nombre': self.nombre
            }))

    def sendResults(self, sock):
        sock.sendall(
            network.encodeForNetwork({
                'command': 'submitResults',
                'nombre': self.nombre,
                'results': self.results
            }))
        self.status = WAITING_FOR_ASSIGNMENT_STATUS

    def handleResponse(self, response):
        command = response.get('command')
        self.responseHandlerDispatcher.get(command, lambda x: x)(response)

    def handleResponseRegistro(self, response):
        print("Contacto exitoso con base terrestre!")
        self.status = WAITING_FOR_ASSIGNMENT_STATUS

    def handleResponseRequestAssignments(self, response):
        self.status = WORKING_ON_ASSIGNMENT_STATUS

        tareas = response.get('plan')

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

    def disconnectFromBase(self, sock):
        sock.sendall(
            network.encodeForNetwork({
                'command': 'desconexion',
                'nombre': self.nombre
            }))
