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

try:
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sat_socket, \
         socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as web_socket:

        sat_socket.setblocking(0)
        sat_socket.bind(sat_address)
        sat_socket.listen(128)

        web_socket.setblocking(0)
        web_socket.bind(web_address)
        web_socket.listen(128)

        print('Abriendo canal de comunicaciones satelital %s' % sat_address)
        print('Abriendo canal de comunicaciones web %s' % web_address)

        @asyncio.coroutine
        def terran_sat_server():
            while True:
                conn, addr = yield from loop.sock_accept(sat_socket)
                request = network.recvPackage(loop, conn)
                loop.create_task(Terran_Base.handleRequest(loop, request, conn))

        @asyncio.coroutine
        def terran_web_server():
            while True:
                conn, addr = yield from loop.sock_accept(web_socket)
                request = network.recvPackage(conn, loop)
                loop.create_task(Terran_Base.handleWebRequest(loop, request, conn))

        loop.create_task(terran_sat_server())
        loop.create_task(terran_web_server())
        loop.run_forever()

except KeyboardInterrupt:
    sys.exit(0)

finally:
    print('Protocolo de autodestrucción iniciado!')
    os.unlink(sat_address)
    os.unlink(web_address)
