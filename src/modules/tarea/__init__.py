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
