#!/usr/bin/env python3

###################### inits ##################
import gi
import sys

gi.require_version("GLib", "2.0")
gi.require_version("GObject", "2.0")
gi.require_version("Gst", "1.0")

from gi.repository import Gst, GLib, GObject

Gst.init(sys.argv[1:])
###################### /inits ################## 

###################### create elemenst ##################
pipStr = 'v4l2src device="/dev/video0" !  video/x-raw,width=640,height=480 !  timeoverlay ! jpegenc ! rtpjpegpay !  udpsink host=127.0.0.1 port= 5000'

pipeline = Gst.parse_launch(pipStr)
if not pipeline:
    print("pipeline error")
    sys.exit(1)
###################### /create elemenst ##################

###################### Running pipline ##################
ret = pipeline.set_state(Gst.State.PLAYING)
if ret == Gst.StateChangeReturn.FAILURE:
    print("Unable to set the pipeline to the playing state.")
    sys.exit(1)

bus = pipeline.get_bus()
msg = bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.ERROR | Gst.MessageType.EOS)

# Parse message
if msg:
    if msg.type == Gst.MessageType.ERROR:
        err, debug_info = msg.parse_error()
        print(f"Error received from element {msg.src.get_name()}: {err.message}")
        print(f"Debugging information: {debug_info if debug_info else 'none'}")
    elif msg.type == Gst.MessageType.EOS:
        print("End-Of-Stream reached.")
    else:
        # This should not happen as we only asked for ERRORs and EOS
        print("Unexpected message received.")

pipeline.set_state(Gst.State.NULL)
###################### Running pipline ##################
