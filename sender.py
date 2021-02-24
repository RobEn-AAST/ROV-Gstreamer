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

devices = {
    'cam0' : {'dev':'video0', 'port':'5000'},
    'cam1' : {'dev':'video1', 'port':'5100'},
    'cam2' : {'dev':'video2', 'port':'5200'},
    'cam3' : {'dev':'video2', 'port':'5300'}
}



###################### create elemenst ##################
pipStr0 = f'v4l2src device="/dev/{devices["cam0"]["dev"]}" !  video/x-raw,width=640,height=480 !  timeoverlay ! jpegenc ! rtpjpegpay !  udpsink host=127.0.0.1 port={devices["cam0"]["port"]}'
pipStr1 = f'v4l2src device="/dev/{devices["cam1"]["dev"]}" !  video/x-raw,width=640,height=480 !  timeoverlay ! jpegenc ! rtpjpegpay !  udpsink host=127.0.0.1 port={devices["cam1"]["port"]}'
pipStr2 = f'v4l2src device="/dev/{devices["cam2"]["dev"]}" !  video/x-raw,width=640,height=480 !  timeoverlay ! jpegenc ! rtpjpegpay !  udpsink host=127.0.0.1 port={devices["cam2"]["port"]}'
pipStr2 = f'v4l2src device="/dev/{devices["cam3"]["dev"]}" !  video/x-raw,width=640,height=480 !  timeoverlay ! jpegenc ! rtpjpegpay !  udpsink host=127.0.0.1 port={devices["cam3"]["port"]}'
print(pipStr0)
pipeline0 = Gst.parse_launch(pipStr0)
pipeline1 = Gst.parse_launch(pipStr1)
pipeline2 = Gst.parse_launch(pipStr2)

if not pipeline0 or not pipeline1 or not pipeline2:
    print("pipeline error")
    sys.exit(1)


###################### Running piplines ##################
while True:
    ret0 = pipeline0.set_state(Gst.State.PLAYING)
    # ret1 = pipeline1.set_state(Gst.State.PLAYING)
    # ret2 = pipeline2.set_state(Gst.State.PLAYING)
    if ret0 == Gst.StateChangeReturn.FAILURE:
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
