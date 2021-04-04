import cv2


cam = cv2.VideoCapture('udpsrc port=5000 !  application/x-rtp, encoding-name=JPEG,payload=26 !  rtpjpegdepay ! jpegdec ! autovideosink')

while True:
    _, frame = cam.read()

    cv2.imshow("Vidoe0", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cam.release()
cv2.destroyAllWindows()