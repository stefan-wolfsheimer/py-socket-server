import logging
import socket
import time
import struct


def recvall(socket, count):
    ret = b''
    while count:
        data = socket.recv(count)
        if not data:
            raise EOFError()
        ret += data
        count -= len(data)
    return ret


def send_message(socket, data):
    length = len(data)
    socket.sendall(struct.pack('!I', length))
    socket.sendall(data)


def recv_message(socket):
    lengthbuf = recvall(socket, 4)
    length, = struct.unpack('!I', lengthbuf)
    return recvall(socket, length)


class Client(object):
    def __init__(self, socket_file,
                 conn_trials=10,
                 reconnect_timeout=1,
                 logger=logging.getLogger("Client")):
        self.socket_file = socket_file
        self.conn_trials = conn_trials
        self.reconnect_timeout = reconnect_timeout
        self.logger = logger

    def request(self, msg):
        sock = self.connect()
        send_message(sock, msg)
        response = recv_message(sock)
        sock.close()
        return response

    def connect(self):
        trials = self.conn_trials
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        while trials > 0:
            trials -= 1
            try:
                sock.connect(self.socket_file)
                return sock
            except Exception:
                if trials == 0:
                    self.logger.error("failed to connect to socket %s",
                                      self.socket_file)
                    raise
                else:
                    self.logger.warning("failed to connect to socket %s " +
                                        "(trying again %d/%d)",
                                        self.socket_file,
                                        self.conn_trials - trials,
                                        self.conn_trials)
                    time.sleep(self.reconnect_timeout)
