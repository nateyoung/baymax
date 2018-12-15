
# references:
# https://github.com/ranomier/pymumble-abot/blob/master/abot.py
# https://github.com/azlux/botamusique/blob/master/mumbleBot.py
# https://github.com/azlux/pymumble/blob/pymumble_py3/API.md
from threading import Thread
import pymumble.pymumble_py3 as pymumble
import wave
import time
import pyaudio

class mumbleAudio(Thread):
    # flag to control whether to send audio to server or not
    muted = 1

    def mute(self):
        print("muting")
        self.muted = 1

    def unmute(self):
        print("unmuting")
        self.muted = 0

    def __init__(self):
        Thread.__init__(self)

        print("hello from mumbleAudio")
        self.mumble = pymumble.Mumble("192.168.1.67", user="baymax", port=64738, password="baymax")
                                      #debug=self.config.getboolean('debug', 'mumbleConnection'),
                                      #certfile=args.certificate)

        self.mumble.start()  # start the mumble thread
        self.mumble.is_ready()  # wait for the connection
        #self.mumble.set_comment()
        self.mumble.users.myself.unmute()
        #self.mumble.channel.send_message("hello world")
        #channel = self.mumble.channels[0]
        #channel.send_message("hello world")
        #self.mumble.channels[0].Channel.move_in(session="dvr")
        #self.mumble.send_message(PYMUMBLE_MSG_TYPES_TEXTMESSAGE,"hello world")
        #user = self.mumble.users[1]
        #user.send_message("hello world")
        #print(user)

    def run(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 48000

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        #input_device_index = 1,
                        frames_per_buffer=CHUNK)
        print("* recording")
        frames = []

        #for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        while True:
            if self.muted==0:
                if stream.is_stopped():
                    stream.start_stream()

                self.mumble.sound_output.add_sound(stream.read(CHUNK))  # send a piece of audio to mumble
            else:
                stream.stop_stream()
                time.sleep(0.1)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

#if __name__ == '__main__':
#    args = ""
#    myMumble = mumbleAudio()

