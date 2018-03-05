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
