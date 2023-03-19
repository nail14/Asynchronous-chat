from socket import *
import time
import sys
import json
from log.config_server_log import server_logger, log
import select
from PortDescriptor import PortDescriptor


class Server:
    port = PortDescriptor("port")

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.socket = self.non_blocking_socket()
        self.clients = {}
        self.connections = []
        server_logger.info(f'init successful {address}')
    def start(self):
        server_logger.info('server started')
        while True:
            try:
                connection, address = self.socket.accept()
            except OSError as e:
                pass
            else:
                print("Получен запрос на соединение с %s" % str(address))
                self.connections.append(connection)
            finally:
                wait = 10
                w, r = [], []
                try:
                    r, w, e = select.select(self.connections, self.connections, [], wait)
                except Exception as ex:
                    pass
                requests = self.read_requests(r)
                if requests:
                    self.write_responses(requests, w)
    @staticmethod
    def get_answer(action=None):
        if action == 'presence':
            return {
                "response": 200,
                "alert": "ok",
            }
        return {
                "response": 400,
                "alert": "bad request",
            }
    @staticmethod
    def decode_message(raw):
        try:
            client_message = raw.decode('unicode_escape')
            return json.loads(client_message)
        except Exception:
            server_logger.error(f'failed to decode message: {raw}')
        return None

    def non_blocking_socket(self):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind((self.address, self.port))
        sock.listen(5)
        sock.settimeout(0.2)
        return sock
    def analyse_response(self, responses: dict):
        try:
            for key in responses:
                decoded_message = responses[key]
                if decoded_message["action"] == "presence":
                    name = decoded_message["from"]["account_name"]
                    self.clients[key] = name
                    print(f'now on server: {self.clients.values()}')
        except Exception:
            pass
    def read_requests(self, clients):
        responses = {}
        for sock in clients:
            try:
                responses[sock] = json.loads(sock.recv(1024).decode('unicode_escape'))
                self.analyse_response(responses)
            except Exception as ex:
                server_logger.info(f'Клиент {sock.fileno()} {sock.getpeername()} отключился')
                sock.close()
                self.connections.remove(sock)
                self.clients.pop(sock)
        return responses
    def write_responses(self, requests, clients):
        for sock in clients:
            try:
                for request in requests.values():
                    try:
                        print(f'{self.clients[sock]=} {request["from"]["account_name"]=} {request["message"]}')
                        if request["mess_to"] in ['', self.clients[sock]] and \
                                request["from"]["account_name"] != self.clients[sock]:
                            response = json.dumps(request).encode('unicode_escape')
                            sock.send(response)
                    except Exception:
                        pass
            except Exception as ex:
                server_logger.info(f'Клиент {sock.fileno()} {sock.getpeername()} отключился')
                sock.close()
                self.connections.remove(sock)
                self.clients.pop(sock)
def get_args(args):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', type=str, default='', help="socket address")
    parser.add_argument('-p', type=int, default=7777, help="socket port")
    result = parser.parse_args(args)
    return result.a, result.p


def main():
    socket_address, socket_port = get_args(sys.argv[1:])

    server = Server(socket_address, socket_port)
    print(server.port)
    server.start()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        server_logger.info('stopped by user')
    except Exception as ex:
        server_logger.error(f'failed to start server, {ex}')