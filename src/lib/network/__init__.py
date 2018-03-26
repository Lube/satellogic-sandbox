import pickle
import sys


def encodeForNetwork(obj):
    serialized = pickle.dumps(obj, pickle.HIGHEST_PROTOCOL)
    length = len(serialized).to_bytes(32, sys.byteorder)

    return bytearray(length) + serialized


def recv(connection):
    cLength = connection.recv(32)

    length = int.from_bytes(cLength, sys.byteorder, signed=False)

    if length > 0:
        response = bytes()
        chunk = bytes()

        while len(response) < length:
            chunk = connection.recv(4096)
            response += chunk

        return decodeForNetwork(response)
    return {}


def decodeForNetwork(response):
    return pickle.loads(response)
