import itertools
import functools

import src.modules.plan as planComponent


def buscarCampañas(planes, numeroSatelites):
    """Busca todos los planes posibles con las tareas provistas

    [Tarea] -> [Plan]
    """
    campañasEncontradas = []
    for length in range(1, numeroSatelites + 1):
        for campaña in itertools.combinations(planes, length):
            campañasEncontradas.append(campaña)

    return [
        list(campaña) for campaña in campañasEncontradas if esValido(campaña)
    ]


def esValido(campaña):
    """Chequea que una campaña no tenga planes con tareas superpuestas

    [Plan] -> Bool
    """
    for (planA, planB) in itertools.combinations(campaña, 2):
        if planComponent.comparteTareas(planA, planB):
            return False

    return True


def calcularValor(campaña):
    """
    [Plan] -> Int
    """
    return functools.reduce(
        lambda valor, plan: planComponent.calcularValor(plan) + valor, campaña,
        0)


def obtenerMejorCampaña(planes, numeroMaximoSatelites):
    """
    [Plan] -> Int -> [Plan]
    """
    return next(
        iter(
            reversed(
                sorted(
                    buscarCampañas(planes, numeroMaximoSatelites),
                    key=lambda estrategia: calcularValor(estrategia)))),
        "No hay campañas")


def obtenerMejorCampañaBarata(tareasIniciales):
    recursosIniciales = list(
        set([
            recurso
            for tarea in [tarea['recursos'] for tarea in tareasIniciales]
            for recurso in tarea
        ]))

    campaña = []
    tareas = sorted(tareasIniciales[:], key=lambda tarea: tarea['payoff'])

    for tarea in tareas:
        plan = []
        recursos = initRecursos(recursosIniciales)

        for tarea in tareas:
            if tareaValidaEnPlan(recursos, tarea):
                plan.append(tarea)
                tareas = actualizarTareas(tareas, tarea)

                for recurso in tarea['recursos']:
                    recursos = actualizarRecursos(recursos, recurso,
                                                  tarea['hora'])

        if len(plan) > 0:
            campaña.append(plan)

    return sorted(campaña, key=getPayoffPlan)


def getPayoffPlan(plan):
    return functools.reduce(lambda total, tarea: tarea['payoff'] + total, plan,
                            0)


def initRecursos(recursos):
    return [{'recurso': recurso, 'horas': []} for recurso in recursos]


def tareaValidaEnPlan(recursos, tarea):
    return all(
        map(lambda recurso: isRecursoFree(recursos, recurso, tarea['hora']),
            tarea['recursos']))


def isRecursoFree(recursos, recursoAChequear, hora):
    for recurso in recursos:
        if recursoAChequear == recurso['recurso'] and hora in recurso['horas']:
            return False
    return True


def actualizarRecursos(recursos, recursoConsumido, hora):
    recursosActualizados = []
    for recurso in recursos:
        if recursoConsumido == recurso['recurso']:
            recurso['horas'].append(hora)
        recursosActualizados.append(recurso)
    return recursosActualizados


def actualizarTareas(tareas, tarea):
    return sorted(
        list(
            filter(lambda tareaAFiltrar: tareaAFiltrar['id'] != tarea['id'],
                   tareas)),
        key=lambda tarea: tarea['payoff'])
