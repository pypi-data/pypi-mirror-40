import socket
from unittest import TestCase

from testfixtures import ShouldRaise

from sockpuppet.ports import find_free_port, wait_for_server
from .helpers import WithServer


class TestFindFreePort(TestCase):

    def test_simple(self):
        port = find_free_port()
        s = socket.socket()
        s.bind(('127.0.0.1', port))
        s.close()

    def test_address_specified(self):
        port = find_free_port('127.0.0.1')
        s = socket.socket()
        s.bind(('127.0.0.1', port))
        s.close()


class TestWaitForServer(WithServer, TestCase):

    def test_there(self):
        self.start_server(self.port)
        wait_for_server(self.port)

    def test_not_there(self):
        with ShouldRaise(AssertionError(
            'server on 127.0.0.1:%s did not start within 0.01s' % self.port
        )):
            wait_for_server(self.port, timeout=0.01, poll_frequency=0.01)

    def test_address_specified(self):
        self.start_server(self.port)
        wait_for_server(self.port, '127.0.0.1')

    def test_other_socket_error(self):
        with ShouldRaise(socket.gaierror):
            wait_for_server(-1)
