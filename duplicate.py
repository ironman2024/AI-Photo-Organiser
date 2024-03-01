from imutils import paths
import numpy as np
import argparse
import cv2
import os

def dhash(image,hashSize=8):
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    resized= cv2.resize(gray,(hashSize+1,hashSize))
    diff =resized[:,1:]>resized[:,:-1]
    return sum([2 **i for (i,v) in enumerate(diff.flatten()) if v])
