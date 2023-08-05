import pytest
from mock import patch


@patch('socket.socket')  # Patch the class
def recv():
    with open("data/probe_response.xml", "rb") as resp:
        return resp.read()



import socket
s = socket.socket()
print(s.recv)
