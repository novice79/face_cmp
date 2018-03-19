#!/usr/bin/env python

import time

import cv2
import StringIO
import urllib
import base64
import os
from PIL import Image
import numpy as np
np.set_printoptions(precision=2)


start = time.time()


def cvMatFromDataUrl(dataURL, w, h):
    head = "data:image/png;base64,"
    assert(dataURL.startswith(head))
    imgdata = base64.b64decode(dataURL[len(head):])
    return cvMatFromRaw(imgdata, w, h)
def cvMatFromRaw(imgdata, w, h):
    imgF = StringIO.StringIO()
    imgF.write(imgdata)
    imgF.seek(0)
    img = Image.open(imgF)

    buf = np.asarray(img)
    bgrImg = np.zeros((h, w, 3), dtype=np.uint8)
    bgrImg[:, :, 0] = buf[:, :, 0]
    bgrImg[:, :, 1] = buf[:, :, 1]
    bgrImg[:, :, 2] = buf[:, :, 2]
    rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)
    # these for flip img
    # buf = np.fliplr(np.asarray(img))
    # rgbImg = np.zeros((h, w, 3), dtype=np.uint8)
    # rgbImg[:, :, 0] = buf[:, :, 2]
    # rgbImg[:, :, 1] = buf[:, :, 1]
    # rgbImg[:, :, 2] = buf[:, :, 0]
    return rgbImg
def landmark_face(rgbImg, bb = None):
    # myVariable = testVariable if bool(testVariable) else somethingElse
    if bb is None:
        bb = align.getLargestFaceBoundingBox(rgbImg)
    if bb is None:
        return    
    landmarks = align.findLandmarks(rgbImg, bb)
    # for p in openface.AlignDlib.OUTER_EYES_AND_NOSE:
    for p in landmarks:
        cv2.circle(rgbImg, center=p, radius=3,
                    color=(102, 204, 255), thickness=-1)
    return rgbImg, bb                
def rectangle_face(rgbImg, bb = None):
    if bb is None:
        bb = align.getLargestFaceBoundingBox(rgbImg)
    if bb is None:
        return     
    bl = (bb.left(), bb.bottom())
    tr = (bb.right(), bb.top())
    cv2.rectangle(rgbImg, bl, tr, color=(153, 255, 204), thickness=3)
    return rgbImg, bb
def cvMat2Raw(img):
    pass
def cvMat2DataUrl(img):
    ret, buf = cv2.imencode('.png', img)
    # imgdata = StringIO.StringIO(img_str)
    content = 'data:image/png;base64,' + \
        urllib.quote(base64.b64encode(np.array(buf)))
    return content

def url_to_image(url):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
	resp = urllib.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)

	# return the image
	return image
def cmp_imgs(img1, img2):

    pass
