import asyncio
import cv2
import numpy as np
from aruco_detection.detect_aruco import ArucoMarkersDetector
from data_manipulation.data_types import PositionData
from robot_communication.ethernet_krl_reciever import RobotServer
from aruco_detection.img_input import FromCamera
from concurrent.futures import ProcessPoolExecutor
from data_transmition.transmitter import Transmitter


MARKER_SIZE_CM = 60


async def main():
    cameraMatrix = np.array([[578.47,   0.,         337.02],
 [  0.,         592.64, 225.09],
 [  0.,           0.,           1.        ]])
    distCoeffs = np.array([[-0.15423951,  0.22055058, -0.00810331, -0.00137378, -0.22319865]])

    detec = ArucoMarkersDetector('DICT_7X7_50', MARKER_SIZE_CM, cameraMatrix, distCoeffs)
    # s = Transmitter('127.0.0.1', 54600)
    cam = FromCamera(0)

    base_to_mark1 = PositionData.get_base()
    mark2_to_tool = PositionData.get_base()

    id1 = 4
    id2 = 3

    last_tool =  PositionData.get_base()
    tools = list()

    while True:
        img = await cam.get_image()
        pos_dict = await detec.get_positions_dict(img)
        cv2.imshow("ttt", img)
        if cv2.waitKey(10) == 32:
            tmp = np.array(tools)
            print(np.mean(tmp, axis=0))
            tools = list()
        # print(pos_dict)
        # s.send_data(last_tool.to_json_str())
        if id1 not in pos_dict or id2 not in pos_dict:
            continue
        last_tool = pos_dict[id1].inv().apply(pos_dict[id2])
        tools.append(last_tool.xyz)
        print(last_tool)

if __name__ == '__main__':
    asyncio.run(main())

