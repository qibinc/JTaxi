import time
import json
import subprocess
from multiprocessing import Process, Queue
from queue import Empty
import numpy as np


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
