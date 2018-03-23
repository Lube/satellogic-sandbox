## Satellogic sandbox by Sebastian Luberriaga

Instalar los pips especificados en requirements.txt

```bash
pip install -r /path/to/requirements.txt
```

## Iniciar base terrestre

```bash
./build_base.sh
```

Este comando lanza dos procesos:

* Un proceso que simula una base terrestre
* Un web server (http://localhost:5000) que se comunica con dicha base, sirve archivos estáticos y una api con datos de la base.

## Lanzamiento de satélites

```bash
./launch_satelite.sh nombre success_rate
```

Este comando lanza un proceso que simula ser un satélite y se conecta con la base terrestre, si no se especifica un nombre se genera uno al azar, si no se especifica un success_rate (de 0 a 1) se le asigna 0.9 por defecto.

```bash
./launch_satelites.sh
```

Este comando lanza un 100 satelites

## Tweak de tareas

Se puede modificar la cantidad de tareas desde src/modules/base/**init**.py

Se pueden modificar los parametros de las tareas creadas desde src/modules/tarea/**init**.py
