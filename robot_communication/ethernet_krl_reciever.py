import socket
import asyncio
import time
from data_manipulation.data_types import PositionData
from threading import Thread


class RobotServer:
    def __init__(self, ip, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stop = False
        self.ip = ip
        self.port = port
        self.tasks = list()
        self.last_pos = PositionData.get_base()
        loop = asyncio.get_event_loop()
        self.tasks.append(loop.create_task(self.run_server()))

    async def run_server(self):
        self.s.bind((self.ip, self.port))
        self.s.listen()
        self.s.setblocking(False)
        print('robot server wait')
        loop = asyncio.get_event_loop()
        while not self.stop:
            fut = loop.sock_accept(self.s)
            try:
                conn, addr = await asyncio.wait_for(fut, 1)
                print("robot connection from:", addr)
                self.tasks.append(loop.create_task(self.handle_client(conn)))
                # Thread(target=self.handle_client(conn)).start()

            except asyncio.TimeoutError:
                pass

    async def handle_client(self, conn):
        with conn:
            conn.setblocking(False)
            loop = asyncio.get_event_loop()
            while not self.stop:
                # data = conn.recv(1024).decode()
                data = (await loop.sock_recv(conn, 255)).decode()
                if not data:
                    break
                self.last_pos = PositionData.from_robot_string(data, t=time.time())

    async def stop_server(self):
        self.stop = True
        for task in self.tasks:
            try:
                await task
            except asyncio.TimeoutError:
                pass


async def main():
    # s = RobotServer('127.0.0.1', 54600)
    s = RobotServer('10.10.10.151', 20001)

    while True:
        if s.last_pos:
            print(s.last_pos.t, s.last_pos.xyz)
        await asyncio.sleep(1)
    await s.stop_server()
    print('---------------------')
    for i in range(5):
        print(i, s.last_pos.t)
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
