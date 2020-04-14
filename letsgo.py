import io
import socket
import struct
from flask import Response
from flask import Flask
from flask import render_template
import time
import config
import logging
logging.basicConfig(level=logging.DEBUG)
import threading
from income_manager import IncomeManager
from image_generator import ImageGenerator



def set_logging():
    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(format=FORMAT)
    print('logging initialized')

def start_flask(income_manager=None):
    app = Flask(__name__)

    @app.route("/video_feed")
    def video_feed():
        try:
            logging.info('Starting video feeding')
            return Response(image_generator_to_http_adapter(ImageGenerator(income_manager).start()),mimetype = "multipart/x-mixed-replace; boundary=frame")
        except Exception as e:
            logging.info('Excepion in video_feed {}'.format(e))

    @app.route("/videobytes_feed")
    def videobytes_feed():
        try:
            logging.info('Starting videobytes_feed feeding')
            for image in ImageGenerator(income_manager).start():
                time.sleep(0.1)
        except Exception as e:
            logging.info('Excepion in videobytes_feed {}'.format(e))

    app.run(host='0.0.0.0', port=5000, debug=True,
            threaded=True, use_reloader=False)
    logging.info('flask started')


def image_generator_to_http_adapter(image_generator):
    for image in image_generator:
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')



if __name__ == "__main__":
    set_logging()
    income_manager = IncomeManager()
    start_flask(income_manager=income_manager)
    image_receiver_thread = threading.Thread(target=income_manager.start_receiving)
    image_receiver_thread.start()
