# -*- coding: utf-8 -*-

import snowboydecoder
from threading import Thread
import sys
import signal
import speech_recognition as sr
import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import queue

interrupted = False

class snowboyClient(Thread):

    def __init__(self,model,translator,mumble_q,audio):
        Thread.__init__(self)
        self.model = model
        self.translator = translator
        self.mumble_q = mumble_q
        self.audio = audio
        # capture SIGINT signal, e.g., Ctrl+C
        #signal.signal(signal.SIGINT, signal_handler)

    def run(self):
        self.detector = snowboydecoder.HotwordDetector(self.model, sensitivity=0.38)
        print("Listening... Press Ctrl+C to exit")

        # main loop
        self.detector.start(detected_callback=self.detectedCallback,
                       audio_recorder_callback=self.audioRecorderCallback,
                       interrupt_check=self.interrupt_callback,
                       silent_count_threshold=5,
                       sleep_time=0.03, audio=self.audio)

        self.detector.terminate()

    def signal_handler(signal, frame):
        global interrupted
        interrupted = True

    def say(self,command):
        #return 'espeak -v en-sc "' + command + '"'
        return 'espeak -v en-gb "' + command + '"'

    def parse_command(self,x):
        if(x=='chat'):
            self.mumble_q.put("chat")
        elif(x=='hang up'):
            self.mumble_q.put("hangup")
        else:
            choices = {
                'say hello'             : self.say("hello. i, am baymax, your pesonal household companion"),
                'what\'s the date'      : self.say("`date +\"%A %B %d %Y\"`"),
                'what is the date'      : self.say("`date +\"%A %B %d %Y\"`"),
                'what time is it'       : self.say("`date +\"%l %M\"`"),
                'what\'s the time'      : self.say("`date +\"%l %M\"`"),
                'tell a joke'           : self.say("`wget \"http://api.icndb.com/jokes/random\" -qO- | jshon -e value -e joke -u`"),
                }
            os.system(choices.get(x,self.say("i don\'t understand")))
#            return {
#                'say hello'             : os.system(self.say("hello. i, am baymax, your pesonal household companion")),
#                'what\'s the date'      : os.system(self.say("`date +\"%A %B %d %Y\"`")),
#                'what is the date'      : os.system(self.say("`date +\"%A %B %d %Y\"`")),
#                'what time is it'       : os.system(self.say("`date +\"%l %M\"`")),
#                'what\'s the time'      : os.system(self.say("`date +\"%l %M\"`")),
#                'tell a joke'           : os.system(self.say("`wget \"http://api.icndb.com/jokes/random\" -qO- | jshon -e value -e joke -u`")),
#                #'chat'                  : self.mumble_q.put("chat"),
#                #'hangup'                : self.mumble_q.put("hangup")
#
#            }.get(x,os.system(self.say("i don\'t understand")))

    def audioRecorderCallback(self,fname):
        commands = ['say hello', 'what\'s the date', 'what time is it']

        print("converting audio to text")
        r = sr.Recognizer()
        with sr.AudioFile(fname) as source:
            audioRec = r.record(source)  # read the entire audio file
            # recognize speech using Google Speech Recognition
            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                #print("trying google recognition")
                #print(r.recognize_google(audio))
                if(self.translator=="google"):
                    print("google listening")
                    text = r.recognize_google(audioRec)
                    print("fuzzy: ", process.extractOne(text, commands))
                else:
                    print("sphinx listening")
                    text = r.recognize_sphinx(audioRec)
                    print("fuzzy: ", process.extractOne(text, commands))

                print("I heard: " + text)
                self.parse_command(text)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

        os.remove(fname)



    def detectedCallback(self):
      snowboydecoder.play_audio_file(self.audio, snowboydecoder.DETECT_DING)
      sys.stdout.write("recording audio...")
      sys.stdout.flush()

    def signal_handler(signal, frame):
        global interrupted
        interrupted = True


    def interrupt_callback(arg1):
        global interrupted
        return interrupted


