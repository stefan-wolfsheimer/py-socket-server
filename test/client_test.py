import unittest
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from test.tempdir import Tempdir
from test.server_app_test import MyServer
from socket_server import ServerApp
from socket_server import Client


class TestStringMethods(unittest.TestCase):
    def test_timeout(self):
        socket_file = "/path/to/nothing.socket"
        client = Client(socket_file, conn_trials=3)
        with self.assertRaises(Exception):
            client.connect()

    def test_client(self):
        with Tempdir(prefix="Test_", remove=False) as td:
            app = ServerApp(MyServer, work_dir=td)
            status_1 = app.status()
            self.assertEqual(status_1.status, "NOT RUNNING")
            app.start()

            client = Client(app.socket_file)
            self.assertEqual(client.request('msg'), '1 msg')
            self.assertEqual(client.request('msg'), '2 msg')
            self.assertEqual(client.request('msg'), '3 msg')

            status_2 = app.status()
            self.assertEqual(status_2.status, "RUNNING")

            app.stop()

            status_3 = app.status()
            self.assertEqual(status_3.status, "NOT RUNNING")


if __name__ == '__main__':
    unittest.main()
