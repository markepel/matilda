import socket
import subprocess
from imutils.video import VideoStream
# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

while True:
    
    print('Listening...')
    # Accept a single connection and make a file-like object out of it
    #connection = server_socket.accept()[0].makefile('rb')

    connection = server_socket.accept()[0].makefile('rb')
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
            data = connection.read(1024)
            if not data:
                raise Exception()
            print('Data recieved, data_format=={}'.format(type(data)))
                        #player.stdin.write(data)
    except:
        print('Exception')
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
