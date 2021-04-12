#! /usr/bin/env python3
from threading import Thread

import gi
import sys
import os
from time import sleep

gi.require_version("Gst", "1.0")
from gi.repository import Gst, GLib
Gst.init(sys.argv[1:])


def isVideo(element):
    return True if element.startswith("video") else False

def getCamsAndPipes():
    cams = filter(isVideo, os.listdir("/dev/")) # gets list of video devices if isVideo finds them in os list
    pipelines = []

    for i, cam in enumerate(cams):
        pipStr = 'v4l2src device="/dev/{}" !  video/x-raw,width=640,height=480 ! jpegenc ! rtpjpegpay !  udpsink host=192.168.2.255 port=5{}00'.format(cam, i)

        # print(pipStr)

        pipeline = Gst.parse_launch(pipStr)
        pipelines.append(pipeline)

    for pipeline in pipelines:
        if not pipeline:
            print("pipeline error")
            sys.exit(1)

    return pipelines

def cleanPipelins(pipelines):
    for i, pipe in enumerate(pipelines):
        pipe.set_state(Gst.State.NULL)
        print("- pipeline " + str(i) + " resetting to null")

def startPipes(pipelines = getCamsAndPipes()):


    for i, pipeline in enumerate(pipelines):
        ret = pipeline.set_state(Gst.State.PLAYING)
        if ret == Gst.StateChangeReturn.FAILURE:
            print("pipeline {} couldn't started.".format(i))
        else:
            print("pipeline {} started.".format(i))

    return pipelines
            
def mainloop(pipes):
    while True:
        sleep(0.01)
        # checkStates(pipes)


main_loop = GLib.MainLoop()
thread = Thread(target=main_loop.run, daemon=True)


try:
    thread.start()
    pipes = startPipes()
    mainloop(pipes)
    
except KeyboardInterrupt:
    print("\nexiting...")

finally:
    cleanPipelins(pipes)
    main_loop.quit()
    exit(0)