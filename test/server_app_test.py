import unittest
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from test.tempdir import Tempdir
from socket_server import ServerApp
from socket_server import Server


class MyServer(Server):
    pass


class TestStringMethods(unittest.TestCase):

    def test_start_stop_server(self):
        with Tempdir(prefix="Test_", remove=True) as td:
            app = ServerApp(MyServer, work_dir=td)
            status_1 = app.status()
            self.assertEqual(status_1.status, "NOT RUNNING")

            app.start()
            status_2 = app.status()
            self.assertEqual(status_2.status, "RUNNING")

            app.stop()

            status_3 = app.status()
            self.assertEqual(status_3.status, "NOT RUNNING")


if __name__ == '__main__':
    unittest.main()
