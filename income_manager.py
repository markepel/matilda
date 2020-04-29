import io
import socket
import struct
import config
import logging
import queue
from collections import deque
import time


class IncomeManager():
    def __init__(self, preprocessor):
        logging.info('Income Manager initialization')
        self.image_deque = deque(maxlen=50)
        self.subscribers = set()
        self.preprocessor = preprocessor
    
    def start_receiving(self):
        logging.info('start_receiving')
        self.start_listening()
        self.wait_on_connection()
        time.sleep(2)
        self.handle_income()
        logging.info('start receiving(income manager thread) ends. bye bye')
        self.try_reconnect(count=300)
        logging.info('start_receiving (income manager thread) really ends. See ya')


    def try_reconnect(self, count=50):
        for i in range(count):
            try:
                logging.info("reconnecting. bye bye was a joke, man")
                time.sleep(5)
                self.start_listening()
                self.wait_on_connection()
                self.handle_income()
            except Exception as e:
                logging.error('try_reconnect start_listening Exception {}'.format(e), exc_info=True)
            


    def start_listening(self):
        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', config.tilda_port))
        self.server_socket.listen(0)
        logging.info('start listening on port {}'.format(tilda_port))

    def wait_on_connection(self):
        self.income_connection = self.server_socket.accept()[0].makefile('rb')
        logging.info('connection accepted')

    def handle_income(self):
        try:
            logging.info('handle_income starts')
            while True:
                image_len = struct.unpack('<L', self.income_connection.read(struct.calcsize('<L')))[0]
                if not image_len:
                    logging.info('IncomeManager handle_income no image')
                    break
                image_stream = io.BytesIO()
                image_stream.write(self.income_connection.read(image_len))
                image_stream.seek(0)
                self.handle_image(image_stream.read())
        except Exception as e:
            logging.error('handle_income Exception {}'.format(e), exc_info=True)
        finally:
            logging.info('handle_income finally')
            self.income_connection.close()
            self.server_socket.close()
    
    def handle_image(self, image_bytes):
        # logging.info('handling new image with image len {}'.format(len(image_bytes)))
        logging.info('Income manager handle_image of type {}'.format(type(image_bytes)))
        processed_image = self.preprocessor.process(image_bytes)
        logging.info('Income manager processed_image of type {}'.format(type(processed_image)))
        self.image_deque.append(processed_image)
        self.notify_subscribers()
    
    def notify_subscribers(self):
        for subscriber in self.subscribers:
            try:
                subscriber.notify()
            except:
                logging.info('Failed notify subscriber {}. removing from subscribers'.format(subscriber))
                self.subscribers.remove(subscriber)
    
    def get_last_image(self):
        return self.image_deque[-1]
    
    def subscribe_for_new_images(self, subscriber):
        self.subscribers.add(subscriber)

    def unsubscribe_from_new_images(self, subscriber):
        self.subscribers.remove(subscriber)
