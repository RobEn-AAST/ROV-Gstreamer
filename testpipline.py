#! /usr/bin/env python3
from threading import Thread

import gi
import sys
from time import sleep

gi.require_version("Gst", "1.0")

from gi.repository import Gst, GLib

def mainloop():
    while True:
        sleep(0.01)

Gst.init(sys.argv[1:])

main_loop = GLib.MainLoop()
thread = Thread(target=main_loop.run)
thread.start()

pip0 = Gst.parse_launch('v4l2src device="/dev/video0" !  video/x-raw,width=640,height=480 ! jpegenc ! rtpjpegpay !  udpsink host=192.168.2.255 port=5000')
pip1 = Gst.parse_launch('v4l2src device="/dev/video1" !  video/x-raw,width=640,height=480 ! jpegenc ! rtpjpegpay !  udpsink host=192.168.2.255 port=5100')


pip0.set_state(Gst.State.PLAYING)
pip1.set_state(Gst.State.PLAYING)

try:
    mainloop()
except KeyboardInterrupt:
    print("exiting")
    pass

pip0.set_state(Gst.State.NULL)
pip1.set_state(Gst.State.NULL)

main_loop.quit()