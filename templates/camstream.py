import io
import socket
import struct
import time
import picamera
# client_socket = socket.socket()
# client_socket.connect(('my_server', 8000))

# connection = client_socket.makefile('wb')

def takePic():
    myfile = open('pic.jpeg','wb')
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        # camera.start_preview()
        time.sleep(0.5)
        camera.capture(myfile)

def getStream():
    try:
        camera = picamera.PiCamera()
        camera.resolution = (640, 480)
        camera.start_preview()
        time.sleep(2)

        start = time.time()
        stream = io.BytesIO()
        for foo in camera.capture_continuous(stream, 'jpeg'):


            # connection.write(struct.pack('<L', stream.tell()))
            # connection.flush()

            stream.seek(0)
            # connection.write(stream.read())


            if time.time() - start > 300:
                break


            stream.seek(0)
            stream.truncate()

    finally:
        print('done')
        # connection.close()
        # client_socket.close()       
