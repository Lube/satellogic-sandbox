import json
import os
import random

_dir = os.path.dirname(os.path.abspath(__file__))


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


star_names = json.load(open(_dir + "/star_names.json", "r"))
verb_names = ['Analizar', 'Explorar', 'Investigar', 'Colonizar', 'Conquistar']


def generateRandomTarea():
    return {
        'payoff':
        int(10 * random.random()),
        'hora':
        int(4 * random.random()),
        'nombre':
        f"{random.choice(verb_names)} {random.choice(star_names)}.",
        'recursos':
        list(
            set([
                int(3 * random.random()) + 1
                for _ in range(int(2 * random.random()) + 1)
            ]))
    }
