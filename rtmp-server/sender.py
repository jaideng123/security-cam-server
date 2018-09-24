import cv2
import sys

camera = cv2.VideoCapture(0)

while True:
    # read current frame
    _, img = camera.read()
    # encode as a jpeg image and return it
    sys.stdout.write(img.tostring())
camera.release()
cv2.destroyAllWindows()
