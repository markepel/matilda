import io
import socket
import struct
from flask import Response
from flask import Flask
from flask import render_template
import time
import config
import logging
# logging.basicConfig(level=logging.INFO)
logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s', datefmt='%Y-%m-%d,%H:%M:%S')
logging initialized
import threading
from income_manager import IncomeManager
from image_generator import ImageGenerator



def set_logging():
    # logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s', datefmt='%Y-%m-%d,%H:%M:%S')
    logging.info('logging initialized')

def create_flask_app(income_manager=None):
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
    
    logging.info('flask starting')

    return app


def image_generator_to_http_adapter(image_generator):
    for image in image_generator:
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')



if __name__ == "__main__":
    set_logging()
    income_manager = IncomeManager()
    flask_app = create_flask_app(income_manager=income_manager)
    logging.info('flask started main')
    image_receiver_thread = threading.Thread(target=income_manager.start_receiving)
    image_receiver_thread.start()
    flask_app.run(host='0.0.0.0', port=5000, debug=True,threaded=True, use_reloader=False)
    
