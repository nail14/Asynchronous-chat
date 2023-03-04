import time
import json
import sys
from log.config_client_log import client_logger, log


@log
def socket_init():
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_logger.info('init ok')
    return client_socket
def socket_connect(client_socket, address, port):
    client_socket.connect((address, port))
    presence = make_json_byte_presence()
    client_socket.send(presence)
    response = client_socket.recv(1024).decode('unicode_escape')
    client_socket.close()
    client_logger.info(f'connect {address=} {port=} send={presence}')
    return response
def make_json_byte_presence():
    presence = {
        "action": "presence",
        "time": time.time(),
        "type": "status",
        "user": {
            "account_name": "test_user",
            "status": "online",
        }
    }
    return json.dumps(presence).encode('unicode_escape')
def get_args(args):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('address', type=str, default='', help="address to connect")
    parser.add_argument('port', nargs='?', type=int, default=7777, help="port to connect")
    result = parser.parse_args(args)
    return result.address, result.port
def main():
    args = sys.argv
    address, port = get_args(args[1:])
    client_socket = socket_init()
    server_response = socket_connect(client_socket, address, port)
    client_logger.info(f'{server_response=}')
if __name__ == '__main__':
    try:
        main()
    except Exception:
        client_logger.critical(f'failed to connect to server')