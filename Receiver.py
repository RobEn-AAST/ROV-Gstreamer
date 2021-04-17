import cv2

numberOfCams = 2

cams = [ cv2.VideoCapture('udpsrc port=5{}00 ! application/x-rtp, encoding-name=JPEG,payload=26 ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink'.format(i), cv2.CAP_GSTREAMER) for i in range(numberOfCams)]

print("We got past here")

frames = []

while True:

    for cam in cams:
        if not cam == None:
            _, frame = cam.read()
            frames.append(frame)

    for i, frame in enumerate(frames):
        if not frame == None:
            cv2.imshow("Frame {}".format(i+3), frame)

    cv2.imshow("Vidoe0", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


for cam in cams:
    if not cam == None:
        cam.release()

cv2.destroyAllWindows()