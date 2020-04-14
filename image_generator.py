import time
import config
import logging
logging.basicConfig(level=logging.INFO)
import threading


class ImageGenerator():
    def __init__(self, income_manager):
        self.income_manager = income_manager
        self.fresh_image_event = threading.Event()
        income_manager.subscribe_for_new_images(self)

    
    def start(self):
        logging.info('ImageGenerator starts')
        start = time.time()
        finish = time.time()
        count = 0
        while finish - start < config.generation_period:
            self.fresh_image_event.wait()
            yield self.income_manager.get_last_image()
            logging.info('ImageGenerator yielded new image')
            self.fresh_image_event.clear()
            count += 1
            finish = time.time()
        logging.info('ImageGenerator generated {} images in {} with {} fps'.format(count,start-finish,count/(start-finish)))
        self.income_manager.unsubscribe_from_new_images(self)
    

    def notify(self):
        self.fresh_image_event.set()