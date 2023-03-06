import unittest
from server import socket_init, get_answer, decode_message, server_accept, get_address, get_port


class TestServer(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self) -> None:
        pass

    def test_get_address_no_value(self):
        self.assertEqual(get_address([]), 'localhost')

    def test_get_address_value(self):
        self.assertEqual(get_address(['', '-a', '127.0.0.2']), '127.0.0.2')

    def test_get_address_bad_value(self):
        self.assertEqual(get_address(['', '-p', '8888']), 'localhost')

    def test_get_address_with_port(self):
        self.assertEqual(get_address(['', '-a', '127.0.0.2', '-p', '7979']), '127.0.0.2')

    def test_get_port_no_value(self):
        self.assertEqual(get_port([]), 7777)

    def test_get_port_value(self):
        self.assertEqual(get_port(['', '-p', '7979']), 7979)

    def test_get_port_bad_value(self):
        self.assertEqual(get_port(['', '-P', '8888']), 7777)

    def test_get_port_with_port(self):
        self.assertEqual(get_port(['', '-a', '127.0.0.2', '-p', '7979']), 7979)

    def test_socket_init(self):
        s = socket_init('localhost', 7777)
        self.assertEqual(str(s),
                         "<socket.socket fd=3, "
                         "family=AddressFamily.AF_INET, "
                         "type=SocketKind.SOCK_STREAM, "
                         "proto=0, "
                         "laddr=('127.0.0.1', 7777)>")
        s.close()

    def test_get_answer_presence(self):
        self.assertEqual(get_answer('presence'), {
            "response": 200,
            "alert": "Необязательное сообщение/уведомление",
        })

    def test_get_answer_bad_value(self):
        self.assertEqual(get_answer('afsdfcxv'), {
            "response": 400,
            "alert": "bad request",
        })

    def test_decode_message(self):
        self.assertEqual(decode_message(b'{"head": "hello", "value": "5"}'), {'head': 'hello', 'value': '5'})


if __name__ == "__main__":
    unittest.main()