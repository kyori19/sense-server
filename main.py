import json
import os
import socket
import threading
import time

BIND = '0.0.0.0'
PORT = int(os.environ.get('PORT'))

pool = {}


def message(obj):
    return bytes(json.dumps(obj), 'utf-8')


def handler(client: socket.socket):
    pid = None
    while True:
        req = client.recv(1024)
        obj = json.loads(req)
        print(f'[R] {obj}')

        cid = obj['id']
        if cid < 0 or cid > 3:
            client.send(message({'ok': False, 'message': 'Invalid ID'}))
            continue

        if cid != pid:
            if cid in pool:
                if time.time() - pool[cid]['last'] > 5:
                    print(f'Client {pid} disconnected')
                    del pool[cid]
                    print(f'Released ID {cid}')
                else:
                    client.send(message({'ok': False, 'message': 'Duplicated ID'}))
                    continue

            if pid is not None:
                del pool[pid]
                print(f'Released ID {pid}')

            pid = cid
            pool[pid] = {'client': client}
            print(f'Accepted ID {pid}')

        pool[pid]['last'] = time.time()
        client.send(message({'ok': True}))


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
