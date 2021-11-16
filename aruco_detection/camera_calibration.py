import numpy as np
import cv2 as cv
import glob
import argparse


def calibrate(chessboard_size, frame_size, size_of_chessboard_squares_mm, path_to_calebrate_images = '*.png')
    ################ FIND CHESSBOARD CORNERS - OBJECT POINTS AND IMAGE POINTS #############################

    # chessboardSize = (24, 17)
    # frameSize = (1440, 1080)

    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessboardSize[0], 0:chessboardSize[1]].T.reshape(-1, 2)

    # size_of_chessboard_squares_mm = 20
    objp = objp * size_of_chessboard_squares_mm

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    images = glob.glob(path_to_calebrate_images)

    for image in images:

        img = cv.imread(image)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, chessboardSize, None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners)

    ############## CALIBRATION #######################################################

    ret, cameraMatrix, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, frameSize, None, None)
    return cameraMatrix, dist

############## UNDISTORTION #####################################################

# img = cv.imread('cali5.png')
# h, w = img.shape[:2]
# newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, dist, (w, h), 1, (w, h))

# # Undistort
# dst = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

# # crop the image
# x, y, w, h = roi
# dst = dst[y:y + h, x:x + w]
# cv.imwrite('caliResult1.png', dst)

# # Undistort with Remapping
# mapx, mapy = cv.initUndistortRectifyMap(cameraMatrix, dist, None, newCameraMatrix, (w, h), 5)
# dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)

# # crop the image
# x, y, w, h = roi
# dst = dst[y:y + h, x:x + w]
# cv.imwrite('caliResult2.png', dst)

# # Reprojection Error
# mean_error = 0

# for i in range(len(objpoints)):
#     imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], cameraMatrix, dist)
#     error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
#     mean_error += error

# print("total error: {}".format(mean_error / len(objpoints)))

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
        type=str
        default='*.png'
        help="Path to images, used for calibration"
    )
    args = vars(ap.parse_args())

    pritn(
        calibrate(
            (args['chessboard_width'], args['chessboard_height']),
            (args['frame_width'], args['frame_height']),
            args['square_size'],
            args['path_to_image']
        )
    )
