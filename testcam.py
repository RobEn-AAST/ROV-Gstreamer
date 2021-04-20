import cv2

cam0 = cv2.VideoCapture(2)

while True:

    try:
        ret0, frame0 = cam0.read()
    except Exception:
        break
    # if ret0:
    #     cv2.imshow("Frame0", frame0)
    # if ret1:
    #     cv2.imshow("Frame1", frame1)
    if not ret0:
        print("errors")

    cv2.imshow("frame", frame0)
    print(frame0.shape)
    # cv2.resizeWindow('Frame0', 640,600)
    # cv2.resizeWindow('Frame1', 640,600)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cam0.release()
cv2.destroyAllWindows()