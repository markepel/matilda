import time
import config
import logging
# logging.basicConfig(level=logging.INFO)
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
        # while finish - start < config.generation_period:
        while True:
            logging.info('ImageGenerator before wait')
            # if count % 10 == 0: logging.info('ImageGenerator before wait')
            self.fresh_image_event.wait(20)
            # if count % 10 == 0: logging.info('ImageGenerator after wait')
            logging.info('ImageGenerator after wait')
            if self.fresh_image_event.is_set():
                yield self.income_manager.get_last_image()
                # if count % 10 == 0: logging.info('ImageGenerator yielded 10 new images')
                logging.info('ImageGenerator yielded 10 new images')
                self.fresh_image_event.clear()
                count += 1
                finish = time.time()
            else:
                logging.info('ImageGenerator wasnt set in 20 seconds. unsubscribing')
                self.income_manager.unsubscribe_from_new_images(self)
                return
        logging.info('ImageGenerator generated {} images in {} with {} fps'.format(count,start-finish,count/(start-finish)))
        self.income_manager.unsubscribe_from_new_images(self)
    

    def notify(self):
        self.fresh_image_event.set()