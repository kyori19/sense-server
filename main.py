import os
import socket
import threading

BIND = '0.0.0.0'
PORT = int(os.environ.get('PORT'))


def handler(client: socket.socket):
    while True:
        req = client.recv(1024)
        print(f'[R] {req}')
        client.send(bytes('Accepted\n', 'utf-8'))


def loop(server: socket.socket):
    client, addr = server.accept()
    print(f'New connection accepted @ {addr[0]}:{addr[1]}')
    thread = threading.Thread(target=handler, args=(client,))
    thread.start()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((BIND, PORT))
    server.listen(5)
    print(f'Started server @ {BIND}:{PORT}')
    while True:
        loop(server)


if __name__ == '__main__':
    main()
