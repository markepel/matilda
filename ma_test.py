import picamera
import time


print('a')
with picamera.PiCamera() as camera:
    print('b')
    camera.start_preview()
    print('c')
    time.sleep(2)
    print('d')
    for filename in camera.capture_continuous(f'img{counter}.jpg'):
        print(f'Captured {filename}')
        time.sleep(4)