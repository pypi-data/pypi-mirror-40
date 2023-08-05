import numpy as np
from cv2 import cv2
import mp_utils.vis as vis
import mp_utils.convert as convert
import mp_utils.utils as utils
import mp_utils.io as io


def match(test, exemplar_descs):
    """using ORB decriptors compute match between test and exemplar_descs.
    
    :param test: image to test
    :type test: cv2 image
    :param exemplar: exemplar descriptions
    :type exemplar: list of orb descriptors
    :return: distance sorted matches
    :rtype: list
    """
    # create an ORB object
    orb = cv2.ORB_create()

    # convert to GRAYSCALE
    test_g = convert.bgr_to_gray(test)

    # Find the keypoints and descriptors with ORB
    _, descs = orb.detectAndCompute(test_g, None)

    # create a brute force matcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # init to hold the best prediciton
    prediction = ('(none)', np.inf)

    # match with each exmplar
    for d in exemplar_descs:
        # match the descriptors
        matches = bf.match(d[1], descs)

        # sort in order of distance, lowest first
        sorted_matches = sorted(matches, key=lambda x:x.distance)

        # extract just the distances
        distances = [m.distance for m in sorted_matches]

        # calculate a score
        score = sum(distances[:4])

        # no matches
        if score == 0:
            score = np.inf
        # update prediction because this match is closer
        if score < prediction[1]:
            prediction = (d[0], score)

    return prediction[0]

def load_symbols(dirname):
    """load all symbols from the directory.
    
    :param dirname: directory path
    :type dirname: str
    :return: loaded images and names
    :rtype: tuple
    """
    symbol_images = [(utils.get_fname(s), io.read_color(s)) for s in dirname]
    return symbol_images

def create_descriptions(dirname):
    """pre-compute a list of descriptors for ORB matching.
    
    :param dirname: directory to find the images to use
    :type dirname: str
    :return: descriptors and filenames
    :rtype: list of tuples
    """
    descs = []
    symbols = load_symbols(dirname)

    orb = cv2.ORB_create()

    for s in symbols:
        gray = convert.bgr_to_gray(s[1])
        _, desc = orb.detectAndCompute(gray, None)
        descs.append((s[0], desc))

    return descs
