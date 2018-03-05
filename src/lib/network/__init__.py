import pickle
import sys


def encodeForNetwork(obj):
    serialized = pickle.dumps(obj, pickle.HIGHEST_PROTOCOL)
    length = len(serialized).to_bytes(32, sys.byteorder)

    return bytearray(length) + serialized


def recvPackage(connection):
    length = int.from_bytes(connection.recv(32), sys.byteorder, signed=False)

    if length > 0:
        response = bytes()
        chunk = bytes()

        while len(chunk) < length:
            chunk = connection.recv(4096)
            response += chunk

        return decodeForNetwork(response)
    return {}


def decodeForNetwork(response):
    return pickle.loads(response)
