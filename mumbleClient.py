# -*- coding: utf-8 -*-
from threading import Thread
import queue


class mumbleClient(Thread):

    def __init__(self,mumble_q):
        Thread.__init__(self)
        self.mumble_q = mumble_q

    def run(self):
        print("hello from mumbleClient")
        # queue/thread code taken from https://eli.thegreenplace.net/2011/12/27/python-threads-communication-and-stopping
        # As long as we weren't asked to stop, try to take new tasks from the
        # queue. The tasks are taken with a blocking 'get', so no CPU
        # cycles are wasted while waiting.
        # Also, 'get' is given a timeout, so stoprequest is always checked,
        # even if there's nothing in the queue.
        while True:
            try:
                self.command = self.mumble_q.get(True, 0.05)
                print("Received command:", self.command)
            except queue.Empty:
                continue
