# ###################### FX ##################
# def resetPipelins(pipelines):
#     for i in range(5):
#         pipelines[i].set_state(Gst.State.NULL)


# def startPipelines(pipelines):
#     failed = 0
#     first_run = True
#     runningPipes = []

#     while failed > 4 or first_run:
#         failed = 0

#         if not first_run:
#             resetPipelins(pipelines)
#             sleep(1)

#         for i, pipeline in enumerate(pipelines):
#             stateReturn = pipeline.set_state(Gst.State.PLAYING)
#             if stateReturn == Gst.StateChangeReturn.FAILURE:
#                 print("- Pipline {} failed".format(i))
#                 failed += 1
#             elif stateReturn == Gst.StateChangeReturn.ASYNC:
#                 print("- Pipline {} succeeded".format(i))
#                 runningPipes.append(pipeline)


#         print("- trial ended with " + str(failed) + " failed cams.")

#         first_run = False

#     return runningPipes

# def checkStates(pipelines):
#     for pipeline in pipelines:
#         _, state, _ = pipeline.get_state(timeout=10*Gst.SECOND)
#         if state != Gst.State.PLAYING:
#             startPipelines([pipeline])
#             print("Pipline stopped !!!!!!1")
#             break

# def mainloop(pipelines):
#     while True:
#         sleep(5)
#         checkStates(pipelines)


# ###################### create elemenst ##################
# pipStr0 = 'v4l2src device="/dev/video0" !  video/x-raw,width=640,height=480 ! jpegenc ! rtpjpegpay !  udpsink host=192.168.2.1 port=5000'
# pipStr1 = 'v4l2src device="/dev/video1" !  video/x-raw,width=640,height=480 ! jpegenc ! rtpjpegpay !  udpsink host=192.168.2.1 port=5100'
# pipStr2 = 'v4l2src device="/dev/video2" !  video/x-raw,width=640,height=480 ! jpegenc ! rtpjpegpay !  udpsink host=192.168.2.1 port=5200'
# pipStr3 = 'v4l2src device="/dev/video3" !  video/x-raw,width=640,height=480 ! jpegenc ! rtpjpegpay !  udpsink host=192.168.2.1 port=5300'
# pipStr4 = 'v4l2src device="/dev/video4" !  video/x-raw,width=640,height=480 ! jpegenc ! rtpjpegpay !  udpsink host=192.168.2.1 port=5400'


# pipelines = [
#     Gst.parse_launch(pipStr0),
#     Gst.parse_launch(pipStr1),
#     Gst.parse_launch(pipStr2),
#     Gst.parse_launch(pipStr3),
#     Gst.parse_launch(pipStr4)
# ]

# ###################### Running piplines ##################
# runningPipes = startPipelines(pipelines)


# ###################### Main loop ##################
# while True:
#     try:
#         mainloop(runningPipes)
#     except KeyboardInterrupt:
#         break


# print("\n- Terminating")
# resetPipelins(pipelines)


#! /usr/bin/env python3
from threading import Thread

import gi
import sys
import os
from time import sleep

gi.require_version("Gst", "1.0")

from gi.repository import Gst, GLib

def mainloop():
    while True:
        sleep(0.01)

def isVideo(element):
    return True if element.startswith("video") else False

def cleanPipelins(pipelines):
    for i, pipe in enumerate(pipelines):
        pipe.set_state(Gst.State.NULL)
        print("- pipeline " + str(i) + " resetting to null")

def startPipes():
    cams = filter(isVideo, os.listdir("/dev/")) # gets list of video devices if isVideo finds them in os list
    pipelines = []
    print(cams)

    for i, cam in enumerate(cams):
        pipStr = 'v4l2src device="/dev/{}" !  video/x-raw,width=640,height=480 ! jpegenc ! rtpjpegpay !  udpsink host=192.168.2.255 port=5{}00'.format(cam, i)
        print(pipStr)

        pipeline = Gst.parse_launch(pipStr)
        pipelines.append(pipeline)

    for pipeline in pipelines:
        if not pipeline:
            print("pipeline error")
            sys.exit(1)

    for i, pipeline in enumerate(pipelines):
        ret = pipeline.set_state(Gst.State.PLAYING)
        if ret == Gst.StateChangeReturn.FAILURE:
            print("Unable to set pipeline {} to the playing state.".format(i))
        else:
            print("pipeline {} started.".format(i))

    return pipelines

Gst.init(sys.argv[1:])

main_loop = GLib.MainLoop()
thread = Thread(target=main_loop.run)
thread.start()


pipes = startPipes()

try:
    mainloop()
except KeyboardInterrupt:
    print("exiting")
    pass


cleanPipelins(pipes)
main_loop.quit()