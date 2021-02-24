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

devices = ["video0", "video1", "video2", "video3"]



###################### create elemenst ##################
pipStr = f'v4l2src device="/dev/{devices[0]}" !  video/x-raw,width=640,height=480 !  timeoverlay ! jpegenc ! rtpjpegpay !  udpsink host=127.0.0.1 port= 5000'

pipeline = Gst.parse_launch(pipStr)
if not pipeline:
    print("pipeline error")
    sys.exit(1)



###################### Running piplines ##################
ret = pipeline.set_state(Gst.State.PLAYING)
if ret == Gst.StateChangeReturn.FAILURE:
    print("Unable to set the pipeline to the playing state.")
    sys.exit(1)



###################### Main loop ##################
try:
    while True:
        sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    pipeline.set_state(Gst.State.NULL)
