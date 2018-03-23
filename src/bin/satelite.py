import sys
import time
import os
import asyncio
import socket
import sys

_dir = os.path.dirname(os.path.abspath(__file__))

import src.modules.satelite as satelite
import src.lib.network as network

server_address = _dir + '/sat_socket'

print('Conectando a la base terrestre en %s' % server_address)

satelite_name = sys.argv[1] if len(sys.argv) > 1 else None
satelite_success_rate = float(sys.argv[2]) if len(sys.argv) > 2 else None

loop = asyncio.get_event_loop()

Satelite = satelite.Satelite(satelite_name, satelite_success_rate, loop)


@asyncio.coroutine
def sat_server(loop, satelite):
    while True:
        action = satelite.getCurrentAction()
        if action is not None:
            loop.create_task(execAction(loop, action, satelite.handleResponse))

        yield from asyncio.sleep(1)


@asyncio.coroutine
def execAction(loop, action, handler):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sat_socket:
        try:
            sat_socket.connect(server_address)
            action(sat_socket)

            if sat_socket.fileno() != -1:
                response = yield from network.recv_async(sat_socket, loop)
                handler(response)
        except ConnectionRefusedError:
            Satelite.resetConnection()
            print('Base terrestre no encontrada!')


try:
    loop.create_task(sat_server(loop, Satelite))
    loop.run_forever()

except KeyboardInterrupt:
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sat_socket:
        try:
            sat_socket.connect(server_address)
            Satelite.disconnectFromBase(sat_socket)
        except ConnectionRefusedError:
            pass

finally:
    print('Deorbitando satelite!')
    sys.exit(0)
