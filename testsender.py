#!/usr/bin/env python3

###################### inits ##################
import gi
import sys
from time import sleep

gi.require_version("GLib", "2.0")
gi.require_version("GObject", "2.0")
gi.require_version("Gst", "1.0")

from gi.repository import Gst, GLib, GObject

Gst.init(sys.argv[1:])
first_run = True

###################### FX ##################
def resetPipelins(pipelines):
    for i in range(5):
        pipelines[i].set_state(Gst.State.NULL)


def startPipelines(pipelines):
    failed = 0
    global first_run
    runningPipes = []

    while failed > 4 or first_run:
        failed = 0

        if not first_run:
            resetPipelins(pipelines)
            sleep(1)

        for i, pipeline in enumerate(pipelines):
            stateReturn = pipeline.set_state(Gst.State.PLAYING)
            if stateReturn == Gst.StateChangeReturn.FAILURE:
                print("- Pipline {} failed".format(i))
                failed += 1
            elif stateReturn == Gst.StateChangeReturn.ASYNC or Gst.StateChangeReturn.SUCCESS:
                print("- Pipline {} succeeded".format(i))
                runningPipes.append(pipeline)


        print("- trial ended with " + str(failed) + " failed cams.")

        first_run = False

    return runningPipes

def pipesAreRunning(runningPipes):
    for pipeline in runningPipes:
        _, state, _ = pipeline.get_state(timeout=10*Gst.SECOND)
        if state != Gst.State.PLAYING:
            print("- Pipline stopped ")
            return False
    return True

def mainloop(pipelines):
    runningPips = startPipelines(pipelines)
    while True:
        sleep(3)
        if not pipesAreRunning(runningPips):
            runningPips = startPipelines(pipelines)


###################### create elemenst ##################
pipStr0 = 'v4l2src device="/dev/video0" !  video/x-raw,width=640,height=480 ! jpegenc ! rtpjpegpay !  udpsink host=192.168.2.1 port=5000'
pipStr1 = 'v4l2src device="/dev/video1" !  video/x-raw,width=640,height=480 ! jpegenc ! rtpjpegpay !  udpsink host=192.168.2.1 port=5100'
pipStr2 = 'v4l2src device="/dev/video2" !  video/x-raw,width=640,height=480 ! jpegenc ! rtpjpegpay !  udpsink host=192.168.2.1 port=5200'
pipStr3 = 'v4l2src device="/dev/video3" !  video/x-raw,width=640,height=480 ! jpegenc ! rtpjpegpay !  udpsink host=192.168.2.1 port=5300'
pipStr4 = 'v4l2src device="/dev/video4" !  video/x-raw,width=640,height=480 ! jpegenc ! rtpjpegpay !  udpsink host=192.168.2.1 port=5400'


pipelines = [
    Gst.parse_launch(pipStr0),
    Gst.parse_launch(pipStr1),
    Gst.parse_launch(pipStr2),
    Gst.parse_launch(pipStr3),
    Gst.parse_launch(pipStr4)
]

###################### Running piplines ##################
# runningPipes = startPipelines(pipelines)


###################### Main loop ##################
while True:
    try:
        mainloop(pipelines)
    except KeyboardInterrupt:
        break


print("\n- Terminating")
resetPipelins(pipelines)