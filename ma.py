import picamera
import socket
from config import tilda_ip
import time
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
        camera.start_preview()
        for i in range(1,6):
            print(f'{i}...')
            time.sleep(i)
        print('Ignition')
        camera.start_recording(connection, format='h264')
        camera.wait_recording(6000)
        camera.stop_recording()
finally:
    connection.close()
    client_socket.close()
