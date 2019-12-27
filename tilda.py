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
    # Accept a single connection and make a file-like object out of it
    #connection = server_socket.accept()[0].makefile('rb')

    connection = server_socket.accept()[0].makefile('rb')
    bytes = b''
    print('connection accepted')
    try:
        while True:
            # Run a viewer with an appropriate command line. Uncomment the mplayer
                # version if you would prefer to use mplayer instead of VLC
                    #cmdline = ['vlc', '--demux', 'h264', '-']
                        #cmdline = ['mplayer', '-fps', '25', '-cache', '1024', '-']
                    
                    #player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
                                            # Repeatedly read 1k of data from the connection and write it to
                                                    # the media player's stdin
            bytes += connection.read(1024)
            a = bytes.find(b'\xff\xd8')
            b = bytes.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = bytes[a:b+2]
                bytes = bytes[b+2:]
                i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
                cv2.imshow('i', i)
                if cv2.waitKey(1) == 27:
                    exit(0) 
            if not bytes:
                raise Exception('No bytes')
            print('Data recieved, data_format=={}, data=={}'.format(type(bytes), bytes))
                        #player.stdin.write(data)
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
