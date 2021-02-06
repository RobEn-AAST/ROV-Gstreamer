#!/usr/bin/env python3

# Sender : gst-launch-1.0 v4l2src !  video/x-raw,width=640,height=480 !  timeoverlay ! jpegenc ! rtpjpegpay !  udpsink host=192.168.2.1 port= 5000
# Reciever : gst-launch-1.0 udpsrc port=5000 !  application/x-rtp, encoding-name=JPEG,payload=26 !  rtpjpegdepay ! jpegdec ! autovideosink