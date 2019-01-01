#!/usr/bin/python3

import mumbleClient
import snowboyClient
import time
import queue
import pyaudio
import collections
import audioop
#from . import mumbleAudio

class RingBuffer(object):
    """Ring buffer to hold audio from PortAudio"""

    def __init__(self, size=4096):
        self._buf = collections.deque(maxlen=size)

    def extend(self, data):
        """Adds data to the end of buffer"""
        self._buf.extend(data)

    def get(self):
        """Retrieves data from the beginning of buffer and clears it"""
        tmp = bytes(bytearray(self._buf))
        self._buf.clear()
        return tmp

def inputCallback(in_data, frame_count, time_info, status):
    snowboy_ring_buffer.extend(in_data)

    # need to convert formats - snowboy is 16 kHz, mumble is 48 kHz
    cvstate = None
    newdata, cvstate = audioop.ratecv(
        in_data, 2, 1, 16000,
        48000, cvstate)

    mumble_ring_buffer.extend(newdata)
    play_data = chr(0) * len(in_data)
    return play_data, pyaudio.paContinue

if __name__ == '__main__':
    # create 1 PyAudio instance and share it among threads
    audio = pyaudio.PyAudio()

    # create input and output streams to be shared across threads
    CHUNK = 2048
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    #RATE = 48000

    snowboy_ring_buffer = RingBuffer(CHANNELS * RATE * 5)
    mumble_ring_buffer = RingBuffer(CHANNELS * 48000 * 5)

    # there can only be 1 input stream, so init here as callback, then write received audio to ring buffers for mumble and
    # snowboy inputs.
    inputStream = audio.open(
        input=True, output=False,
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        frames_per_buffer=CHUNK,
        stream_callback=inputCallback)

    # create mumble client for communicating with murmur server & other devices
    mumble_q = queue.Queue()
    mc = mumbleClient.mumbleClient(mumble_q, mumble_ring_buffer)
    mc.setDaemon(True)
    mc.start()


    # create snowboy instance to listen for trigger word, then control mumble client appropriately
    sc = snowboyClient.snowboyClient(["Baymax.pmdl","Baymax_tucker.pmdl"],"google", mumble_q, snowboy_ring_buffer )
    sc.setDaemon(True)
    sc.start()

    # run forever
    while True: time.sleep(0.1)


