import numpy as np
from cv2 import cv2


def read_gray32(img_path):
    """read in the image from the path as a grayscale and convert to float32.

    :param img_path: path to the image
    :type img_path: string
    :return: the loaded image
    :rtype: cv2 image
    """
    # load the image and convert to float32
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = np.float32(img)

    return img


def read_gray(img_path):
    """read in the image from the path as a grayscale image.

    :param img_path: path to the image
    :type img_path: string
    :return: the loaded image
    :rtype: cv2 image
    """
    # load the image and convert to float32
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    return img


def read_color(img_path):
    """read in the image from the path as BGR color.

    :param img_path: path to the image
    :type img_path: string
    :return: the loaded image
    :rtype: cv2 image
    """
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)

    return img