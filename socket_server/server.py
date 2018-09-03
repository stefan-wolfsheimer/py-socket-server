import logging
import threading
import os
import socket
import time
import json
import traceback
from util import send_message
from util import recv_message
from util import ReturnCode


class Server(object):
    """
    A basic server that accepts request via unix sockets
    """
    @classmethod
    def get_system_name(cls):
        return cls.__name__

    def __init__(self, socket_file, tick_sec=1,
                 is_daemon=True,
                 logger=logging.getLogger("Server")):
        self.socket_file = socket_file
        self.tick_sec = tick_sec
        self.socket = None
        self.logger = logger
        self.active = True
        self.listener_thread = threading.Thread(name='listener',
                                                target=self.listener,
                                                args=())
        self.listener_thread.setDaemon(is_daemon)

    def run(self):
        while self.active:
            time.sleep(self.tick_sec)
            self.tick()
        self.tear_down()
        self.logger.info("stopped")

    def tick(self):
        pass

    def tear_down(self):
        pass

    def start_listener(self):
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        if os.path.exists(self.socket_file):
            self.logger.info("remove old socket file %s", self.socket_file)
            os.remove(self.socket_file)
        self.logger.info("bind %s", self.socket_file)
        self.socket.bind(self.socket_file)
        self.listener_thread.start()

    def stop(self, signum=0, frame=None):
        self.logger.info("stop requested")
        self.active = False

    def listener(self):
        self.logger.info("listen")
        self.socket.listen(1)
        while True:
            self.logger.debug('waiting for a connection')
            conn, addr = self.socket.accept()
            self.logger.debug('accepted')
            try:
                code, data = recv_message(conn)
                self.logger.debug('recvall %s', data)
                if self.active:
                    try:
                        code, ret = self.process(code, data)
                        if isinstance(ret, dict):
                            ret = json.dumps(ret)
                        send_message(conn, ret, code)
                    except Exception as e:
                        msg = str(e) + "\n" + traceback.format_exc()
                        send_message(conn, msg, ReturnCode.ERROR)
                else:
                    msg = 'Server stopped'
                    send_message(conn, msg, ReturnCode.STOPPED)
            except Exception as e:
                msg = str(e) + "\n" + traceback.format_exc()
                send_message(conn, msg, ReturnCode.ERROR)
            finally:
                conn.close()

    def process(self, code, data):
        raise NotImplementedError('process not implemented')
