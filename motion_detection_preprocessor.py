import datetime
import numpy as np
import imutils
import cv2
import logging
from single_motion_detector import SingleMotionDetector
import requests
from privateconfig import TELEGRAM_BOT_API_KEY, TELEGRAM_BOT_NAME, MARK_CHAT_ID
import config
from multiprocessing.pool import ThreadPool
from concurrent.futures import ThreadPoolExecutor
import io

class MotionDetectionProcessor():
    def __init__(self, operational_image_width=400, background_model_frame_count=30):
        self.operational_image_width = operational_image_width
        self.background_model_frame_count = background_model_frame_count
        self.motion_detector = SingleMotionDetector(accumWeight=config.motion_detection_accum_weight, min_area=config.min_motion_area)
        self.detection_count = 0
        self.thread_executor = ThreadPoolExecutor(max_workers=2)
    
    def process(self, image):
        motion_detected = False
        nparr = np.fromstring(image, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # image = imutils.resize(image, width=400)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        timestamp = datetime.datetime.now()
        cv2.putText(image, timestamp.strftime("%A %d %B %Y %I:%M:%S%p"), (10, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (96, 255, 71), 1)
        if self.detection_count <= self.background_model_frame_count:
            self.detection_count += 1
        else:
            motion = self.motion_detector.detect(gray)
            if motion is not None:
                motion_detected = True
                (thresh, (minX, minY, maxX, maxY)) = motion
                cv2.rectangle(image, (minX, minY), (maxX, maxY),(96, 255, 71), 2)
        (flag, encodedImage) = cv2.imencode(".jpg", image)
        self.motion_detector.update(gray)
        output_image = bytearray(encodedImage)
        if motion_detected:
            logging.info('motion detected')
            self.thread_executor.submit(send_image, output_image)
        return bytearray(encodedImage)

def send_image(image_bytes):
    try:
        f_image = io.BytesIO(image_bytes)
        f_image.name = 'img.jpg'
        files = {'photo': f_image.read()}
        data = {'chat_id' : '{}'.format(MARK_CHAT_ID), 'caption': 'Motion detected'}
        response = requests.post('https://api.telegram.org/bot{}/sendPhoto'.format(TELEGRAM_BOT_API_KEY), files=files, data=data)
        logging.info(response.json())
    except:
        logging.info('exception on requests send_image')
        pass








