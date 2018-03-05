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

sat_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sat_socket.setblocking(0)

print('Abriendo canal de comunicaciones satelital %s' % sat_address)

web_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
web_socket.setblocking(0)

print('Abriendo canal de comunicaciones web %s' % web_address)

sat_socket.bind(sat_address)
web_socket.bind(web_address)

sat_socket.listen(1)
web_socket.listen(1)

print(r"""
,--..Y    
\   /`.   
 \.    \
  :::--' 
""")

print('Esperando conexiones de satelites')

checkSatelites = 0

try:
    while True:
        readable, w, e = select.select([sat_socket, web_socket], [], [], 1000)
        for s in readable:
            if s is sat_socket:
                connection, client_address = s.accept()

                request = network.recvPackage(connection)

                Terran_Base.handleRequest(request, connection)

                connection.close()

            if s is web_socket:
                connection, client_address = s.accept()

                request = network.recvPackage(connection)

                Terran_Base.handleWebRequest(request, connection)

                connection.close()
        
        if checkSatelites > 10:
            Terran_Base.cleanupOldSatelites()
            checkSatelites = 0

        checkSatelites += 1

except KeyboardInterrupt:
    sys.exit(0)

finally:
    print('Protocolo de autodestrucción iniciado!')
    web_socket.close()
    sat_socket.close()
    os.unlink(sat_address)
    os.unlink(web_address)
