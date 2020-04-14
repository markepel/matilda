import time
import config
import logging
logger = logging.getLogger(__name__) 
import threading


class ImageGenerator():
    def __init__(self, income_manager):
        self.income_manager = income_manager
        self.fresh_image_event = threading.Event()
        income_manager.subscribe_for_new_images(self)

    
    def start():
        logger.info('ImageGenerator starts')
        start = time.time()
        finish = time.time()
        count = 0
        while finish - start < config.generation_period:
            self.fresh_image_event.wait()
            yield income_manager.get_last_image()
            logger.info('ImageGenerator yielded new image')
            self.fresh_image_event.clear()
            count += 1
            finish = time.time()
        logger.info('ImageGenerator generated {} images in {} with {} fps'.format(count,start-finish,count/(start-finish)))
        self.income_manager.unsubscribe_from_new_images(self)
    

    def notify():
        self.fresh_image_event.set()