import random
import sys
import time
import pickle
import json
import functools
import os.path
import time, threading

_dir = os.path.dirname(os.path.abspath(__file__))

import src.modules.tarea as tareaComponent
import src.modules.plan as planComponent
import src.modules.campaña as campañaComponent
import src.lib.network as network

WAITING_FOR_ORDERS_STATUS = "WAITING FOR ORDERS"
WAITING_FOR_RESULTS_STATUS = "WAITING FOR RESULTS"

SATELITE_FREE_STATUS = "FREE"
SATELITE_BUSY_STATUS = "BUSY"

# tareaA = dict = {'recursos': [1, 2], 'payoff': 10, 'hora': 1, 'nombre': 'A'}
# tareaB = dict = {'recursos': [1, 5], 'payoff': 4, 'hora': 1, 'nombre': 'B'}
# tareaC = dict = {'recursos': [1, 6], 'payoff': 4, 'hora': 1, 'nombre': 'C'}
# tareaD = dict = {'recursos': [5, 6], 'payoff': 4, 'hora': 1, 'nombre': 'D'}

# tareas = [tareaA, tareaB, tareaC, tareaD]

# tareas = [
#     tareaComponent.generateRandomTarea()
#     for _ in range(int(2500 * random.random()) + 1)
# ]

# tareas = [tareaComponent.generateRandomTarea() for _ in range(2500)]

# with open(_dir + "/tareas.pck", "wb") as f:
#     tareas = pickle.dump(tareas, f, pickle.HIGHEST_PROTOCOL)

with open(_dir + "/tareas.pck", "rb") as f:
    tareas = pickle.load(f)


class Base:
    def __init__(self):
        self.status = WAITING_FOR_ORDERS_STATUS
        self.tareas = tareas
        self.satelites = []

        with open(_dir + "/results.json", "w") as f:
            json.dump(list(), f, indent=2)
        with open(_dir + "/assignments.json", "w") as f:
            json.dump(list(), f, indent=2)

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

        t = threading.Thread(target=self.cleanupOldSatelites)
        t.start()

    def __del__(self):
        with open(_dir + "/results.json", "w") as f:
            json.dump(list(), f, indent=2)
        with open(_dir + "/assignments.json", "w") as f:
            json.dump(list(), f, indent=2)

    def cleanupOldSatelites(self):
        while True:
            self.satelites = [
                satelite for satelite in self.satelites
                if satelite.get('last_message_at') + 10 > time.time()
            ]

            time.sleep(10)
            t = threading.Thread(target=self.cleanupOldSatelites)
            t.start()

    def handleRegistro(self, request):
        self.satelites.append({
            'id': request.get('id'),
            'nombre': request.get('nombre'),
            'status': SATELITE_FREE_STATUS,
            'success_rate': request.get('success_rate'),
            'results': None,
            'last_message_at': time.time()
        })

        return True

    def handleDesconexion(self, request):
        self.satelites = [
            satelite for satelite in self.satelites
            if satelite.get('id') != request.get('id')
        ]

    def handleRequestAssignments(self, request):
        response = None

        for idx, satelite in enumerate(self.satelites):
            if satelite.get('id') == request.get('id') and \
                    satelite.get('status') == SATELITE_FREE_STATUS and \
                    satelite.get('plan') is not None:
                self.satelites[idx]['status'] = SATELITE_BUSY_STATUS

                response = satelite.get('plan')

        return response

    def resetAssignments(self):
        for idx, satelite in enumerate(self.satelites):
            self.satelites[idx]['status'] = SATELITE_FREE_STATUS
            self.satelites[idx]['results'] = None
            self.satelites[idx]['plan'] = None

    def handleResults(self, request):
        for idx, satelite in enumerate(self.satelites):
            if satelite.get('id') == request.get('id'):
                self.satelites[idx]['results'] = request.get('results')

        if all(
                list(
                    map(lambda x: x.get('results') is not None, [
                        satelite for satelite in self.satelites
                        if satelite.get('plan') is not None
                    ]))):
            try:
                with open(_dir + "/results.json", "r") as f:
                    results = json.load(f)
            except:
                results = []

            results.append(self.satelites)
            with open(_dir + "/results.json", "w") as f:
                json.dump(results, f, indent=2)

            self.status = WAITING_FOR_ORDERS_STATUS
            self.resetAssignments()

        return True

    def updateLastMessageAt(self, sateliteId):
        for idx, satelite in enumerate(self.satelites):
            if satelite.get('id') == sateliteId:
                self.satelites[idx]['last_message_at'] = time.time()

    def handleRequest(self, request):
        self.updateLastMessageAt(request.get('id'))

        response = self.sateliteRequestHandlerDispatcher.get(
            request.get('command'))(request)

        return {'command': request.get('command'), 'result': response}

    def handleWebRequest(self, request):
        response = self.webRequestHandlerDispatcher.get(
            request.get('command'))(request)

        return {'command': request.get('command'), 'result': response}

    def addTarea(self, request):
        self.tareas.append(request.get('tarea'))
        return True

    def ejecutarCampaña(self, request):
        if self.status == WAITING_FOR_ORDERS_STATUS and len(
                self.satelites) > 0:
            self.status = WAITING_FOR_RESULTS_STATUS
            self.repartirPlanesEntreSatelites(self.calcularCampañaBarata())

        return True

    def calcularCampaña(self):
        return campañaComponent.obtenerMejorCampaña(
            planComponent.buscarPlanes(self.tareas), len(self.satelites))

    def calcularCampañaBarata(self):
        return campañaComponent.obtenerMejorCampañaBarata(self.tareas)

    def repartirPlanesEntreSatelites(self, campaña):
        satelites = sorted(self.satelites, key=lambda s: s.get('success_rate'))
        campaña = sorted(campaña, key=lambda c: planComponent.calcularValor(c))

        for sateliteA, plan in zip(satelites, campaña):
            for idx, sateliteB in enumerate(self.satelites):
                if sateliteA.get('id') == sateliteB.get('id'):
                    self.satelites[idx]['plan'] = plan

        try:
            with open(_dir + "/assignments.json", "r") as f:
                assignments = json.load(f)
        except:
            assignments = []

        assignments.append(self.satelites)
        with open(_dir + "/assignments.json", "w") as f:
            json.dump(assignments, f, indent=2)

    def getAsignaciones(self, request):
        try:
            with open(_dir + "/assignments.json", "r") as f:
                return json.load(f)
        except:
            return []

    def getResultados(self, request):
        try:
            with open(_dir + "/results.json", "r") as f:
                return json.load(f)
        except:
            return []

    def getTareas(self, request):
        return self.tareas

    def getSatelites(self, request):
        return self.satelites