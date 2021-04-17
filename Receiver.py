import cv2

cam0 = cv2.VideoCapture('udpsrc port=5000 ! application/x-rtp, encoding-name=JPEG,payload=26 ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink', cv2.CAP_GSTREAMER)
cam1 = cv2.VideoCapture('udpsrc port=5100 ! application/x-rtp, encoding-name=JPEG,payload=26 ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink', cv2.CAP_GSTREAMER)

while True:

    try:
        ret0, frame0 = cam0.read()
        ret1, frame1 = cam1.read()
    except Exception:
        break
    if ret0:
        cv2.imshow("Frame0", frame0)
    if ret1:
        cv2.imshow("Frame1", frame1)

    cv2.resizeWindow('Frame0', 640,600)
    cv2.resizeWindow('Frame1', 640,600)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cam0.release()
cam1.release()
cv2.destroyAllWindows()
