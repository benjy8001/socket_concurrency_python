from socket import (
    socket,
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR
)
from select import select

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

def conn_sock_readline(conn_s):
    line = b''
    while True:
        c = conn_s.recv(1)
        if c == b'':
            conn_s.close()
            conn_sockets.remove(conn_s)
            break
        line += conn_s
        if c == b'\n':
            send_line(conn_s, line)
            break

def main():
    server_sock = create_server_sock()
    while True:
        fds = tuple(conn_sockets) + (server_sock,)
        r, w, e = select(fds, [], [])
        fd = r[0]
        if fd == server_sock:
            conn_s, addr = server_sock.accept()
            conn_sockets.append(conn_s)
        else:
            conn_sock_readline(fd)

main()
