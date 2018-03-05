import sys
import time
import os
import sys

_dir = os.path.dirname(os.path.abspath(__file__))

import src.modules.satelite as satelite
import src.lib.network as network

server_address = _dir + '/sat_socket'

print('Conectando a la base terrestre en %s' % server_address)

satelite_name = sys.argv[1] if len(sys.argv) > 1 else None
satelite_success_rate = float(sys.argv[2]) if len(sys.argv) > 2 else None

Satelite = satelite.Satelite(satelite_name, satelite_success_rate,
                             server_address)

try:
    while True:

        if Satelite.status == satelite.OPERATIONAL_STATUS:
            sock = Satelite.connectToBase()
            Satelite.registerToTerranBase(sock)
        elif Satelite.status == satelite.WAITING_FOR_ASSIGNMENT_STATUS:
            sock = Satelite.connectToBase()
            Satelite.sendAssignmentRequest(sock)
        elif Satelite.status == satelite.WAITING_TO_SEND_RESULTS_STATUS:
            sock = Satelite.connectToBase()
            Satelite.sendResults(sock)
            print("Tareas del satelite terminadas, enviando resultados!")


        if sock.fileno() != -1:
            response = network.recvPackage(sock)

            sock.close()

            Satelite.handleResponse(response)

        time.sleep(2)

except KeyboardInterrupt:
    sock = Satelite.connectToBase()
    Satelite.disconnectFromBase(sock)
    sys.exit(0)

finally:
    print('Deorbitando satelite!')
