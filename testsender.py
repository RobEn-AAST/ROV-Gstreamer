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

def resetPipelins(pip0, pip1, pip2, pip3):
    pip0.set_state(Gst.State.NULL)
    pip1.set_state(Gst.State.NULL)
    pip2.set_state(Gst.State.NULL)
    pip3.set_state(Gst.State.NULL)

def mainloop():
    print("\n- entered main loop...")
    while True:
        sleep(0.01)

def checkStates():
    pass

def startPipelines(pip0, pip1, pip2, pip3):
    failed = 0
    first_run = True
    print("- starting pipes...")

    while failed > 3 or first_run:

        if not first_run:
            sleep(1)

        first_run = False
        failed = 0

        resetPipelins(pip0, pip1, pip2, pip3)

        _, pip0State, _ = pip1.get_state(timeout=10*Gst.SECOND)

        ret0 = pip0.set_state(Gst.State.PLAYING)
        if ret0 == Gst.StateChangeReturn.FAILURE:
            print("- Pipline 0 failed")
            failed += 1

        ret1 = pip1.set_state(Gst.State.PLAYING)
        if ret1 == Gst.StateChangeReturn.FAILURE:
            print("- Pipline 1 failed")
            failed += 1

        ret2 = pip2.set_state(Gst.State.PLAYING)
        if ret2 == Gst.StateChangeReturn.FAILURE:
            print("- Pipline 2 failed")
            failed += 1

        ret3 = pip3.set_state(Gst.State.PLAYING)
        if ret3 == Gst.StateChangeReturn.FAILURE:
            print("- Pipline 3 failed")
            failed += 1

        print("- trial ended with ", failed, " failed cams.")


###################### create elemenst ##################
pipStr0 = 'v4l2src device="/dev/video0" !  video/x-raw,width=640,height=480 !  timeoverlay ! jpegenc ! rtpjpegpay !  udpsink host=192.168.2.1 port=5000'
pipStr1 = 'v4l2src device="/dev/video1" !  video/x-raw,width=640,height=480 !  timeoverlay ! jpegenc ! rtpjpegpay !  udpsink host=192.168.2.1 port=5100'
pipStr2 = 'v4l2src device="/dev/video2" !  video/x-raw,width=640,height=480 !  timeoverlay ! jpegenc ! rtpjpegpay !  udpsink host=192.168.2.1 port=5200'
pipStr3 = 'v4l2src device="/dev/video3" !  video/x-raw,width=640,height=480 !  timeoverlay ! jpegenc ! rtpjpegpay !  udpsink host=192.168.2.1 port=5300'


pipeline0 = Gst.parse_launch(pipStr0)
pipeline1 = Gst.parse_launch(pipStr1)
pipeline2 = Gst.parse_launch(pipStr2)
pipeline3 = Gst.parse_launch(pipStr3)


###################### Running piplines ##################
startPipelines(pipeline0, pipeline1, pipeline2, pipeline3)


###################### Main loop ##################
while True:
    try:
        mainloop()
    except KeyboardInterrupt:
        break
    except Exception:
        startPipelines(pipeline0, pipeline1, pipeline2, pipeline3)
        continue;

print("\nterminating")
resetPipelins(pipeline0, pipeline1, pipeline2, pipeline3)