import cv2
import sys

camera = cv2.VideoCapture(0)
try:
    camera.set(cv2.cv.CV_CAP_PROP_FPS, 10)
except:
    camera.set(cv2.CAP_PROP_FPS, 10)

while True:
    # read current frame
    _, img = camera.read()
    # encode as a jpeg image and return it
    # sys.stdout.write(cv2.imencode('.jpg', img)[1].tobytes())
    sys.stdout.write(img)
camera.release()
cv2.destroyAllWindows()
