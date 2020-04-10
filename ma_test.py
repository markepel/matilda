import picamera
import time

counter = 0
print('a')
with picamera.PiCamera() as camera:
    print('b')
    camera.start_preview()
    print('c')
    time.sleep(2)
    print('d')
    for filename in camera.capture_continuous('img{counter:03d}.jpg'):
        print(f'Captured {filename}')
        counter+=1
        time.sleep(4)