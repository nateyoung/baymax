#!/usr/bin/python3

import mumbleClient
import snowboyClient
import time
import queue
import pyaudio
#from . import mumbleAudio


if __name__ == '__main__':
    # create 1 PyAudio instance and share it among threads
    audio = pyaudio.PyAudio()

    # create input and output streams to be shared across threads
    CHUNK = 2048
    FORMAT = pyaudio.paInt16
    #FORMAT = 8
    CHANNELS = 1
    RATE = 16000

    #inputStream = audio.open(
    #    input=True, output=False,
    #    format=FORMAT,
    #    channels=CHANNELS,
    #    rate=RATE,
    #    frames_per_buffer=CHUNK)

    #outputStream = audio.open(format=FORMAT,
    #                channels=CHANNELS,
    #                rate=RATE,
    #                output=True,
    #                frames_per_buffer=CHUNK)

    # create mumble client for communicating with murmur server & other devices
    mumble_q = queue.Queue()
    #mc = mumbleClient.mumbleClient(mumble_q, audio)
    #mc.setDaemon(True)
    #mc.start()


    # create snowboy instance to listen for trigger word, then control mumble client appropriately
    sc = snowboyClient.snowboyClient(["Baymax.pmdl","Baymax_tucker.pmdl"],"google", mumble_q, audio)
    sc.setDaemon(True)
    sc.start()

    # run forever
    while True: time.sleep(0.1)


