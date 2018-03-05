import random
import sys
import time
import pickle
import json
import functools
import os.path

_dir = os.path.dirname(os.path.abspath(__file__))

import src.modules.plan as planComponent
import src.modules.campaña as campañaComponent
import src.lib.network as network

OPERATIONAL_STATUS = "OPERATIONAL"
WAITING_FOR_ORDERS_STATUS = "WAITING FOR ORDERS"
SENDING_ASSIGNMENT_INFO_STATUS = "SENDING ASSIGNMENT INFO"
WAITING_FOR_RESULTS_STATUS = "WAITING FOR RESULTS"

SATELITE_FREE_STATUS = "FREE"
SATELITE_BUSY_STATUS = "BUSY"

tareaA = dict = {'recursos': [1, 2], 'payoff': 10, 'hora': 1, 'nombre': 'A'}
tareaB = dict = {'recursos': [1, 5], 'payoff': 4, 'hora': 1, 'nombre': 'B'}
tareaC = dict = {'recursos': [1, 6], 'payoff': 4, 'hora': 1, 'nombre': 'C'}
tareaD = dict = {'recursos': [5, 6], 'payoff': 4, 'hora': 1, 'nombre': 'D'}

tareas = [tareaA, tareaB, tareaC, tareaD]


class Base:
    def __init__(self):
        self.status = OPERATIONAL_STATUS
        self.tareas = tareas
        self.satelites = []

        json.dump(list(), open(_dir + "/results.json", "w"), indent=2)
        json.dump(list(), open(_dir + "/assignments.json", "w"), indent=2)

        self.sateliteRequestHandlerDispatcher = {
            'registro': self.handleRegistro,
            'desconexion': self.handleDesconexion,
            'requestAssignments': self.handleRequestAssignments,
            'submitResults': self.handleResults
        }

        self.webRequestHandlerDispatcher = {
            'getTareas': self.getTareas,
            'getSatelites': self.getSatelites,
            'getAsignaciones': self.getAsignaciones,
            'getResultados': self.getResultados,
            'addTarea': self.addTarea,
            'startCampaña': self.ejecutarCampaña
        }

    def updateLastMessageAt(self, sateliteName): 
        for idx, satelite in enumerate(self.satelites):
            if satelite.get('nombre') == sateliteName:
                self.satelites[idx]['last_message_at'] = time.time()

    def cleanupOldSatelites(self): 
        self.satelites = [satelite for satelite in self.satelites if satelite.get('last_message_at') + 10 > time.time()]


    def handleRegistro(self, request, sock):
        self.satelites.append({
            'nombre': request.get('nombre'),
            'status': SATELITE_FREE_STATUS,
            'success_rate': request.get('success_rate'),
            'results': None,
            'last_message_at': time.time()
        })
        self.status = WAITING_FOR_ORDERS_STATUS
        sock.sendall(
            network.encodeForNetwork({
                'command': request.get('command'),
                'result': True
            }))

    def handleDesconexion(self, request, sock):
        self.satelites = [
            satelite for satelite in self.satelites
            if satelite.get('nombre') == request.get('nombre')
        ]

        sock.sendall(
            network.encodeForNetwork({
                'command': request.get('command'),
                'result': True
            }))

    def handleRequestAssignments(self, request, sock):
        if self.status == SENDING_ASSIGNMENT_INFO_STATUS:
            for idx, satelite in enumerate(self.satelites):
                if satelite.get('nombre') == request.get('nombre') and \
                        satelite.get('status') == SATELITE_FREE_STATUS and \
                        satelite.get('plan') is not None:
                    self.satelites[idx]['status'] = SATELITE_BUSY_STATUS
                    sock.sendall(
                        network.encodeForNetwork({
                            'command':
                            request.get('command'),
                            'plan':
                            satelite.get('plan')
                        }))

        if (all(
                map(lambda satelite: satelite.get('status') == SATELITE_BUSY_STATUS,
                    self.satelites))):
            self.status = WAITING_FOR_RESULTS_STATUS

    def resetAssignments(self):
        for idx, satelite in enumerate(self.satelites):
            self.satelites[idx]['status'] = SATELITE_FREE_STATUS
            self.satelites[idx]['results'] = None
            self.satelites[idx]['plan'] = None

    def handleResults(self, request, sock):
        if self.status == WAITING_FOR_RESULTS_STATUS:
            for idx, satelite in enumerate(self.satelites):
                if satelite.get('nombre') == request.get('nombre'):
                    self.satelites[idx]['results'] = request.get('results')

            if all([
                    satelite.get('results') is not None
                    for satelite in self.satelites
            ]):
                try:
                    results = json.load(open(_dir + "/results.json", "r"))
                except:
                    results = []

                results.append(self.satelites)
                json.dump(results, open(_dir + "/results.json", "w"), indent=2)

                self.status = WAITING_FOR_ORDERS_STATUS
                self.resetAssignments()

            sock.sendall(
                network.encodeForNetwork({
                    'command': request.get('command'),
                    'result': True
                }))
        else:
            sock.sendall(
                network.encodeForNetwork({
                    'command': request.get('command'),
                    'result': False
                }))

    def handleRequest(self, request, sock):
        command = request.get('command')
        self.updateLastMessageAt(request.get('nombre'))
        self.sateliteRequestHandlerDispatcher.get(command,
                                                  lambda x: x)(request, sock)

    def handleWebRequest(self, request, sock):
        command = request.get('command')
        self.webRequestHandlerDispatcher.get(command, lambda x: x)(request,
                                                                   sock)

    def addTarea(self, request, sock):
        self.tareas.append(request.get('tarea'))
        sock.sendall(
            network.encodeForNetwork({
                'command': request.get('command'),
                'result': True
            }))

    def ejecutarCampaña(self, request, sock):
        sock.sendall(
            network.encodeForNetwork({
                'command': request.get('command'),
                'result': True
            }))

        if self.status == WAITING_FOR_ORDERS_STATUS:
            self.repartirPlanesEntreSatelites(self.calcularCampaña())

    def calcularCampaña(self):
        return campañaComponent.obtenerMejorCampaña(
            planComponent.buscarPlanes(self.tareas), len(self.satelites))

    def repartirPlanesEntreSatelites(self, campaña):
        satelites = sorted(self.satelites, key=lambda s: s.get('success_rate'))
        campaña = sorted(campaña, key=lambda c: planComponent.calcularValor(c))

        for sateliteA, plan in zip(satelites, campaña):
            for idx, sateliteB in enumerate(self.satelites):
                if sateliteA.get('nombre') == sateliteB.get('nombre'):
                    self.satelites[idx]['plan'] = plan

        try:
            assignments = json.load(open(_dir + "/assignments.json", "r"))
        except:
            assignments = []

        assignments.append(self.satelites)
        json.dump(assignments, open(_dir + "/assignments.json", "w"), indent=2)

        self.status = SENDING_ASSIGNMENT_INFO_STATUS

    def getAsignaciones(self, request, sock):
        try:
            sock.sendall(
                network.encodeForNetwork({
                    'command':
                    request.get('command'),
                    'result':
                    json.load(open(_dir + "/assignments.json", "r"))
                }))
        except:
            sock.sendall(
                network.encodeForNetwork({
                    'command': request.get('command'),
                    'result': []
                }))

    def getResultados(self, request, sock):
        try:
            sock.sendall(
                network.encodeForNetwork({
                    'command':
                    request.get('command'),
                    'result':
                    json.load(open(_dir + "/results.json", "r"))
                }))
        except:
            sock.sendall(
                network.encodeForNetwork({
                    'command': request.get('command'),
                    'result': []
                }))

    def getTareas(self, request, sock):
        sock.sendall(
            network.encodeForNetwork({
                'command': request.get('command'),
                'result': self.tareas
            }))

    def getSatelites(self, request, sock):
        sock.sendall(
            network.encodeForNetwork({
                'command': request.get('command'),
                'result': self.satelites
            }))