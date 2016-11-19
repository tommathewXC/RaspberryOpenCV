from picamera.array import PiRGBArray
from picamera import PiCamera
import picamera
import time
import cv2
import numpy as np

class VideoCaptureFilter:
  def laplacianFilter(arr):
    return cv2.Laplacian(arr, cv2.CV_64F);

  def getAdaptiveThresh(arr):
    return cv2.adaptiveThreshold(arr, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2);

  def subtractBackground(arr):
    bgs = cv2.createBackgroundSubtractorMOG2()
    return bgs.apply(arr)

  def gaussianBlur(arr):
    return cv2.GaussianBlur(arr, (5,5), 0)

  def getContour(arr):
    a = cv2.findContours(arr, cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)
    cnt = a[0]
    (x,y),r = cv2.minEnclosingCircle(cnt)
    cent = (int(x), int(y))
    radi = int(r)
    cv2.circle(arr, cent, radi, (0,255,0),2)
    return arr
