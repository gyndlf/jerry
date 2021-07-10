# d7041

# The video streaming object. Redirects from OBS straight to opencv

import cv2 as cv
from threading import Thread


class VideoStream:
    """Streaming object"""
    def __init__(self, src=0):
        self.stream = cv.VideoCapture(src)  # src is the video target
        self.stopped = False
        (self.grabbed, self.frame) = self.stream.read()  # get the first frame

    def start(self):
        # Start the multi-thread
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:  # Keep looping
            if self.stopped:
                self.stream.release()
                return

            # Get next frame
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True