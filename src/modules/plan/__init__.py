import itertools
import functools
import pprint
import src.modules.tarea as tareaComponent


def buscarPlanes(tareas):
    """Busca todos los planes posibles con las tareas provistas

    [Tarea] -> [Plan]
    """
    planesEncontrados = []
    for length in range(1, len(tareas) + 1):
        for plan in itertools.combinations(tareas, length):
            if (esValido(plan)):
                planesEncontrados.append(plan)

    return [list(plan) for plan in planesEncontrados]


def esValido(plan):
    """Chequea que dentro del plan no haya tareas que compartan recursos a una misma hora

    [Tarea] -> Bool
    """
    for (tareaA, tareaB) in itertools.combinations(plan, 2):
        if tareaComponent.comparteRecursosEnLaMismaHora(tareaA, tareaB):
            return False

    return True


def planTieneTarea(plan, tareaABuscar):
    """ 
    Plan -> Tarea -> Bool
    """
    for tarea in plan:
        if tareaComponent.sonLaMismaTarea(tarea, tareaABuscar):
            return True

    return False


def comparteTareas(planA, planB):
    """ Chequea si dos planes comparten alguna tarea

    Plan -> Plan -> Bool
    """
    for tarea in planA:
        if planTieneTarea(planB, tarea):
            return True

    return False


def calcularValor(plan):
    """
    Plan -> Int
    """
    return functools.reduce(
        lambda valor, tarea: tareaComponent.calcularValor(tarea) + valor, plan,
        0)
