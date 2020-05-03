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
        self.motion_detector = SingleMotionDetector(accumWeight=config.motion_detection_accum_weight)
        self.detection_count = 0
        self.thread_executor = ThreadPoolExecutor(max_workers=2)
    
    def process(self, image):
        # total = 0
        # while True:
        motion_detected = False
        nparr = np.fromstring(image, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        image = imutils.resize(image, width=400)
        # logging.info('MotionDetectionProcessor image of type {}'.format(type(image)))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        # logging.info('MotionDetectionProcessor gray of type {}'.format(type(gray)))
        timestamp = datetime.datetime.now()
        cv2.putText(image, timestamp.strftime("%A %d %B %Y %I:%M:%S%p"), (10, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        if self.detection_count <= self.background_model_frame_count:
            self.detection_count += 1
        else:
            motion = self.motion_detector.detect(gray)
            if motion is not None:
                motion_detected = True
                (thresh, (minX, minY, maxX, maxY)) = motion
                cv2.rectangle(image, (minX, minY), (maxX, maxY),(0, 0, 255), 2)
        (flag, encodedImage) = cv2.imencode(".jpg", image)
        self.motion_detector.update(gray)
        if motion_detected:
            logging.info('motion detected')
            try:
                f_image = io.BytesIO(bytearray(encodedImage))
            except:
                logging.info('exception in mtion')
                raise
            self.thread_executor.submit(send_image, f_image)
        return bytearray(encodedImage)

def send_image(image):
    # files = {'image': ('IMAGENAME.jpg',image,'multipart/form-data')}
    # files2 = {'media': image}
    image.name = 'img.jpg'
    files = {'photo': image}
    data = {'chat_id' : '{}'.format(MARK_CHAT_ID)}

    # files = {
    #     'chat_id': '{}'.format(MARK_CHAT_ID),
    #     'caption': 'test requests',
    #     'photo': ('f.jpg', f_image.read()),
    # }
    try:
        response = requests.post('https://api.telegram.org/bot{}/sendPhoto'.format(TELEGRAM_BOT_API_KEY), files=files, data=data)
        logging.info(response.json())
    except:
        logging.info('exception on requests phto')
        pass
    # try:
    #     res1 = requests.post("https://api.telegram.org/bot{}/sendPhoto?photo={}&chat_id={}&caption={}".format(image, TELEGRAM_BOT_API_KEY, MARK_CHAT_ID, 'photo motion detection'), data=files)
    #     logging.info(res1.json())
    # except:
    #     pass
    # try:
    #     res2 = requests.post("https://api.telegram.org/bot{}/sendPhoto?photo={}&chat_id={}&caption={}".format(image, TELEGRAM_BOT_API_KEY, MARK_CHAT_ID, 'photo motion detection'), files=files)
    #     logging.info(res2.json())
    # except:
    #     pass
    # try:








