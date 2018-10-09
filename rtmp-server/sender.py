import cv2
import sys
import subprocess
import os
import thread

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
    '-c:v', 'h264_omx',
    '-b:v', '500k',
    'rtmp://a.rtmp.youtube.com/live2/'+os.environ['YOUTUBEKEY']
]

from flask import Flask, render_template, Response


app = Flask(__name__)

running = False


@app.route('/off')
def off():
    stopStream()
    return 'OFF'


@app.route('/on')
def on():
    startStream()
    return 'ON'


@app.route('/status')
def status():
    global running
    if(running):
        return 'ON'
    else:
        return 'OFF'


def stopStream():
    global running
    if(not running):
        return False
    running = False
    return True


def streamVideo():
    camera = cv2.VideoCapture(0)
    try:
        camera.set(cv2.cv.CV_CAP_PROP_FPS, 10)
    except:
        camera.set(cv2.CAP_PROP_FPS, 10)
    # Set Resolution
    camera.set(3, 1280)
    camera.set(4, 720)
    ffmpeg = subprocess.Popen(args=ffargs, stdin=subprocess.PIPE)
    while running:
        # read current frame
        _, img = camera.read()
        # encode as a jpeg image and return it
        # sys.stdout.write(cv2.imencode('.jpg', img)[1].tobytes())
        ffmpeg.stdin.write(img)
    ffmpeg.kill()
    camera.release()
    cv2.destroyAllWindows()


def startStream():
    global running
    if(running):
        return False
    running = True
    thread.start_new_thread(streamVideo, ())
    return True


app.run(host='localhost', threaded=True)
