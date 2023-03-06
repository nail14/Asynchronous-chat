from socket import *
import time
import sys
import json
from log.server_log_config import server_logger, log
import select


@log
def socket_init(address, port):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((address, port))
    s.listen(5)
    server_logger.info(f'init {address=} {port=}')
    return s
def get_answer(action=None):
    if action == 'presence':
        return {
            "response": 200,
            "alert": "Необязательное сообщение/уведомление",
        }
    return {
            "response": 400,
            "alert": "bad request",
        }
def decode_message(raw):
    try:
        client_message = raw.decode('unicode_escape')
        return json.loads(client_message)
    except Exception:
        server_logger.error(f'failed to decode message: {raw}')
    return None
def server_accept(s):
    while True:
        client, client_address = s.accept()
        client_message = decode_message(client.recv(1024))
        answer = get_answer(client_message['action'])
        server_logger.info(f'{client_message=}; {answer=}')
        client.send(json.dumps(answer).encode('unicode_escape'))
        client.close()
def get_args(args):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', type=str, default='', help="socket address")
    parser.add_argument('-p', type=int, default=7777, help="socket port")
    result = parser.parse_args(args)
    return result.a, result.p
def main():
    socket_address, socket_port = get_args(sys.argv[1:])
    server_socket = socket_init(socket_address, socket_port)
    server_accept(server_socket)


def non_blocking_socket(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(5)
    sock.settimeout(0.2)
    return sock


def read_requests(clients, all_clients):
    responses = {}

    for sock in clients:
        try:
            data = sock.recv(1024).decode('unicode_escape')
            responses[sock] = data
        except Exception as ex:
            print(f'Клиент {sock.fileno()} {sock.getpeername()} отключился')
            all_clients.remove(sock)
    return responses


def write_responses(requests, clients, all_clients):

    for sock in clients:
        try:
            for request in requests.values():
                response = request.encode('unicode_escape')
                sock.send(response)

        except Exception as ex:
            print(f'Клиент {sock.fileno()} {sock.getpeername()} отключился')
            sock.close()
            all_clients.remove(sock)


def main_non_blocking():
    socket_address = get_args(sys.argv[1:])

    clients = []
    server_socket = non_blocking_socket(socket_address)

    while True:
        try:
            connection, address = server_socket.accept()
        except OSError as e:
            pass
        else:
            print("Получен запрос на соединение с %s" % str(address))
            clients.append(connection)
        finally:
            wait = 10
            w, r = [], []
            try:
                r, w, e = select.select(clients, clients, [], wait)
            except Exception as ex:
                pass

            requests = read_requests(r, clients)
            if requests:
                write_responses(requests, w, clients)


if __name__ == '__main__':
    try:
        # main()
        main_non_blocking()
    except KeyboardInterrupt:
        server_logger.info('stopped by user')
    except Exception as ex:
        server_logger.critical(f'failed to start server, {ex}')