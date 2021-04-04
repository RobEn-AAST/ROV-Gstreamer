import cv2


cam = cv2.VideoCapture('udpsrc port=5000 ! application/x-rtp, encoding-name=JPEG,payload=26 ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink')

while True:
    videoComing, frame = cam.read()
    while not videoComing:
        print("NO FEED COMING IN")
        videoComing, frame = cam.read()

    cv2.imshow("Vidoe0", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cam.release()
cv2.destroyAllWindows()