# -*- coding: utf-8 -*-
from threading import Thread
import queue
import mumbleAudio
import pyaudio

class mumbleClient(Thread):

    def __init__(self,mumble_q,mumble_ring_buffer):
        Thread.__init__(self)
        self.mumble_q = mumble_q

        self.ma = mumbleAudio.mumbleAudio(mumble_ring_buffer)
        self.ma.setDaemon(True)
        self.ma.start()

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
                if(self.command=="chat"):
                    self.ma.unmute()
                elif(self.command=="hangup"):
                    self.ma.mute()

            except queue.Empty:
                continue
