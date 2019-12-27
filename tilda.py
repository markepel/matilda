import socket
import subprocess
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import sys, traceback
import cv2
import numpy as np
# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
app = Flask(__name__)

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

while True:
    print('Listening...')
    connection = server_socket.accept()[0].makefile('rb')
    bytes = b''
    print('connection accepted')
    try:
        #counter = 0
        while True:
            bytes += connection.read(1024)
            a = bytes.find(b'\xff\xd8')
            b = bytes.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = bytes[a:b+2]
                bytes = bytes[b+2:]
                i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                #cv2.imwrite('image{}.jpg'.format(counter), i)
                #counter += 1
                (flag, encodedImage) = cv2.imencode(".jpg", i)
                # print('flag {}'.format(flag))
                # print('encodedImage {}'.format(encodedImage))
                # print(type(i))
                # print('i {}, type {}'.format(i, type(i)))
                # cv2.imshow('i', i)
            if not bytes:
                raise Exception('No bytes')
    except Exception as e:
        print('Exception')
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        traceback.print_exc(limit=2, file=sys.stdout)

        connection.close()
        try:
            pass
            #server_socket.close()
        except:
            print('Error in except server socket.close')
        print('connection closed, listening')
        #server_socket.listen(0)
        print('after listen')
        #connection = server_socket.accept()[0].makefile('rb')
        print('new connection')
        
    # finally:
    #     connection.close()
    #     server_socket.close()

        #player.terminate()

#def gen(camera):
 #       frame = camera.read()
  #      yield (b'--frame\r\n
   #     'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

#@app.route('/video_feed')
#def video_feed():
 #   return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')
