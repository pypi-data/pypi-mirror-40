import shlex
import socket
from subprocess import check_output, CalledProcessError, STDOUT
from unittest import TestCase

from testfixtures import compare

from .helpers import WithServer


class TestCLI(WithServer, TestCase):

    def cmd(self, cmd, expected_returncode=0):
        try:
            output = check_output(shlex.split(cmd), stderr=STDOUT)
        except CalledProcessError as e:
            output = e.output
            rc = e.returncode
        else:
            rc = 0
        if rc != expected_returncode: # pragma: no cover
            self.fail('for %r, rc expected %i but was %i:\n%s' % (
                cmd, expected_returncode, rc, output
            ))
        return output.decode('ascii')

    def test_defaults(self):
        self.start_server()
        output = self.cmd('sockpuppet wait --port '+str(self.port))
        compare(output, expected='server on 127.0.0.1:%i is up\n' % self.port)

    def test_explicit(self):
        host = socket.gethostname()
        self.start_server(host=host)
        output = self.cmd((
            'sockpuppet wait --address %s --port %s '
            '--timeout 4 --poll-frequency 0.1'
            ) % (host, self.port))
        compare(output, expected='server on %s:%i is up\n' % (host, self.port))

    def test_timeout(self):
        output = self.cmd(
            'sockpuppet wait --timeout 0.05 --port '+str(self.port),
            expected_returncode=1
        )
        compare(output, expected='server on 127.0.0.1:%i '
                                 'did not start within 0.05s\n' % self.port)
