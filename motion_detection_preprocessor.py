import datetime
import numpy as np
import imutils
import cv2
import logging
from single_motion_detector import SingleMotionDetector

class MotionDetectionProcessor():
    def __init__(self, operational_image_width=400, background_model_frame_count=30):
        self.operational_image_width = operational_image_width
        self.background_model_frame_count = background_model_frame_count
        self.motion_detector = SingleMotionDetector(accumWeight=0.1)
        self.detection_count = 0
    
    def process(self, image):
        # total = 0
        # while True:
        nparr = np.fromstring(image, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        image = imutils.resize(image, width=400)
        logging.info('MotionDetectionProcessor image of type {}'.format(type(image)))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        logging.info('MotionDetectionProcessor gray of type {}'.format(type(gray)))
        timestamp = datetime.datetime.now()
        cv2.putText(image, timestamp.strftime("%A %d %B %Y %I:%M:%S%p"), (10, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        if self.detection_count <= self.background_model_frame_count:
            self.detection_count += 1
        else:
            motion = motion_detector.detect(gray)
            if motion is not None:
                (thresh, (minX, minY, maxX, maxY)) = motion
                cv2.rectangle(image, (minX, minY), (maxX, maxY),
                    (0, 0, 255), 2)
        motion_detector.update(gray)
        return image
