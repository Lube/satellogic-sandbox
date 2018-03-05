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
- Un proceso que simula una base terrestre
- Un web server que se comunica con dicha base, sirve archivos estáticos y una api con datos de la base

## Lanzamiento de satelites

```bash
./launch_satellite.sh
```

Este comando lanza un proceso que simula ser un satelite y se conecta con la base terrestre