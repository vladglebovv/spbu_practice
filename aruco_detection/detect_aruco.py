import cv2
import argparse
import sys
import imutils
import asyncio
import numpy as np
from data_manipulation.data_types import PositionData

ARUCO_DICT = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
    "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
    "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
    "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
    "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

MARKER_SIZE_CM = 60


class ArucoMarkersDetector:
    def __init__(self, dict_name, marker_length, camera_matrix, dist_coeffs):
        if dict_name not in ARUCO_DICT:
            print(f"[INFO] ArUCo tag of '{dict_name}' is not supported")
            raise ValueError

        self.arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[dict_name])
        self.arucoParams = cv2.aruco.DetectorParameters_create()
        self.marker_length = marker_length
        self.camera_matrix = camera_matrix
        self.dist_coeffs = dist_coeffs

    async def get_markers_corners(self, img):
        (corners, ids, rejected) = cv2.aruco.detectMarkers(
            img,
            self.arucoDict,
            parameters=self.arucoParams
        )
        return corners, ids

    async def get_positions_from_corners(self, corners):
        rvecs, tvecs, _objPoints = cv2.aruco.estimatePoseSingleMarkers(	corners, self.marker_length, self.camera_matrix, self.dist_coeffs)
        return rvecs, tvecs

    async def get_positions_dict(self, img):
        res = dict()
        corners, markerIds = await self.get_markers_corners(img)
        if markerIds is not None:
            rvecs, tvecs = await self.get_positions_from_corners(corners)
            for id, rvec, tvec in zip(markerIds, rvecs, tvecs):
                res[id[0]] = PositionData.from_cv2(tvec, rvec)
        return res


async def main():
    cap = cv2.VideoCapture(0)

    cameraMatrix = np.array([[578.47,   0.,         337.02],
 [  0.,         592.64, 225.09],
 [  0.,           0.,           1.        ]])
    distCoeffs = np.array([[-0.15423951,  0.22055058, -0.00810331, -0.00137378, -0.22319865]])

    detec = ArucoMarkersDetector('DICT_7'
                                 'X7_50', MARKER_SIZE_CM, cameraMatrix, distCoeffs)
    while True:
        ret, img = cap.read()
        # img = imutils.resize(img, width=1000)
        corners, markerIds = await detec.get_markers_corners(img)
        rvecs, tvecs = await detec.get_positions_from_corners(corners)
        cv2.aruco.drawDetectedMarkers(img, corners, markerIds)
        # print(tvecs)
        pos1 = None
        pos2 = None
        if rvecs is not None and tvecs is not None:
            for rvec, tvec in zip(rvecs, tvecs):
                img = cv2.aruco.drawAxis(img, cameraMatrix, distCoeffs, rvec, tvec, MARKER_SIZE_CM)
            for id, rvec, tvec in zip(markerIds, rvecs, tvecs):
                if id == 3:
                    pos1 = PositionData.from_cv2(tvec, rvec)
                if id == 4:
                    pos2 = PositionData.from_cv2(tvec, rvec).inv()
            # if pos1 is not None and pos2 is not None:
            #     print(pos1.xyz, pos2.xyz, pos1.apply(pos2).xyz)
        cv2.imshow("ArUco Detector", img)
        cv_key = cv2.waitKey(10)
        if cv_key == 32:
            print(pos1, "pos1")
            print(pos2, "pos2")
            print(pos2.apply(pos1), "diff")
        if cv_key == 27 or not ret:
            cap.release()
            cv2.destroyAllWindows()
            sys.exit(0)

if __name__ == '__main__':
    asyncio.run(main())
