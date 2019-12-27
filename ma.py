import picamera
import socket
from matilda.config import tilda_ip
import time
import cv2
#import imutils

client_socket = socket.socket()
print('connecting...')
client_socket.connect((tilda_ip, 8000))

print('connected')

connection = client_socket.makefile('wb')

try:
    #vs = imutils.VideoStream(src=0, usePicamera=True, resolution=(720, 576)).start()

    #for i in range(1,6):
     #  print(f'{i}...')
      #  time.sleep(i)
    #print('Ignition')
    #while True:
     #   frame = vs.read()
        #client_socket.sendall(frame)
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 24
        rawCapture = picamera.PiRGBArray(camera, size=(640, 480))

        # camera.start_preview()
        for i in range(1,6):
            print(f'{i}...')
            time.sleep(i)
        print('Ignition')
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            encoded, buffer = cv2.imencode('.jpg', frame)
            print('encofed = {}, buffer = {}'.format(encoded, buffer))
            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)
finally:
    connection.close()
    client_socket.close()
