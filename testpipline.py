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

# main_loop = GLib.MainLoop()
# thread = Thread(target=main_loop.run)
# thread.start()

pipeline = Gst.parse_launch('v4l2src device="/dev/video0" ! decodebin ! videoconvert ! autovideosink')


pipeline.set_state(Gst.State.PLAYING)

try:
    mainloop()
except KeyboardInterrupt:
    print("exiting")
    pass

pipeline.set_state(Gst.State.NULL)
# main_loop.quit()