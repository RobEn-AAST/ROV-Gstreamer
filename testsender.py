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

###################### FX ##################
def resetPipelins(pipelines):
    pipelines[0].set_state(Gst.State.NULL)
    pipelines[1].set_state(Gst.State.NULL)
    pipelines[2].set_state(Gst.State.NULL)
    pipelines[3].set_state(Gst.State.NULL)


def checkStates(pipelines):
    _, pip0State, _ = pipelines[0].get_state(timeout=10*Gst.SECOND)

def mainloop(pipelines):
    while True:
        sleep(0.01)
        checkStates(pipelines)

def startPipelines(pipelines):
    failed = 0
    first_run = True

    while failed > 1 or first_run:

        if not first_run:
            sleep(1)


        resetPipelins(pipelines)


        ret0 = pipelines[0].set_state(Gst.State.PLAYING)
        if ret0 == Gst.StateChangeReturn.FAILURE:
            print("- Pipline 0 failed")
            failed += 1

        ret1 = pipelines[1].set_state(Gst.State.PLAYING)
        if ret1 == Gst.StateChangeReturn.FAILURE:
            print("- Pipline 1 failed")
            failed += 1

        ret2 = pipelines[2].set_state(Gst.State.PLAYING)
        if ret2 == Gst.StateChangeReturn.FAILURE:
            print("- Pipline 2 failed")
            failed += 1

        ret3 = pipelines[3].set_state(Gst.State.PLAYING)
        if ret3 == Gst.StateChangeReturn.FAILURE:
            print("- Pipline 3 failed")
            failed += 1

        print("- trial ended with ", failed, " failed cams.")

        failed = 0
        first_run = False

###################### create elemenst ##################
pipStr0 = 'v4l2src device="/dev/video0" !  video/x-raw,width=640,height=480 !  timeoverlay ! jpegenc ! rtpjpegpay !  udpsink host=192.168.2.1 port=5000'
pipStr1 = 'v4l2src device="/dev/video1" !  video/x-raw,width=640,height=480 !  timeoverlay ! jpegenc ! rtpjpegpay !  udpsink host=192.168.2.1 port=5100'
pipStr2 = 'v4l2src device="/dev/video2" !  video/x-raw,width=640,height=480 !  timeoverlay ! jpegenc ! rtpjpegpay !  udpsink host=192.168.2.1 port=5200'
pipStr3 = 'v4l2src device="/dev/video3" !  video/x-raw,width=640,height=480 !  timeoverlay ! jpegenc ! rtpjpegpay !  udpsink host=192.168.2.1 port=5300'

pipelines = [Gst.parse_launch(pipStr0), Gst.parse_launch(pipStr1), Gst.parse_launch(pipStr2), Gst.parse_launch(pipStr3)]

###################### Running piplines ##################
startPipelines(pipelines)


###################### Main loop ##################
while True:
    try:
        mainloop(pipelines)
    except KeyboardInterrupt:
        break
    except Exception:
        startPipelines(pipelines)
        continue;


print("\n- Terminating")
resetPipelins(pipelines)