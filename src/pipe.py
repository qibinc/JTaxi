import json
import subprocess


class Pipe(object):

    def __init__(self, path):
        self.subproc = subprocess.Popen(
            [path], stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)

    def send(self, data):
        self.subproc.stdin.write(json.dumps(data) + '\n')
        self.subproc.stdin.flush()

    def recv(self):
        stdout = self.subproc.stdout.readline()
        data = json.loads(stdout)
        return data
