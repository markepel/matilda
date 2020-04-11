import io
import socket
import struct
from PIL import Image
from flask import Response
from flask import Flask
from flask import render_template

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8008))
server_socket.listen(0)
connection = server_socket.accept()[0].makefile('rb')
print('connection accepted')



def image_generator():
  try:
      while True:
          image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
          if not image_len:
              break
          image_stream = io.BytesIO()
          image_stream.write(connection.read(image_len))
          image_stream.seek(0)
          yield (b'--frame\r\n'
                 b'Content-Type: image/jpeg\r\n\r\n' + image_stream.read() + b'\r\n')
          print('after yield image')
          # image = Image.open(image_stream)
          # print('Image is %dx%d' % image.size)
          # image.verify()
          # print('Image is verified')
  except Exception as e:
      print('Exception {}'.format(e))
  finally:
      print('finally')
      connection.close()
      server_socket.close()



app = Flask(__name__)
@app.route("/video_feed")
def video_feed():
    # return 'Hello, World!'
    print('Starting video feeding')
    return Response(image_generator(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")


app.run(host='0.0.0.0', port=5000, debug=True,
        threaded=True, use_reloader=False)

print('Listening...')



