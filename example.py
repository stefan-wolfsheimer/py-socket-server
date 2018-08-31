import os
import sys
import json
from socket_server import ServerApp
from socket_server import Client
from socket_server import Server
from socket_server import ReturnCode
from argparse import ArgumentParser


def do_put(argv=sys.argv[1:]):
    parser = ArgumentParser(description='Put a key value pair')
    parser.add_argument("key", type=str, help="key")
    parser.add_argument("value", type=str, help="value")
    parser.add_argument("-v", "--verbose", action='store_true',
                        help="verbose logging")
    args = parser.parse_args()
    app = ServerApp(ExampleServer, verbose=args.verbose)
    app.start()
    client = Client(app.socket_file)
    req = {"op": "put",
           "key": args.key,
           "value": args.value}
    code, result = client.request(json.dumps(req))
    if code == ReturnCode.OK:
        print(result)
    else:
        print(result)
        raise ValueError("failed: %s" %
                         ReturnCode.to_string(code))


def do_get(argv=sys.argv[1:]):
    parser = ArgumentParser(description='Get a value')
    parser.add_argument("key", type=str, help="key")
    parser.add_argument("-v", "--verbose", action='store_true',
                        help="verbose logging")
    args = parser.parse_args()
    app = ServerApp(ExampleServer, verbose=args.verbose)
    app.start()
    client = Client(app.socket_file)
    req = {"op": "get",
           "key": args.key}
    code, result = client.request(json.dumps(req))
    if code == ReturnCode.OK:
        print(result)
    else:
        print(result)
        raise ValueError("failed: %s" %
                         ReturnCode.to_string(code))


class ExampleServer(Server):
    def __init__(self, **kwargs):
        super(ExampleServer, self).__init__(**kwargs)
        self.db_file = os.path.join(os.path.expanduser("~"),
                                    'ExampleServer')
        if os.path.isfile(self.db_file):
            with open(self.db_file, "r") as fp:
                self.data = json.load(fp)
        else:
            self.data = {}

    def process(self, code, msg):
        obj = json.loads(msg)
        if obj.get('op') == 'put':
            self.data[obj.get('key')] = obj.get('value')
            return (ReturnCode.OK, "")
        elif obj.get('op') == 'get':
            k = obj.get('key')
            if k in self.data:
                return (ReturnCode.OK, self.data.get(k))
            else:
                return (ReturnCode.UNDEFINED, "")

    def tear_down(self):
        with open(self.db_file, "w") as fp:
            json.dump(self.data, fp)
