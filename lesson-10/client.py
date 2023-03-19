from socket import *
import time
import json
import sys
from log.client_log_config import client_logger
from threading import Thread
import argparse


class Client:
    def __init__(self, address, login: str, send_to: str, mode: str):
        self.address = address
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect(self.address)
        self.login = login
        self.message_to = send_to
        self.mode = mode
        client_logger.info(f'client init successful {address}; login:{self.login}; send to:{self.message_to}')
        self.is_running = False

    def make_message(self, message=None):
        result = {
            "action": "msg",
            "time": time.time(),
            "from": {
                "account_name": self.login,
            },
            "mess_to": self.message_to,
            "message": message,
            "encoding": "unicode_escape",
        }
        return self.make_json(result)
    def make_presence(self):
        result = {
            "action": "presence",
            "time": time.time(),
            "from": {
                "account_name": self.login,
            },
        }
        return self.make_json(result)
    @staticmethod
    def make_json(string: dict):
        return json.dumps(string).encode('unicode_escape')
    def client_send(self, message):
        try:
            self.socket.send(message)
        except Exception:
            client_logger.error(f'failed to send')
    def client_receive(self):
        try:
            raw = self.socket.recv(1024).decode('unicode_escape')
            return json.loads(raw)
        except Exception as ex:
            pass

    def listener(self):
        while self.is_running:
            self.client_receiver()

    def user_interface(self):
        while self.is_running:
            self.client_sender()

    def client_sender(self):
        message = input('>>')
        if message:
            json_package = self.make_message(message=message)
            self.client_send(json_package)

    def client_receiver(self):
        response = self.client_receive()
        if response:
            if response["action"] == "msg":
                print(f"\n{response['from']['account_name']} says: {response['message']}\n>>", end='')

    @staticmethod
    def parse_response(response):
        return f"\n{response['from']} says: {response['message']}"

    def start(self):
        self.socket.send(self.make_presence())
        self.is_running = True

        if self.mode == 'r':
            self.client_receiver()
        elif self.mode == 's':
            self.client_sender()
        else:
            t1 = Thread(target=self.listener)
            t2 = Thread(target=self.user_interface)
            t1.start()
            t2.start()


def get_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-address', type=str, default='', help="address to connect")
    parser.add_argument('-port', type=int, default=7777, help="port to connect")
    parser.add_argument('-login', type=str, default='anonymous', help="your login")
    parser.add_argument('-to', type=str, default='', help="send to")
    parser.add_argument('-mode', type=str, default='', help="mode('r'=read, 's'=send, default=send/read)")
    result = parser.parse_args(args)

    return result.address, result.port, result.login, result.to, result.mode


def main():
    address, port, login, send_to, mode = get_args(sys.argv[1:])
    client = Client((address, port), login, send_to, mode)
    client.start()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        client_logger.info('stopped by user')
    except Exception as ex:
        client_logger.error(f'failed to connect to server')