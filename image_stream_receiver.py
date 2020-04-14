import io
import socket
import struct
from PIL import Image
from flask import Response
from flask import Flask
from flask import render_template
import tim
from config import tilda_ip, tilda_port
from image_generator import image_generator

try:
  server_socket = socket.socket()
  server_socket.bind(('0.0.0.0', tilda_port))
  server_socket.listen(0)
  connection = server_socket.accept()[0].makefile('rb')
  print('connection accepted')



  def image_generator():
    try:
        print('image_generator starts')
        while True:
            image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
            if not image_len:
                break
            image_stream = io.BytesIO()
            image_stream.write(connection.read(image_len))
            image_stream.seek(0)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + image_stream.read() + b'\r\n')
            # image = Image.open(image_stream)
            # print('Image is %dx%d' % image.size)
            # image.verify()
            # print('Image is verified')
    except Exception as e:
        print('image_generator Exception {}'.format(e))
    finally:
        print('image_generator finally')
        connection.close()
        server_socket.close()



  app = Flask(__name__)
  @app.route("/video_feed")
  def video_feed():
      try:
        print('Starting video feeding')
        return Response(image_generator(),
            mimetype = "multipart/x-mixed-replace; boundary=frame")
      except Exception as e:
        print('Excepion in video_feed {}'.format(e))

  @app.route("/videobytes_feed")
  def videobytes_feed():
      try:
        print('Starting videobytes_feed feeding')
        for image in image_generator():
          time.sleep(0.1)
      except Exception as e:
        print('Excepion in videobytes_feed {}'.format(e))

  app.run(host='0.0.0.0', port=5000, debug=True,
          threaded=True, use_reloader=False)

  print('Listening...')
except Exception as e:
  print('__main__ error {}'.format(e))