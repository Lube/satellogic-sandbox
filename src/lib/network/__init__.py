import pickle
import sys


def encodeForNetwork(obj):
    serialized = pickle.dumps(obj, pickle.HIGHEST_PROTOCOL)
    length = len(serialized).to_bytes(32, sys.byteorder)

    return bytearray(length) + serialized


def recvPackage(connection, loop=None):
    if loop is None:
        cLength = loop.sock_recv(connection, 32)
    else:
        cLength = yield from loop.sock_recv(connection, 32)

    length = int.from_bytes(cLength, sys.byteorder, signed=False)

    if length > 0:
        response = bytes()
        chunk = bytes()

        while len(chunk) < length:
            chunk =  yield from loop.sock_recv(connection, 4096)
            response += chunk

        return decodeForNetwork(response)
    return {}


def decodeForNetwork(response):
    return pickle.loads(response)
