import picamera
# import picamera.array
# import socket
import time
import io



print('Starting')

try:
    #vs = imutils.VideoStream(src=0, usePicamera=True, resolution=(720, 576)).start()

    #for i in range(1,6):
     #  print(f'{i}...')
      #  time.sleep(i)
    #print('Ignition')
    #while True:
     #   frame = vs.read()
        #client_socket.sendall(frame)
counter = 0
with picamera.PiCamera() as camera:
    camera.start_preview()
    time.sleep(2)
    for filename in camera.capture_continuous(f'img{counter}.jpg'):
        print(f'Captured {filename}')
        time.sleep(0.4) # wait 5 minutes

    # with picamera.PiCamera() as camera:
    #     camera.resolution = (640, 480)
    #     camera.framerate = 4
    #     # stream = io.BytesIO()
    #     # rawCapture = picamera.PiRGBArray(camera, size=(640, 480))

    #     # camera.start_preview()
    #     for i in range(1,3):
    #         print(f'{i}...')
    #         time.sleep(i)
    #     print('Ignition')

    #     camera.start_recording(connection, format='mjpeg')
    #     camera.wait_recording(1000)
    #     camera.stop_recording()

        # for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # for foo in camera.capture_continuous(stream, format='jpeg'):

            # encoded, buffer = cv2.imencode('.jpg', frame)
            # print('foo = {}, type = {}'.format(foo, type(foo)))
            # clear the stream in preparation for the next frame
            # stream.truncate(0)
            # stream.seek(0)

        # with picamera.array.PiRGBArray(camera) as stream:
            # image = 1
            # while image is not None:
            #     camera.capture(stream, format='bgr')
            #     image = stream.array
            #     print('image ={} len = {}'.format(image, len(image)))
except Exception as e:
    print(f'Exception {e}')
finally:
    connection.close()
    client_socket.close()
