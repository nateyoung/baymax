#!/usr/bin/python3

import mumbleClient
import snowboyClient
import time
import queue
#from . import mumbleAudio


if __name__ == '__main__':
    # create mumble client for communicating with murmur server & other devices
    mumble_q = queue.Queue()
    mc = mumbleClient.mumbleClient(mumble_q)
    mc.setDaemon(True)
    mc.start()


    # create snowboy instance to listen for trigger word, then control mumble client appropriately
    sc = snowboyClient.snowboyClient(["Baymax.pmdl","Baymax_tucker.pmdl"],"google", mumble_q)
    sc.setDaemon(True)
    sc.start()

    # run forever
    while True: time.sleep(0.1)


