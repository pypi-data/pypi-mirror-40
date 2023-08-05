import os
from functools import wraps
from time import time

import numpy as np
from cv2 import cv2

EXTENSIONS = ['jpg', 'jpeg', 'png']


def get_images_in_dir(d):
    """get the relative path to all of the images in the given directory

    :param d: the directory to look in relative to the running process
    :type d: str
    :return: all of the image paths
    :rtype: list[str]
    """
    # list to store the paths to the images
    paths = []

    # get all the files in the directory
    for path in os.listdir(d):
        full_path = os.path.join(d, path)
        if os.path.isfile(full_path):
            paths.append(full_path)

    # filter out the files that don't have typical image extensions
    image_paths = [f for f in paths if f.split('.')[-1].lower() in EXTENSIONS]

    return image_paths


def get_fname_and_ext(path):
    """extract filename and extension from path.

    :param path: input path
    :type path: str
    :return: name and extension
    :rtype: tuple
    """

    # split the name and the ext
    name, ext = os.path.splitext(path)

    # get just the filename, remove the directory hierarchy
    name = name.split('/')[-1]
    return name, ext


def get_fname(path):
    """extract only the filename, excluding the extension from the path

    :param path: path including filename
    :type path: string / path
    :return: filename
    :rtype: string
    """
    name, _ = os.path.splitext(path)
    name = name.split('/')[-1]
    return name


def flip_kernel(kernel):
    """flip a kernel (probably to prep for convolution).

    :param img: the kernel
    :type img: matrix
    """
    k = np.copy(kernel)

    return(cv2.flip(k, -1))


def convolve(image, kernel):
    """convolve the image with the kernel.

    :param img: the image to convolve
    :type img: cv2 image
    :param kernel: the kernel to convolve with
    :type kernel: matrix
    """
    img = np.copy(image)

    return(cv2.filter2D(img, -1, flip_kernel(kernel)))


def distance(p, q):
    """calculates the euclidean distance between 2 points

    :param p: first point
    :type p: numpy array
    :param q: second point
    :type q: numpy array
    :return: distance
    :rtype: integer
    """
    return np.linalg.norm(p - q)


def resize(image, width):
    """resize the input image to specified width and maintain aspect ratio

    :param image: input image
    :type image: cv2 image
    :param width: output width
    :type width: integer
    :return: resized image
    :rtype: cv2 image
    """
    width = float(width)
    r = width / image.shape[1]
    dim = (int(width), int(image.shape[0] * r))

    # perform the actual resizing of the image and show it
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)


def resize_full(image, dim):
    """resize the input image to specified width, disregards aspect ratio

     :param image: input image
     :type image: cv2 image
     :param width: output width
     :type width: integer
     :return: resized image
     :rtype: cv2 image
     """
    # perform the actual resizing of the image and show it
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)


def combine_masks(a, b):
    return cv2.bitwise_and(a, b)


def bbox_from_contour(cnt):
    """Calculate bounding box and return the coordinates

    :param contour: contour
    :type contour: numpy array
    :return: bbox (x1, y1, x2, y2)
    :rtype: tuple
    """
    # using cnt[0] because contours are returned in a list, even though there
    # should only be a single contour in this function
    x, y, w, h = cv2.boundingRect(cnt[0])
    bbox = (x, y, x + w - 1, y + h - 1)
    return bbox


def crop_to_contour(image, cnt, padding=(0, 0)):
    """crop the image to the contour.

    :param image: input image
    :type image: cv2 image
    :param cnt: contours to crop to
    :type cnt: numpy array
    :param padding: padding to be added all around, defaults to (0, 0)
    :param padding: tuple, optional
    :return: cropped image
    :rtype: cv2 image
    """
    x1, y1, x2, y2 = bbox_from_contour(cnt)
    cropped = image[y1:y2, x1:x2]
    return cropped


def crop_to_bbox(image, bbox, padding=(0, 0), ignore=None):
    """crop the image to the bbox

    :param image: input image
    :type image: cv2 image
    :param cnt: bbox to crop to (x1, y1, x2, y2)
    :type cnt: tuple
    :param padding: padding to be added all around, defaults to (0, 0)
    :param padding: tuple, optional
    :param padding: crop axis to ignore, 'x' or 'y'
    :param padding: str, optional
    :return: cropped image
    :rtype: cv2 image
    """
    xmax, ymax, _ = image.shape

    x1, y1, x2, y2 = bbox
    x1 = max(x1 - padding[0], 0)
    y1 = max(y1 - padding[0], 0)
    x2 = min(x2 + padding[1], xmax)
    y2 = min(y2 + padding[1], ymax)

    # full crop
    if not ignore:
        cropped = image[y1:y2, x1:x2]
    # don't crop the x axis
    elif ignore is 'x':
        cropped = image[y1:y2, :]
    # don't crop the y axis
    elif ignore is 'y':
        cropped = image[:, x1:x2]

    return cropped


def timing(f):
    """decorator for timing functions

    :param f: function to be timed
    :type f: function
    :return: wrapped function
    :rtype: function
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        ts = time()
        result = f(*args, **kwargs)
        te = time()
        print('func:%r args:[%r, %r] took: %2.4f sec' %
              (f.__name__, args, kwargs, te - ts))
        return result
    return wrap


def test_correct(predict, actual, name='default test'):
    """compare two lists and provide statitics about how similar they are for testing.

    :param predict: predictions
    :type predict: list
    :param actual: actual
    :type actual: list
    :param name: name of the test for formatting, defaults to 'Test'
    :param name: str, optional
    """

    correct = 0
    incorrect = 0
    for i in range(len(predict)):
        if predict[i] is actual[i]:
            correct += 1
        else:
            incorrect += 1
    percent = (correct / (incorrect + correct)) * 100
    print('{}: {:.2f}% correct'.format(name, percent))


def fetch_rgb(img):
    """for outputing rgb values from click event to the terminal.

    :param img: input image
    :type img: cv2 image
    :return: the rgb list
    :rtype: list
    """
    rgb_list = []

    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            red = img[y, x, 2]
            blue = img[y, x, 0]
            green = img[y, x, 1]
            print(red, green, blue)  # prints to command line
            strRGB = str(red) + "," + str(green) + "," + str(blue)
            rgb_list.append([red, green, blue])
            cv2.imshow('original', img)
    cv2.imshow('original', img)
    cv2.setMouseCallback("original", click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows
    return rgb_list
