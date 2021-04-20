import cv2
import numpy as np

cam0 = cv2.VideoCapture('udpsrc port=5000 ! application/x-rtp, encoding-name=JPEG,payload=26 ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink', cv2.CAP_GSTREAMER)
cam1 = cv2.VideoCapture('udpsrc port=5100 ! application/x-rtp, encoding-name=JPEG,payload=26 ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink', cv2.CAP_GSTREAMER)

while True:

    try:
        ret0, frame0 = cam0.read()
        ret1, frame1 = cam1.read()
    except Exception:
        break


    Hori = np.concatenate((frame0, frame1), axis=1)
    cv2.imshow("frame", Hori)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cam0.release()
cam1.release()
cv2.destroyAllWindows()
