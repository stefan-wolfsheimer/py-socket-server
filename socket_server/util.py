import struct


class ReturnCode(object):
    OK = 0
    ERROR = 1
    UNDEFINED = 2
    STOPPED = 3

    @staticmethod
    def to_string(code):
        if code == ReturnCode.OK:
            return "OK"
        elif code == ReturnCode.ERROR:
            return "ERROR"
        elif code == ReturnCode.UNDEFINED:
            return "UNDEFINED"
        elif code == ReturnCode.STOPPED:
            return "STOPPED"


def recvall(socket, count):
    ret = b''
    while count:
        data = socket.recv(count)
        if not data:
            raise EOFError()
        ret += data
        count -= len(data)
    return ret


def send_message(socket, data, code=ReturnCode.OK):
    length = len(data)
    socket.sendall(struct.pack('!II', length, code))
    socket.sendall(data)


def recv_message(socket):
    lengthbuf = recvall(socket, 8)
    length, code = struct.unpack('!II', lengthbuf)
    return (code, recvall(socket, length))
