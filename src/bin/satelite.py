import sys
import time
import os
import socket
import sys

_dir = os.path.dirname(os.path.abspath(__file__))

import src.modules.satelite as satelite
import src.lib.network as network

server_address = _dir + '/sat_socket'

print('Conectando a la base terrestre en %s' % server_address)

satelite_name = sys.argv[1] if len(sys.argv) > 1 else None
satelite_success_rate = float(sys.argv[2]) if len(sys.argv) > 2 else None

Satelite = satelite.Satelite(satelite_name, satelite_success_rate)

try:
    while True:
        if Satelite.status in [
                satelite.OPERATIONAL_STATUS,
                satelite.WAITING_FOR_ASSIGNMENT_STATUS,
                satelite.WAITING_TO_SEND_RESULTS_STATUS
        ]:
            with socket.socket(socket.AF_UNIX,
                               socket.SOCK_STREAM) as sat_socket:
                try:
                    sat_socket.connect(server_address)

                    if Satelite.status == satelite.OPERATIONAL_STATUS:
                        Satelite.registerToTerranBase(sat_socket)
                    elif Satelite.status == satelite.WAITING_FOR_ASSIGNMENT_STATUS:
                        Satelite.sendAssignmentRequest(sat_socket)
                    elif Satelite.status == satelite.WAITING_TO_SEND_RESULTS_STATUS:
                        Satelite.sendResults(sat_socket)
                        print("Tareas del satelite terminadas, enviando resultados!")

                    if sat_socket.fileno() != -1:
                        response = network.recv(sat_socket)
                        Satelite.handleResponse(response)

                except ConnectionRefusedError:
                    print('Base terrestre no encontrada!')
                    sys.exit(0)

        time.sleep(2)

except KeyboardInterrupt:
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sat_socket:
        try:
            sat_socket.connect(server_address)
            Satelite.disconnectFromBase(sat_socket)
        except ConnectionRefusedError:
            pass
    sys.exit(0)

finally:
    print('Deorbitando satelite!')
