import socket
import select
import sys
import os

_dir = os.path.dirname(os.path.abspath(__file__))

import src.modules.base as base
import src.lib.network as network

sat_address = _dir + '/sat_socket'
web_address = _dir + '/web_socket'

print('Terran base warming up')
Terran_Base = base.Base()

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

try:
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sat_socket, \
         socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as web_socket:

        sat_socket.setblocking(0)
        sat_socket.bind(sat_address)
        sat_socket.listen(1)

        web_socket.setblocking(0)
        web_socket.bind(web_address)
        web_socket.listen(1)

        print('Abriendo canal de comunicaciones satelital %s' % sat_address)
        print('Abriendo canal de comunicaciones web %s' % web_address)

        while True:
            readable, w, e = select.select([sat_socket, web_socket], [], [],
                                           1000)

            for s in readable:
                with s.accept()[0] as connection:
                    request = network.recvPackage(connection)
                    if s is sat_socket:
                        Terran_Base.handleRequest(request, connection)
                    if s is web_socket:
                        Terran_Base.handleWebRequest(request, connection)

except KeyboardInterrupt:
    sys.exit(0)

finally:
    print('Protocolo de autodestrucción iniciado!')
    os.unlink(sat_address)
    os.unlink(web_address)
