import socket
import time
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sn

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 20001        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        last = time.time()
        time_list = list()
        for i in range(1, 5000):
            data = conn.recv(1024)
            curr = time.time()
            print(data, curr-last)
            time_list.append(curr - last)
            last = curr
            if not data:
                break
            # conn.sendall(data)

time_list = np.array(time_list)
print(np.max(time_list))
print(np.min(time_list))
res = sn.kdeplot(time_list)
plt.grid()
plt.show()

