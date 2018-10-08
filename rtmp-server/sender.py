import cv2
import sys
import subprocess
import os

camera = cv2.VideoCapture(0)

try:
    camera.set(cv2.cv.CV_CAP_PROP_FPS, 10)
except:
    camera.set(cv2.CAP_PROP_FPS, 10)

# Set Resolution
camera.set(3, 1280)
camera.set(4, 720)

ffargs = [
    'ffmpeg',
    '-f', 'rawvideo',
    '-pixel_format', 'bgr24',
    '-video_size', '1280x720',
    '-framerate', '10',
    '-i', '-',
    '-f', 'lavfi',
    '-i', 'anullsrc',
    '-acodec', 'aac',
    '-f', 'flv',
    '-c:v', 'libx264',
    '-b:v', '500k',
    'rtmp://a.rtmp.youtube.com/live2/'+os.environ['YOUTUBEKEY']
]

ffmpeg = subprocess.Popen(args=ffargs, stdin=subprocess.PIPE)

while True:
    # read current frame
    _, img = camera.read()
    # encode as a jpeg image and return it
    # sys.stdout.write(cv2.imencode('.jpg', img)[1].tobytes())
    ffmpeg.stdin.write(img)
camera.release()
cv2.destroyAllWindows()
