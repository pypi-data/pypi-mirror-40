import socket
import threading

from sockpuppet.ports import find_free_port


def simple_server(host, port):
    server_sock = socket.socket()
    server_sock.bind((host, port))
    server_sock.listen(0)
    server_sock.settimeout(1)
    server_sock.accept()
    server_sock.close()


class WithServer(object):

    def setUp(self):
        self.port = find_free_port()

    def start_server(self, port=None, host='127.0.0.1'):
        if port is None:
            port = self.port
        server_thread = threading.Thread(target=simple_server,
                                         args=(host, port))
        server_thread.start()
        self.addCleanup(server_thread.join)
