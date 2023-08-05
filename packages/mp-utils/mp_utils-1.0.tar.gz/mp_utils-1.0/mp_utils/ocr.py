import numpy as np
from cv2 import cv2
import operator
import pytesseract

import mp_utils.filters as filters
import mp_utils.vis as vis
import mp_utils.convert as convert
import mp_utils.features as features
import mp_utils.utils as utils


def extract_all_words(image, filter='CAPS'):
    """extract all of the words form the image.

    extracts words from the inverse and normal threshold of the input image so
    and joins these lists together. this is because pytesseract likes black text
    on a white background.

    :param image: input image
    :type image: cv2 image
    :return: extracted words
    :rtype: list
    """
    # standard and inverse threshold so that at least one of the images
    # is black text on white background tessearact likes this more
    variations = []
    _, thresh = cv2.threshold(convert.bgr_to_gray(
        image), 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    variations.append(thresh)
    _, thresh_inv = cv2.threshold(convert.bgr_to_gray(
        image), 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    variations.append(thresh_inv)

    # get the text from each version of the image
    if filter is 'CAPS':
        text = []
        for v in variations:
            text.append(get_caps(v))
        return text
    elif filter is 'NUMS':
        text = []
        for v in variations:
            text.append(get_nums(v))
        return text


def get_nums(image):
    """get the words from an image using pytesseract.

    the extracted words are cleaned and all spaces, newlines and non uppercase
    characters are removed.

    :param image: inpout image
    :type image: cv2 image
    :return: extracted words
    :rtype: list
    """
    
    # pytesseract config
    config = ('--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789/')

    # extract text and preprocess
    text = pytesseract.image_to_string(image, config=config)
    text = ''.join([c for c in text if c.isdigit() or c in ['\n', ' ', '.']])

    # return as a lis
    return text.split()


def get_caps(image):
    """get the words from an image using pytesseract.

    the extracted words are cleaned and all spaces, newlines and non uppercase
    characters are removed.

    :param image: inpout image
    :type image: cv2 image
    :return: extracted words
    :rtype: list
    """
    # pytesseract config
    # config = ('-l eng --oem 1 --psm 3')
    config = ('-l eng --psm 1 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    # extract text and preprocess
    text = pytesseract.image_to_string(image, config=config)
    text = ''.join([c for c in text if c.isupper() or c in ['\n', ' ']])

    # return as a list
    return text.split()


def determine_label(words, dictionary):
    """from a list of words and a dictionary determine the closest label.

    :param words: candidate words extracted via ocr
    :type words: list
    :param dictionary: dictionary with lists of corrections
    :type dictionary: dict
    :return: label
    :rtype: str
    """
    # to store the candidates and their scores
    candidates = {}

    # for each candidate iterate through the dictionary and calculate a score
    for w in words:
        for key, value in dictionary.items():
            score = 0
            for v in value:
                # check exact match
                if w == v:
                    score += 4
                # check substring match
                elif v in w:
                    score += 1
            if key in candidates:
                candidates[key] += score
            else:
                candidates[key] = score

    # sort the candidate dict based on the score, highest first
    sorted_candidates = sorted(
        candidates.items(), key=operator.itemgetter(1), reverse=True)

    # if there are no candidates or the score of the top candidate is 0
    if (not sorted_candidates) or (sorted_candidates[0][1] == 0):
        label = '(none)'
    # if there is a top scoring candidate
    else:
        label = sorted_candidates[0][0]

    return label


def find_optimal_components_subset(contours, edges):
    """Find a crop which strikes a good balance of coverage/compactness.

    Adapted from https://github.com/danvk/oldnyc/blob/master/ocr/tess/crop_morphology.py
    Copyright 2015 danvk
    Copyright 2018 kevinglasson
    http://www.apache.org/licenses/LICENSE-2.0

    :param contours: countours
    :type contours: numpy array of points
    :param edges: image the countours are from
    :type edges: cv2 image
    :return: crop coordinates (x1, y1, x2, y2)
    :rtype: tuple
    """
    c_info = props_for_contours(contours, edges)
    c_info.sort(key=lambda x: x['sum'], reverse=True)
    total = np.sum(edges) / 255
    area = edges.shape[0] * edges.shape[1]

    c = c_info[0]
    del c_info[0]
    this_crop = c['x1'], c['y1'], c['x2'], c['y2']
    crop = this_crop
    covered_sum = c['sum']

    while covered_sum < total:
        changed = False
        recall = 1.0 * covered_sum / total
        prec = 1 - 1.0 * crop_area(crop) / area
        f1 = 2 * (prec * recall / (prec + recall))
        # print '----'
        for i, c in enumerate(c_info):
            this_crop = c['x1'], c['y1'], c['x2'], c['y2']
            new_crop = union_crops(crop, this_crop)
            new_sum = covered_sum + c['sum']
            new_recall = 1.0 * new_sum / total
            new_prec = 1 - 1.0 * crop_area(new_crop) / area
            new_f1 = 2 * new_prec * new_recall / (new_prec + new_recall)

            # Add this crop if it improves f1 score,
            # _or_ it adds 25% of the remaining pixels for <10% crop expansion.
            # ^^^ very ad-hoc! make this smoother
            remaining_frac = c['sum'] / (total - covered_sum)
            new_area_frac = 1.0 * crop_area(new_crop) / crop_area(crop) - 1
            if new_f1 > f1 or (
                    remaining_frac > 0.25 and new_area_frac < 0.10):
                    # print('%d %s -> %s / %s (%s), %s -> %s / %s (%s), %s -> %s' % (
                    # i, covered_sum, new_sum, total, remaining_frac,
                    # crop_area(crop), crop_area(new_crop), area, new_area_frac,
                    # f1, new_f1))
                crop = new_crop
                covered_sum = new_sum
                del c_info[i]
                changed = True
                break

        if not changed:
            break

    return crop


def props_for_contours(contours, ary):
    """Calculate bounding box & the number of set pixels for each contour.

    Adapted from https://github.com/danvk/oldnyc/blob/master/ocr/tess/crop_morphology.py
    Copyright 2015 danvk.
    http://www.apache.org/licenses/LICENSE-2.0

    :param contours: contours
    :type contours: numpy array
    :param ary: image the contours are from
    :type ary: cv2 image
    :return: contour info
    :rtype: [dicts]
    """
    c_info = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        c_im = np.zeros(ary.shape)
        cv2.drawContours(c_im, [c], 0, 255, -1)
        c_info.append({
            'x1': x,
            'y1': y,
            'x2': x + w - 1,
            'y2': y + h - 1,
            'sum': np.sum(ary * (c_im > 0))/255
        })
    return c_info


def union_crops(crop1, crop2):
    """Union two (x1, y1, x2, y2) rects.

    Adapted from https://github.com/danvk/oldnyc/blob/master/ocr/tess/crop_morphology.py
    Copyright 2015 danvk.
    http://www.apache.org/licenses/LICENSE-2.0

    :param crop2: crop coordinates
    :type crop2: tuple
    :param crop2: crop coordinates
    :type crop2: tuple
    :return: coordinates of the union of two crops
    :rtype: tuple
    """
    x11, y11, x21, y21 = crop1
    x12, y12, x22, y22 = crop2
    return min(x11, x12), min(y11, y12), max(x21, x22), max(y21, y22)


def crop_area(crop):
    """calculate the area of a crop (x1, y1, x2, y2).

    Adapted from https://github.com/danvk/oldnyc/blob/master/ocr/tess/crop_morphology.py
    Copyright 2015 danvk.
    http://www.apache.org/licenses/LICENSE-2.0

    :param crop: crop coordinates
    :type crop: tuple
    :return: area of the crop
    :rtype: int
    """
    x1, y1, x2, y2 = crop
    return max(0, x2 - x1) * max(0, y2 - y1)


def find_text(image):
    """attempt to isolate the text in the image.
    
    :param image: input image
    :type image: cv2 image
    :return: contours, cropped image, if text is found
    :rtype: cv2 cnts, cv2 image, boolean
    """
    # convert to GRAYSCALE
    g_label = convert.bgr_to_gray(image)

    # binarise the image
    _, thresh = cv2.threshold(
        g_label, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # detect edges
    canny = features.apply_canny(thresh, 175, 190)

    # blur
    blur = filters.median_blur(canny, 3)

    # xor between canny and blur to attempt to remove some fo the lines from the diamond
    text_im = cv2.bitwise_xor(canny, blur)

    # blur again
    text_blur = filters.apply_gaussian_blur(text_im, 3)

    # attemtp to dilate the text so it is one big blob
    kernel_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1))
    dilated = cv2.dilate(text_blur, kernel_rect, iterations=6)

    # attempt to remove anythin gthat is not veritcal or horizontal i.e. lines form the diamond
    kernel_cross = cv2.getStructuringElement(cv2.MORPH_CROSS, (7, 7))
    erosion = cv2.erode(dilated, kernel_cross, iterations=2)

    # threshold the image again
    _, thresh_dilated = cv2.threshold(
        erosion, 127, 255, cv2.THRESH_BINARY)

    # blur again
    td_blur = filters.median_blur(thresh_dilated, 9)

    # dilate the text into itself
    kernel_rect2 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 2))
    td_dilate = cv2.dilate(td_blur, kernel_rect2, iterations=10)

    for _ in range(12):
        td_dilate = filters.apply_gaussian_blur(td_dilate, 5)
        td_dilate = cv2.dilate(td_blur, kernel_rect2, iterations=10)

    kernel_rect3 = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 8))
    td_dilate = cv2.dilate(td_dilate, kernel_rect3, iterations=3)

    # find contours that encompass the areas text could be
    _, cnts, _ = cv2.findContours(
        td_dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # report whether contours weere foun
    if cnts:
        found = True
        # optimise the contours found to only include the important ones
        bbox = find_optimal_components_subset(cnts, td_dilate)
        # crop to the optimal height, keep the entire width
        im = utils.crop_to_bbox(image, bbox, ignore='x')
    else:
        found = False
        im = image 

    return im, found

def find_text_pytess(image):
    """use pytesseract to attempt to find the text.
    
    :param image: input image
    :type image: cv2 image
    :return: words found
    :rtype: cv2 image
    """
    # attempt to find the box around the number
    box = pytesseract.image_to_boxes(image)
    # if one exists
    if box:
        # each box is separated by a newline
        box = box.split('\n')
        # init values for 'final' box
        x1, y1, x2, y2 = np.inf, np.inf, 0, 0
        # combine the boxes into one box that encompasses all of them
        for b in box:
            b = b.split(' ')[1:-1]
            tup = tuple([int(i) for i in b])
            x1 = min(tup[0], x1)
            y1 = min(tup[1], y1)
            x2 = max(tup[2], x2)
            y2 = max(tup[3], y2)

        # crop to the bounding box
        bbox = utils.crop_to_bbox(image, (x1, y1, x2, y2), padding=(5, 24))
        found = True
    # just return the image as is if nothing was found
    else:
        bbox = image
        found = False

    return bbox, found


def is_text_black(image):
    """attempts to determine the color of the text on thresholded image.
    
    :param image: input thresholded image
    :type image: cv2 image
    """
    # binarise the image
    _, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    _, thresh_inv = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)

    total_px = thresh.size
    white_px = np.sum(thresh > 0)
    ratio = white_px / total_px

    inv_total_px = thresh_inv.size
    inv_white_px = np.sum(thresh_inv > 0)
    inv_ratio = inv_white_px / inv_total_px

    dif = inv_ratio - ratio

    text_color = 'WHITE' if dif > 0 else 'BLACK'
