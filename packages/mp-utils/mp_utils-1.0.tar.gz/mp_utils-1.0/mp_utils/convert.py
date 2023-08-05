import numpy as np
from cv2 import cv2


def gray_to_rgb(image):
    """convert cv2 image from GRAYSCALE to RGB

    :param image: the image to be converted
    :type image: cv2 image
    :return: converted image
    :rtype: cv2 image
    """
    return cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

def rgb_to_gray(image):
    """convert cv2 image from RGB to GRAY

    :param image: the image to be converted
    :type image: cv2 image
    :return: converted image
    :rtype: cv2 image
    """
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

def bgr_to_rgb(image):
    """convert from BGR order to RGB

    :param img: image to be converted
    :type img: cv2 image
    :return: converted image
    :rtype: cv2 image
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def rgb_to_bgr(image):
    """convert from RGB to BGR

    :param img: image to be converted
    :type img: cv2 image
    :return: converted image
    :rtype: cv2 image
    """
    return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


def bgr_to_gray(image):
    """convert from BGR to GRAYSCALE

    :param img: image to be converted
    :type img: cv2 image
    :return: converted image
    :rtype: cv2 image
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def gray_to_bgr(image):
    """convert from GRAYSCALE to BGR

    :param img: image to be converted
    :type img: cv2 image
    :return: converted image
    :rtype: cv2 image
    """
    return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

def bgr_to_lab(image):
    """convert from BGR to LAB

    :param img: image to be converted
    :type img: cv2 image
    :return: converted image
    :rtype: cv2 image
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

def lab_to_bgr(image):
    """convert from LAB to BGR

    :param img: image to be converted
    :type img: cv2 image
    :return: converted image
    :rtype: cv2 image
    """
    return cv2.cvtColor(image, cv2.COLOR_LAB2BGR)

def bgr_to_hsv(image):
    """convert from BGR to HSV
    :param img: image to be converted
    :type img: cv2 image
    :return: converted image
    :rtype: cv2 image
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

def hsv_to_bgr(image):
    """convert from HSV to BGR
    :param img: image to be converted
    :type img: cv2 image
    :return: converted image
    :rtype: cv2 image
    """
    return cv2.cvtColor(image, cv2.COLOR_HSV2BGR)


def bgr_to_yuv(image):
    """convert from BGR to YUV

    :param img: image to be converted
    :type img: cv2 image
    :return: converted image
    :rtype: cv2 image
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2YUV)

def yuv_to_bgr(image):
    """convert from BGR to YUV

    :param img: image to be converted
    :type img: cv2 image
    :return: converted image
    :rtype: cv2 image
    """
    return cv2.cvtColor(image, cv2.COLOR_YUV2BGR)

def contour_to_ptarray(cnt):
    """convert a cv2 contour array into an array of points that describe the shape
    
    :param cnt: contour array
    :type cnt: numpy array
    :return: point array
    :rtype: numpy array
    """
    return np.float32(cnt.reshape(-1, 2))

def ptarray_to_contour(ptarray):
    """convert an array of points into a contour array
    
    :param ptarray: point array
    :type ptarray: numpy array
    :return: contour array
    :rtype: numpy array
    """

    return ptarray.reshape(-1, 1, 2)