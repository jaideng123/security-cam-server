import cv2
import time
import threading
try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident


class StreamSynchronizer(object):
    """An Event-like class that signals all active clients when a new frame is
    available.
    """

    def __init__(self):
        self.events = {}

    def wait(self):
        """Invoked from each client's thread to wait for the next frame."""
        ident = get_ident()
        if ident not in self.events:
            # this is a new client
            # add an entry for it in the self.events dict
            # each entry has two elements, a threading.Event() and a timestamp
            self.events[ident] = {
                'event': threading.Event(), 'timestamp': time.time()}
        return self.events[ident]['event'].wait()

    def set(self):
        """Invoked by the camera thread when a new frame is available."""
        now = time.time()
        remove = None
        for ident, event in self.events.items():
            if not event['event'].isSet():
                # if this client's event is not set, then set it
                # also update the last set timestamp to now
                event['event'].set()
                event['timestamp'] = now
            else:
                # if the client's event is already set, it means the client
                # did not process a previous frame
                # if the event stays set for more than 5 seconds, then assume
                # the client is gone and remove it
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        """Invoked from each client's thread after a frame was processed."""
        self.events[get_ident()]['event'].clear()


class Stream():
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera
    event = StreamSynchronizer()
    video_source = 0

    def __init__(self):
        """Start the background camera thread if it isn't running yet."""
        if Stream.thread is None:
            Stream.last_access = time.time()

            # start background frame thread
            Stream.thread = threading.Thread(target=self._thread)
            Stream.thread.start()

            # wait until frames are available
            while self.get_frame() is None:
                time.sleep(0)

    def get_frame(self):
        """Return the current camera frame."""
        Stream.last_access = time.time()

        # wait for a signal from the camera thread
        Stream.event.wait()
        Stream.event.clear()

        return Stream.frame

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Stream.video_source)
        print(camera.get(cv2.CAP_PROP_FPS))
        print(str(camera.get(cv2.CAP_PROP_FRAME_WIDTH))+'x' +
              str(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')
        while True:
            # read current frame
            _, img = camera.read()
            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()

    def _thread(self):
        """Camera background thread."""
        print('Starting camera thread.')
        frames_iterator = self.frames()
        for frame in frames_iterator:
            Stream.frame = frame
            Stream.event.set()  # send signal to clients
            time.sleep(0)
        Stream.thread = None
