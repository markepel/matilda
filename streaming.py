import io
import socket
import struct
import time
import threading
import picamera
from config import tilda_ip


client_socket = socket.socket()
client_socket.connect((tilda_ip, 8008))
print('connecting...')
connection = client_socket.makefile('wb')
print('connected')

try:
    connection_lock = threading.Lock()
    pool_lock = threading.Lock()
    pool = []

    class ImageStreamer(threading.Thread):
        def __init__(self):
            super(ImageStreamer, self).__init__()
            print('init image streamer')
            self.stream = io.BytesIO()
            self.event = threading.Event()
            self.terminated = False
            self.start()

        def run(self):
            # This method runs in a background thread
            while not self.terminated:
                # Wait for the image to be written to the stream
                print('image_streamer:waiting for event')
                if self.event.wait(1):
                    try:
                        print('image_streamer:got event')
                        with connection_lock:
                            print('image_streamer:start writing')
                            connection.write(struct.pack('<L', self.stream.tell()))
                            print('image_streamer:writing first message')
                            connection.flush()
                            self.stream.seek(0)
                            connection.write(self.stream.read())
                            print('image_streamer:wrote stream read to connection')
                    finally:
                        print('image_streamer:finally')
                        self.stream.seek(0)
                        self.stream.truncate()
                        self.event.clear()
                        with pool_lock:
                            pool.append(self)

    count = 0
    start = time.time()
    finish = time.time()

    def streams():
        global count, finish
        while finish - start < 300:
            with pool_lock:
                if pool:
                    streamer = pool.pop()
                    print('streams:streamer popped')
                else:
                    streamer = None
            if streamer:
                yield streamer.stream
                streamer.event.set()
                print('streams:set streamer')
                count += 1
            else:
                # When the pool is starved, wait a while for it to refill
                time.sleep(0.1)
            finish = time.time()

    with picamera.PiCamera() as camera:
        pool = [ImageStreamer()]
        camera.resolution = (640, 480)
        camera.framerate = 3
        time.sleep(2)
        start = time.time()
        camera.capture_sequence(streams(), 'jpeg', use_video_port=True)

    # Shut down the streamers in an orderly fashion
    while pool:
        streamer = pool.pop()
        streamer.terminated = True
        streamer.join()

    # Write the terminating 0-length to the connection to let the server
    # know we're done
    with connection_lock:
        connection.write(struct.pack('<L', 0))

finally:
    connection.close()
    client_socket.close()

print('Sent %d images in %d seconds at %.2ffps' % (
    count, finish-start, count / (finish-start)))