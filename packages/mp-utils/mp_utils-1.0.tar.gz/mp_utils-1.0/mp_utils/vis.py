import math

import numpy as np
from cv2 import cv2
from matplotlib import pyplot as plt


def show(images, title='image'):
    """show a opencv2 window that can be destroyed with any key.

    this will only work if the images are all of the same size.

    :param img: images to show
    :type img: list[cv2 image]
    :param title: title of the window to create, defaults to 'image'
    :type title: string
    """
    # if images is not a list make it one
    if type(images) is not list:
        images = [images]

    # check if the list is greater than 1 and concat the images for opencv
    if len(images) > 1:
        cv2.imshow(title, np.hstack(images))
    else:
        cv2.imshow(title, images[0])
    cv2.waitKey(0)
    cv2.destroyWindow(title)


def save_mpl_subplot(plot, filename):
    """save the mpl subplot with dpi high enough that lines are not lost!

    :param plot: the mpl plot
    :type plot: mpl plot
    :param filename: the name to give the file including dir
    :type filename: str
    """

    plot.savefig(filename, dpi=300)


def create_mpl_subplot(images, color=True):
    """create mpl subplot with all images in list.

    even when the color is set to false it still seems to

    :param images: the list of images to plot
    :type images: cv2 image
    :param color: whether to plot in color or grayscale, defaults to True
    :type color: boolean
    :return: the complete plot
    :rtype: mpl plot
    """
    if not color:
        plt.set_cmap('gray')

    n = math.ceil(math.sqrt(len(images)))
    i = 1

    for img in images:
        plt.subplot(n, n, i)
        plt.imshow(img)
        plt.xticks([]), plt.yticks([])
        i += 1

    return plt


def create_mpl_histogram_gray(img):
    """create mpl histogram from the supplied grayscale image.

    :param img: the loaded image
    :type img: cv2 image
    :return: the computed histogram
    :rtype: mpl plot
    """

    plt.hist(img.ravel(), 256, [0, 256])
    return plt


def create_mpl_histogram_color(img, order=('r', 'g', 'b')):
    """create mpl histogram from the supplied image.

    this can deal with bgr, or rgb images.

    :param img: the loaded image
    :type img: cv2 image
    :param order: the channel ordering, defaults to ('r', 'g', 'b')
    :type order: tuple, optional
    :return: the computed histogram
    :rtype: mpl plot
    """
    plt.figure()
    plt.title("'Flattened' Color Histogram")
    plt.xlabel("Bins")
    plt.ylabel("# of Pixels")

    chans = cv2.split(img)

    # loop over the image channels
    for (chan, color) in zip(chans, order):
        hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
        plt.plot(hist, color=color)
        plt.xlim([0, 256])

    return plt
