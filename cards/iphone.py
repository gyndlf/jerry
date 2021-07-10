# d7041

#

import cv2 as cv
import VideoStream
import time
import logging

font = cv.FONT_HERSHEY_SIMPLEX
freq = cv.getTickFrequency()
frame_rate = 0  # For initial frame

videostream = VideoStream.VideoStream().start()
logging.info("Initialising camera...")
time.sleep(1)  # Warm-up everything
quit = False

while quit == False:
    tic = cv.getTickCount()

    image = videostream.read()

    cv.putText(image, "FPS: " + str(int(frame_rate)), (10, 26), font, 0.7, (255, 0, 255), 2, cv.LINE_AA)
    cv.imshow("Card", image)

    # Find framerate
    toc = cv.getTickCount()
    frame_rate = freq/(toc-tic)

    # Exit the loop?
    key = cv.waitKey(1) & 0xFF
    if key == ord("q"):
        quit = True

cv.destroyAllWindows()
videostream.stop()