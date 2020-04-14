import socket
import struct
import time
import threading
import picamera
from config import tilda_ip, tilda_port, camera_resolution, camera_framerate
import io


try:
    client_socket = socket.socket()
    client_socket.connect((tilda_ip, tilda_port))
    print('connecting to {tilda_ip}:{tilda_port}...')
    connection = client_socket.makefile('wb')
    print(f'connected to {tilda_ip}:{tilda_port}')

    connection_lock = threading.Lock()

    class ImageStreamer(threading.Thread):
        def __init__(self):
            super(ImageStreamer, self).__init__()
            self.stream = io.BytesIO()
            self.event = threading.Event()
            self.terminated = False
            self.start()

        def run(self):
            # This method runs in a background thread
            while not self.terminated:
                # Wait for the image to be written to the stream
                if self.event.wait(3):
                    try:
                        connection.write(struct.pack('<L', self.stream.tell()))
                        connection.flush()
                        self.stream.seek(0)
                        connection.write(self.stream.read())
                    finally:
                        self.stream.seek(0)
                        self.stream.truncate()
                        self.event.clear()


    count = 0
    start = time.time()
    finish = time.time()

    def streamer_setter_generator(streamer):
        global count, finish
        print('streaming starts')
        while finish - start < 1800:
            yield streamer.stream
            streamer.event.set()
            count += 1
            finish = time.time()


    with picamera.PiCamera() as camera:
        # pool = [ImageStreamer() for i in range(4)]
        image_streamer = ImageStreamer()
        camera.resolution = camera_resolution
        camera.framerate = camera_framerate
        time.sleep(2)
        print('camera is ready')
        start = time.time()
        camera.capture_sequence(streamer_setter_generator(image_streamer), 'jpeg', use_video_port=True)

    # Shut down the streamers in an orderly fashion
    image_streamer.terminated = True
    image_streamer.join()

    # Write the terminating 0-length to the connection to let the server
    # know we're done
    with connection_lock:
        print('connection write last')
        connection.write(struct.pack('<L', 0))
    print('connection write ends')

finally:
    print('Sent %d images in %d seconds at %.2ffps' % (count, finish-start, count / (finish-start)))
    connection.close()
    client_socket.close()
