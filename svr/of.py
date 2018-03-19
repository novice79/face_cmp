#!/usr/bin/env python

import time

start = time.time()

import cv2
import StringIO
import urllib
import base64
import os
from PIL import Image
import numpy as np
np.set_printoptions(precision=2)
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

import openface
curDir = os.path.dirname(os.path.realpath(__file__))
fileDir = '/root/openface'
modelDir = os.path.join(fileDir, 'models')
dlibModelDir = os.path.join(modelDir, 'dlib')
openfaceModelDir = os.path.join(modelDir, 'openface')

dlibFacePredictor = os.path.join(dlibModelDir, "shape_predictor_68_face_landmarks.dat")
networkModel = os.path.join(openfaceModelDir, 'nn4.small2.v1.t7')
imgDim = 96
verbose = False #True

if verbose:
    print("Argument parsing and loading libraries took {} seconds.".format(
        time.time() - start))

start = time.time()
align = openface.AlignDlib(dlibFacePredictor)
net = openface.TorchNeuralNet(networkModel, imgDim)
if verbose:
    print("Loading the dlib and OpenFace models took {} seconds.".format(
        time.time() - start))

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
    plt.figure()
    plt.imshow(img)
    plt.xticks([])
    plt.yticks([])

    imgdata = StringIO.StringIO()
    plt.savefig(imgdata, format='png')
    imgdata.seek(0)
    content = 'data:image/png;base64,' + \
        urllib.quote(base64.b64encode(imgdata.buf))
    plt.close()
    return content

def getRep(img):
    rgbImg = cvMatFromRaw(img['data'], img['w'], img['h'])    
    
    if verbose:
        print("  + Original size: {}".format(rgbImg.shape))

    start = time.time()
    bb = align.getLargestFaceBoundingBox(rgbImg)
    if bb is None:
        raise Exception("Unable to find a face: {}".format( img['name'] ))
    if verbose:
        print("  + Face detection took {} seconds.".format(time.time() - start))
        
    start = time.time()
    alignedFace = align.align(imgDim, rgbImg, bb,
                              landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
    if alignedFace is None:
        raise Exception("Unable to align image: {}".format( img['name'] ))
    if verbose:
        print("  + Face alignment took {} seconds.".format(time.time() - start))

    start = time.time()
    rep = net.forward(alignedFace)
    if verbose:
        print("  + OpenFace forward pass took {} seconds.".format(time.time() - start))
        print("Representation:")
        print(rep)
        print("-----\n")
    # annotate ################################
    rectangle_face(rgbImg, bb)
    landmark_face(rgbImg, bb)    
    if img['name'] is not None:
        ip = os.path.join(curDir, 'static', img['name'])
        print("write image file to {} ".format(ip))
        cv2.imwrite( ip, rgbImg)
    ############################################    
    return rep

def cmp_imgs(img1, img2):
    d = getRep(img1) - getRep(img2)
    dis = np.dot(d, d)
    print("  + Squared l2 distance between representations: {:0.3f}".format(dis))
    return dis 
