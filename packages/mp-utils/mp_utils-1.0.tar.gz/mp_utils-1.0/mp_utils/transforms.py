import numpy as np
from cv2 import cv2
import mp_utils.convert as convert


def get_xform(src, dst):
    """get the transform between the two input arrays
    
    :param src: source points
    :type src: numpy array
    :param dst: destination points
    :type dst: numpy array
    :return: transform matrix
    :rtype: numpy array
    """
    return cv2.getPerspectiveTransform(src, dst)

def xform(image, src, dst):
    """perform the xform on the image
    
    :param image: image to perform the transform on
    :type image: cv2 image
    :param src: contour decribing the part of the image to be xformed
    :type src: cv2 contour
    :param dst: destination to xform the area described by the contour to
    :type dst: np array
    :return: the xformed image
    :rtype: cv2 image
    """
    # convert the source 'contour' to something we can work with
    src = convert.contour_to_ptarray(src)
    # get the xform matrix
    M = get_xform(src, dst)
    # return the xformed image
    return cv2.warpPerspective(image, M, _get_output_size(dst))
    

def _get_output_size(dst):
    """return the max of each axis in a numpy point array
    
    :param dst: xform destination array
    :type dst: numpy array
    :return: maximum for each axis
    :rtype: tuple
    """
    max_x = np.max(dst[:, 0])
    max_y = np.max(dst[:, 1])
    return max_x, max_y