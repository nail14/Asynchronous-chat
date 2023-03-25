import unittest
from client import socket_init, socket_connect, make_json_byte_presence, get_args
import json


class TestClient(unittest.TestCase):

    def test_socket_init(self):
        s = socket_init()
        self.assertEqual(str(s),
                         "<socket.socket fd=3, "
                         "family=AddressFamily.AF_INET, "
                         "type=SocketKind.SOCK_STREAM, "
                         "proto=0, "
                         "laddr=('0.0.0.0', 0)>")
        s.close()

    def test_make_json_byte_presence(self):
        presence = json.loads(make_json_byte_presence().decode('unicode_escape'))
        presence['time'] = None
        self.assertEqual(presence, {
            "action": "presence",
            "time": None,
            "type": "status",
            "user": {
                "account_name": "test_user",
                "status": "online",
            }
    })

    def test_get_args(self):
        self.assertEqual(get_args(['', '127.0.0.2', '7979']), ('127.0.0.2', 7979))

    def test_get_args_no_port(self):
        self.assertEqual(get_args(['', '127.0.0.2']), ('127.0.0.2', 7777))

    def test_get_args_no_address(self):
        self.assertEqual(get_args(['']), ('', 7777))


if __name__ == "__main__":
    unittest.main()