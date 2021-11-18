import numpy as np
import cv2
import argparse


def calibrate(chessboard_size, size_of_chessboard_squares_mm, img):
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

    # size_of_chessboard_squares_mm = 20
    objp = objp * size_of_chessboard_squares_mm

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners)
        # Draw and display the corners
        cv2.drawChessboardCorners(img, chessboard_size, corners2, ret)

    mtx, dist = None, None
    try:
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape, None, None)
    except Exception:
        pass
    return mtx, dist, img


if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-cw", "--chessboard_width",
        type=int,
        required=True,
        help="Width of chessboard"
    )
    ap.add_argument(
        "-ch", "--chessboard_height",
        type=int,
        required=True,
        help="Height of chessboard"
    )
    ap.add_argument(
        "-fw", "--frame_width",
        type=int,
        help="Width of frame")
    ap.add_argument(
        "-fh", "--frame_height",
        type=int,
        required=True,
        help="Height of frame"
    )
    ap.add_argument(
        "-ss", "--square_size",
        type=int,
        required=True,
        help="Size of chessboard squarex"
    )
    ap.add_argument(
        "-p", "--path_to_images",
        required=False,
        type=str,
        default='*.png',
        help="Path to images, used for calibration"
    )
    args = vars(ap.parse_args())

    cap = cv2.VideoCapture(0)
    ret, img = cap.read()
    mtx, dist, o_img = calibrate((args['chessboard_width'], args['chessboard_height']), args['square_size'], img)
    mean_dist = np.array(dist)
    mead_mtx = np.array(mtx)
    while True:
        ret, img = cap.read()
        mtx, dist, o_img = calibrate((args['chessboard_width'], args['chessboard_height']), args['square_size'], img)
        mean_dist = mean_dist + np.array(dist) / 2.0
        mean_mtx = mean_mtx + np.array(mtx) / 2.0
        cv2.imshow('', img)
        cv2.waitKey(1)
        if mtx is not None and dist is not None:
            print(mead_mtx, mean_dist)
