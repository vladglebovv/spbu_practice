import socket


class Transmitter:
    def __init__(self, ip, port):
        self.addr = (ip, port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(self.addr)

    def send_data(self, data):
        try:
            self.s.sendall(data.encode())
        except Exception:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect(self.addr)
            self.s.sendall(data.encode())

    def stop(self):
        self.s.close()
