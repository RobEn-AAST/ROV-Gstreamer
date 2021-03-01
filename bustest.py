#!/usr/bin/env python3

###################### inits ##################
import gi
import sys
import os

gi.require_version("GLib", "2.0")
gi.require_version("GObject", "2.0")
gi.require_version("Gst", "1.0")

from gi.repository import Gst, GLib, GObject

Gst.init(sys.argv[1:])
###################### /inits ################## 

###################### create elemenst ##################
def isVideo(element):
    return True if element.startswith("video") else False 

cams = filter(isVideo, os.listdir("/dev/"))
pipelines = []

for i, cam in enumerate(cams):
    pipStr = 'v4l2src device="/dev/{}" !  video/x-raw,width=640,height=480 ! jpegenc ! rtpjpegpay !  udpsink buffer-size=50000000 host=192.168.2.255 port=5{}00'.format(cam, i)
    pipeline = Gst.parse_launch(pipStr)
    pipelines.append(pipeline)

for pipeline in pipelines:
    if not pipeline:
        print("pipeline error")
        sys.exit(1)
###################### /create elemenst ##################

###################### Running pipline ##################
for pipeline in pipelines:
    ret = pipeline.set_state(Gst.State.PLAYING)
    if ret == Gst.StateChangeReturn.FAILURE:
        print("Unable to set the pipeline to the playing state.")
    else:
        print("pipeline started.")

bus = pipelines[0].get_bus()
print("bus running")
msg = bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.ERROR | Gst.MessageType.EOS)

# Parse message
if msg:
    if msg.type == Gst.MessageType.ERROR:
        err, debug_info = msg.parse_error()
        print("Error received from element" +  str(msg.src.get_name()) + " : " +  str(err.message))
        print("Debugging information: " + str(debug_info if debug_info else 'none'))
    elif msg.type == Gst.MessageType.EOS:
        print("End-Of-Stream reached.")
    else:
        # This should not happen as we only asked for ERRORs and EOS
        print("Unexpected message received.")

pipeline.set_state(Gst.State.NULL)
###################### Running pipline ##################
