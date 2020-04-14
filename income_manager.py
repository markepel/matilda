import io
import socket
import struct
from config import tilda_port
import logging
logger = logging.getLogger(__name__) 
import queue
from collections import deque
import time


class IncomeManager():
    def __init__(self):
        self.image_deque =  deque(maxlen=50)
        self.subscribers = set()
    
    def start_receiving(self):
        logger.info('start_receiving')
        self.start_listening()
        time.sleep(2)
        handle_income()

    def start_listening(self):
        server_socket = socket.socket()
        server_socket.bind(('0.0.0.0', tilda_port))
        server_socket.listen(0)
        logger.info('start listening on port {}'.format(tilda_port))
        connection = server_socket.accept()[0].makefile('rb')
        logger.info('connection accepted')

    def handle_income(self):
        try:
            logger.info('handle_income starts')
            while True:
                image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
                if not image_len:
                    break
                image_stream = io.BytesIO()
                image_stream.write(connection.read(image_len))
                image_stream.seek(0)
                self.handle_image(image_stream.read())
        except Exception as e:
            logger.info('handle_income Exception {}'.format(e))
        finally:
            logger.info('handle_income finally')
            connection.close()
            server_socket.close()
    
    def handle_image(image_bytes):
        self.image_deque.append(image_bytes)
        self.notify_subscribers()
    
    def notify_subscribers(self):
        for subscriber in self.subscribers:
            try:
                subscriber.notify()
            except:
                logger.info('Failed notify subscriber {}. removing from subscribers'.format(subscriber))
                self.subscribers.remove(subscriber)
    
    def get_last_image(self):
        return self.image_deque[-1]
    
    def subscribe_for_new_images(self, subscriber):
        self.subscribers.add(subscriber)

    def unsubscribe_from_new_images(self, subscriber):
        self.subscribers.remove(subscriber)
