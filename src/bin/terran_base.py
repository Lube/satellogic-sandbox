import socket
import asyncio
import select
import sys
import os

_dir = os.path.dirname(os.path.abspath(__file__))

import src.modules.base as base
import src.lib.network as network

sat_address = _dir + '/sat_socket'
web_address = _dir + '/web_socket'

try:
    os.unlink(sat_address)
    os.unlink(web_address)
except OSError:
    if os.path.exists(sat_address):
        raise
    if os.path.exists(web_address):
        raise

print(r"""
,--..Y    
\   /`.   
 \.    \
  :::--' 
""")

print('Esperando conexiones de satelites')
print('Web Server escuchando en http://localhost:5000')

loop = asyncio.get_event_loop()

print('Terran base warming up')
Terran_Base = base.Base(loop)


@asyncio.coroutine
def terran_server(socket, handler):
    while True:
        conn, addr = yield from loop.sock_accept(socket)
        loop.create_task(request(conn, handler))


@asyncio.coroutine
def request(connection, handler):
    request = yield from network.recv_async(connection, loop)
    response = handler(request)
    try:
        yield from loop.sock_sendall(connection,
                                     network.encodeForNetwork(response))
        connection.close()
    except BrokenPipeError:
        pass


def init_socket(socket, address):
    socket.setblocking(0)
    socket.bind(address)
    socket.listen(128)


try:
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sat_socket, \
         socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as web_socket:

        init_socket(sat_socket, sat_address)
        init_socket(web_socket, web_address)

        print('Abriendo canal de comunicaciones satelital %s' % sat_address)
        print('Abriendo canal de comunicaciones web %s' % web_address)

        loop.create_task(terran_server(sat_socket, Terran_Base.handleRequest))
        loop.create_task(
            terran_server(web_socket, Terran_Base.handleWebRequest))
        loop.run_forever()

except KeyboardInterrupt:
    sys.exit(0)

finally:
    print('Protocolo de autodestrucción iniciado!')
    os.unlink(sat_address)
    os.unlink(web_address)
