import asyncio
import cv2
import numpy as np
from aruco_detection.detect_aruco import ArucoMarkersDetector
from data_manipulation.data_types import PositionData
from robot_communication.ethernet_krl_reciever import RobotServer
from aruco_detection.img_input import FromCamera
from concurrent.futures import ProcessPoolExecutor
from data_transmition.reciever import DataServer

MARKER_SIZE_CM = 6.0


async def main():
    cameraMatrix = np.array([[578.47,   0.,         337.02],
 [  0.,         592.64, 225.09],
 [  0.,           0.,           1.        ]])
    distCoeffs = np.array([[-0.15423951,  0.22055058, -0.00810331, -0.00137378, -0.22319865]])

    detec = ArucoMarkersDetector('DICT_5X5_50', MARKER_SIZE_CM, cameraMatrix, distCoeffs)
    s = RobotServer('10.10.10.151', 20001)
    s2 = DataServer('127.0.0.1', 54600)
    pred = 0
    while True:
        await asyncio.sleep(1)
        if pred != max(s.last_pos.t, s2.last_pos.t):
            print(s.last_pos, "robot")
            print(s2.last_pos, "marker")
            pred = max(s.last_pos.t, s2.last_pos.t)

if __name__ == '__main__':
    asyncio.run(main())

