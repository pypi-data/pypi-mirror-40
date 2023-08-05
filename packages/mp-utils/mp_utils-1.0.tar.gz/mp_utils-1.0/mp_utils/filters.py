import numpy as np
from cv2 import cv2
import mp_utils.convert as convert


def apply_gaussian_blur(image, n, border=0):
    """apply a gaussian blur to the image.

    :param img: the loaded image
    :type img: cv2 image
    :param n: the size of the kernel n x n
    :type n: int
    :param border: what to do when the kernel overlaps the border, defaults to 0
    :param border: int, optional
    :return: copy of the blurred image
    :rtype: cv2 image
    """
    return cv2.GaussianBlur(image, (n, n), border)


def median_blur(image, n, border=0):
    """apply a median blur of kernel size n to the image.

    :param image: input image
    :type image: cv2 image
    :param n: kernel size
    :type n: int
    :param border: what to do when the kernel overlaps the border, defaults to 0
    :param border: int, optional
    :return: blurred image
    :rtype: cv2 image
    """
    return cv2.medianBlur(image, n, border)


def normalise(image):
    """normalise an images values.

    :param img: the loaded image in grayscale
    :type img: cv2 image
    :return: copy of the normalised image
    :rtype: cv2 image
    """
    img = np.copy(image)

    maximum = np.max(img)

    img = np.absolute(img)

    img = img * (255.0 / maximum)

    return img


def normlise_intensity(image):
    """normalise the intensity of the image.

    using an adaptive method convert the image to LAB and normalise the
    intensity channel before merging and converting back to BGR.

    :param image: image to be normalised
    :type image: cv2 image
    :return: normalised image
    :rtype: cv2 image
    """
    # convert to LAB
    lab = convert.bgr_to_lab(image)
    # split into individual channels
    l, a, b = cv2.split(lab)

    # normalise the intensity
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)

    # merge the image back together
    lab_img = cv2.merge([l, a, b])
    # convert back to BGR and return it
    return convert.lab_to_bgr(lab_img)


def white_balance(img):
    """apply white balancing to this image.

    this code comes from a stack overflow post by norok2 which can be found here: 
    https://stackoverflow.com/questions/46390779/automatic-white-balancing-with-grayworld-assumption

    :param img: input image
    :type img: cv2 image
    :return: white balanced image
    :rtype: cv2 image
    """
    result = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    avg_a = np.average(result[:, :, 1])
    avg_b = np.average(result[:, :, 2])
    result[:, :, 1] = result[:, :, 1] - \
        ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result[:, :, 2] = result[:, :, 2] - \
        ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
    return result
