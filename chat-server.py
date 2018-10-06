from socket import (
    socket,
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR
)
from threading import Thread

conn_sockets = []


def send_line(sender, line):
    for recv_s in conn_sockets:
        recv_s.send(line)


def create_server_sock():
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(('', 5555))
    s.listen(0)
    return s


def conn_sock_manager(conn_s):
    conn_sockets.append(conn_s)
    line = b''
    while True:
        c = conn_s.recv(1)
        if c == b'':
            break
        line += c
        if c == b'\n':
            send_line(conn_s, line)
            line = b''
    conn_s.close()
    conn_sockets.remove(conn_s)


def server_sock_manager():
    s = create_server_sock()
    while True:
        conn_s, addr = s.accept()
        t = Thread(target=conn_sock_manager, args=(conn_s,))
        t.start()


server_sock_manager()
