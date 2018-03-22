import random
import sys
import time
import pickle
import json
import functools
import os.path
import time, threading
import asyncio

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
    def __init__(self, loop):
        self.status = OPERATIONAL_STATUS
        self.tareas = tareas
        self.loop = loop
        self.satelites = []

        json.dump(list(), open(_dir + "/results.json", "w"), indent=2)
        json.dump(list(), open(_dir + "/assignments.json", "w"), indent=2)

        self.webRequestHandlerDispatcher = {
            'getTareas': self.getTareas,
            'getSatelites': self.getSatelites,
            'getAsignaciones': self.getAsignaciones,
            'getResultados': self.getResultados,
            'addTarea': self.addTarea,
            'startCampaña': self.ejecutarCampaña
        }

        self.sateliteRequestHandlerDispatcher = {
            'registro': self.handleRegistro,
            'desconexion': self.handleDesconexion,
            'requestAssignments': self.handleRequestAssignments,
            'submitResults': self.handleResults
        }

        self.loop.create_task(self.cleanupOldSatelites())

    def updateLastMessageAt(self, sateliteName):
        for idx, satelite in enumerate(self.satelites):
            if satelite.get('nombre') == sateliteName:
                self.satelites[idx]['last_message_at'] = time.time()


    @asyncio.coroutine
    def cleanupOldSatelites(self):
        while True:
            self.satelites = [
                satelite for satelite in self.satelites
                if satelite.get('last_message_at') + 10 > time.time()
            ]

            yield from asyncio.sleep(10)


    def handleRegistro(self, request):
        self.satelites.append({
            'nombre': request.get('nombre'),
            'status': SATELITE_FREE_STATUS,
            'success_rate': request.get('success_rate'),
            'results': None,
            'last_message_at': time.time()
        })

        self.status = WAITING_FOR_ORDERS_STATUS

        return True

    def handleDesconexion(self, request):
        self.satelites = [
            satelite for satelite in self.satelites
            if satelite.get('nombre') != request.get('nombre')
        ]

    def handleRequestAssignments(self, request):
        if self.status == SENDING_ASSIGNMENT_INFO_STATUS:
            for idx, satelite in enumerate(self.satelites):
                if satelite.get('nombre') == request.get('nombre') and \
                        satelite.get('status') == SATELITE_FREE_STATUS and \
                        satelite.get('plan') is not None:
                    self.satelites[idx]['status'] = SATELITE_BUSY_STATUS
                    
                    response = satelite.get('plan')

            if (all(
                    map(lambda satelite: satelite.get('status') == SATELITE_BUSY_STATUS,
                        self.satelites))):
                self.status = WAITING_FOR_RESULTS_STATUS

        return response or None

    def resetAssignments(self):
        for idx, satelite in enumerate(self.satelites):
            self.satelites[idx]['status'] = SATELITE_FREE_STATUS
            self.satelites[idx]['results'] = None
            self.satelites[idx]['plan'] = None

    def handleResults(self, request):
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

            return True
        else:
            return False

    def handleRequest(self, request, conn):
        command = request.get('command')
        self.updateLastMessageAt(request.get('nombre'))
        response = self.sateliteRequestHandlerDispatcher.get(command)(request, conn)
        
        yield from self.loop.sendall(conn, network.encodeForNetwork({
            'command': request.get('command'),
            'result': response
        }))
        conn.close()


    def handleWebRequest(self, request, conn):
        command = request.get('command')
        response = self.webRequestHandlerDispatcher.get(command)(request, conn)

        yield from self.loop.sendall(conn, network.encodeForNetwork({
            'command': request.get('command'),
            'result': response
        }))

        conn.close()

    def addTarea(self, request):
        self.tareas.append(request.get('tarea'))
        return True

    def ejecutarCampaña(self, request):
        if self.status == WAITING_FOR_ORDERS_STATUS:
            self.repartirPlanesEntreSatelites(self.calcularCampaña())
        
        return True

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

    def getAsignaciones(self, request):
        try:
            return json.load(open(_dir + "/assignments.json", "r"))
        except:
            return []

    def getResultados(self, request):
        try:
            return json.load(open(_dir + "/results.json", "r"))
        except:
            return []

    def getTareas(self, request):
        return self.tareas

    def getSatelites(self, request):
        return self.satelites