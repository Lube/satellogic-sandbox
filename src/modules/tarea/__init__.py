import json
import os
import random
import uuid

_dir = os.path.dirname(os.path.abspath(__file__))

star_names = json.load(open(_dir + "/star_names.json", "r"))
verb_names = ['Analizar', 'Explorar', 'Investigar', 'Colonizar', 'Conquistar']


def generateRandomTarea():
    return {
        'id':
        str(uuid.uuid4()),
        'payoff':
        int(50 * random.random()) + 1,
        'hora':
        int(1 * random.random()),
        'nombre':
        random.choice(verb_names) + ' ' + random.choice(star_names),
        'recursos':
        list(
            set([
                int(5 * random.random()) + 1
                for _ in range(int(5 * random.random()) + 1)
            ]))
    }


def comparteRecursos(tareaA, tareaB):
    """Chequea si dos tareas comparten recursos

    Tarea -> Tarea -> Bool
    """
    return len(
        list(
            filter(lambda recurso: recurso in tareaB.get("recursos"),
                   tareaA.get("recursos")))) > 0


def sonLaMismaTarea(tareaA, tareaB):
    """Chequea si dos Tareas tienen los mismos recursos (o son Iguales)

    Tarea -> Tarea -> Bool
    """
    return all(recurso in tareaB.get('recursos') for recurso in tareaA.get('recursos')) \
        and all(recurso in tareaA.get('recursos') for recurso in tareaB.get('recursos'))


def calcularValor(tarea):
    return tarea.get('payoff')


def comparteRecursosEnLaMismaHora(tareaA, tareaB):
    """Chequea si dos tareas comparten recursos

    Tarea -> Tarea -> Bool
    """
    return comparteRecursos(
        tareaA, tareaB) and tareaA.get("hora") == tareaB.get("hora")
