import cv2
import sys
import subprocess
import os
import thread
import time

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

from flask import Flask, render_template, send_from_directory, Response
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

running = False


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/off')
@cross_origin()
def off():
    stopStream()
    return 'OFF'


@app.route('/on')
@cross_origin()
def on():
    startStream()
    return 'ON'


@app.route('/status')
@cross_origin()
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


def current_milli_time(): return int(round(time.time() * 1000))


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
    start = current_milli_time()
    while running:
        # See if this fixed timing issues
        # if(current_milli_time() - start < 167):
        #     continue

        # read current frame
        _, img = camera.read()
        # encode as a jpeg image and return it
        # sys.stdout.write(cv2.imencode('.jpg', img)[1].tobytes())
        ffmpeg.stdin.write(img)
        start = current_milli_time()
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
