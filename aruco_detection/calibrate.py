import numpy as np
import cv2


def draw_pattern(chessboard_size, img):
    '''! Draw chess pattern on image if can find it

    :param chessboard_size: typle(int, int)
        size of chessboard for detection

    :param img:
    :return:
    '''
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)
    # If found, add object points, image points (after refining them)
    if ret == True:
        cv2.drawChessboardCorners(img, chessboard_size, corners, ret)
    return img


def calibrate(chessboard_size, size_of_chessboard_squares_mm, imgs):
    """! Calculate camera matrix and dist coefficients

    :param chessboard_size: tuple(int, int)
        Size of chess board pattern

    :param size_of_chessboard_squares_mm:
        ...

    :param imgs: list
        list of images for rpocessing

    :return: matrix, array
        Camera matrix and dist coefficients
    """
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

    # size_of_chessboard_squares_mm = 20
    objp = objp * size_of_chessboard_squares_mm

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.
    gray = None

    for img in imgs:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

    mtx, dist = None, None
    try:
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape, None, None)
    except Exception:
        pass
    return mtx, dist


def main_make_images(folder_name: str):
    '''! show 0 camera, press space to save image in given folder

    :param folder_name:str
        folder name to save images (relative from script)

    :return: None
    '''
    cap = cv2.VideoCapture(0)
    i = 1
    while True:
        ret, img = cap.read()
        print(type(img))
        img_old = img.copy()
        img = draw_pattern((4, 4), 40, img)
        cv2.imshow('', img)
        if cv2.waitKey(10) == 32:
            cv2.imwrite(f"{folder_name}/im{i}.png", img_old)
            print(i)
            i = i + 1


def main_make_calib(folder_name, n):
    imgs = list()
    for i in range(1, n+1):
        img = cv2.imread(f"{folder_name}/im{i}.png")
        imgs.append(img)
    mean_mtx, mean_dist = calibrate((4, 4), 40, imgs)
    for img in imgs:
        img2 = img.copy()
        img2 = cv2.undistort(img2, mean_mtx, mean_dist)
        cv2.imshow('', img2)
        cv2.waitKey()
    print(mean_mtx, mean_dist)


if __name__ == '__main__':
    img_folder_name = 'imgs1'
    main_make_images(img_folder_name)
    # main_make_calib(img_folder_name, 14)
