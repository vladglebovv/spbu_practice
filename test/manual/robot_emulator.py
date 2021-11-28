import socket
import time

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 54600        # Port to listen on (non-privileged ports are > 1023)

data = b'<Robot><Data><LastPos X="92.700218" Y="-49.260582" Z="512.477051" A="79.518661" B="-41.605556" C="22.007378"></LastPos></Data></Robot>'

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            s.sendall(data)
            time.sleep(0.1)
