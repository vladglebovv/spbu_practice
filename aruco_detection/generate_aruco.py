import numpy as np
import argparse
import cv2
import sys
import uuid

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


def generate_marker(_id: int, output: str = None, type: int = cv2.aruco.DICT_ARUCO_ORIGINAL, tag_width: int = 300,
                    show: bool = False):
    if ARUCO_DICT.get(type, None) is None:
        raise ValueError('Wrong type!')

    if not output:
        output = f'aruco_tag_{type}_{_id}.png'

    arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
    tag = np.zeros((tag_width, tag_width, 1), dtype="uint8")
    cv2.aruco.drawMarker(arucoDict, _id, tag_width, tag, 1)
    cv2.imwrite(output, tag)
    if show:
        cv2.imshow("ArUCo Tag", tag)
        cv2.waitKey(0)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", required=False,
                    default=f'{uuid.uuid4().hex}.png',
                    help="path to output image containing ArUCo tag")
    ap.add_argument("-i", "--id", type=int, required=True,
                    help="ID of ArUCo tag to generate")
    ap.add_argument("-t", "--type", type=str,
                    default="DICT_ARUCO_ORIGINAL",
                    help="type of ArUCo tag to generate")
    args = vars(ap.parse_args())

    try:
        generate_marker(
            args["id"],
            args["output"],
            args["type"],
            show=True
        )
    except ValueError:
        print("[INFO] ArUCo tag of '{}' is not supported".format(
            args["type"])
        )
        sys.exit(0)
