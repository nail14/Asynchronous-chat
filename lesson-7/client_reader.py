from socket import *


def echo_client():
    with socket(AF_INET, SOCK_STREAM) as sock:  # Создать сокет TCP
        sock.connect(('localhost', 7777))  # Соединиться с сервером
        while True:
            data = sock.recv(1024).decode('unicode_escape')
            if data:
                print('Ответ:', data)


if __name__ == '__main__':
    try:
        echo_client()
    except KeyboardInterrupt:
        print('Aborted by user')
    except Exception as ex:
        print(f'{ex}')