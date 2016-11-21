from picamera.array import PiRGBArray
from picamera import PiCamera
import picamera
import time
import cv2
import numpy as np
import VideoCaptureFilter as VCF

class VideoCapturer:
  multiplier = int()
  height = int()
  width = int()
  camera = object()
  filename = str()
  rawCapture = object()
  fifoFilters = []
  snapRate = 20
  
  def __init__(self, _height, _width, mult, frame_rate):
    self.multiplier = mult
    self.height = int( mult* _height)
    self.width = int( mult* _width);
    self.camera = PiCamera()
    self.camera.resolution = (self.height, self.width)
    self.camera.framerate = frame_rate
    self.rawCapture = PiRGBArray(self.camera, size=(self.height, self.width))
    time.sleep(0.1)
    self.filename = "temp.mp4"

  def runCam(self, loadFilters = False):
    count = 0
    prev = float()
    for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
      image = frame.array
      image = self.rotateImage(image, 270)      
      b, g, r = cv2.split(image)
      if loadFilters:
        for funct in self.fifoFilters:
          b = funct(b)
      else:
          b = image
      count= count + 1
      if count > 0:
        b = 0.5 * (b + prev)
      prev = b
      cv2.imshow("Frame", b)
      if (count > 0 and count % self.snapRate == 0):
        cv2.imwrite(str(count) + ".png", b)
      
      key = cv2.waitKey(1) & 0xFF
      self.rawCapture.truncate(0)
      if key == "ord":
        break;
    self.camera.close();
    cv2.destroyAllWindows()

  # works for single channel only
  def addFilter(self, newFilterFunction):
    self.fifoFilters.append(newFilterFunction)

  def rotateImage(self, arr, angle):
    if angle > 89:
      arr = np.rot90(arr)
    if angle > 179:
      arr = np.rot90(arr)
    if angle > 269:
      arr = np.rot90(arr)
    return arr
      

   
VCAP = VideoCapturer(1000, 1000, 0.5, 32)

VCAP.addFilter(VCF.VideoCaptureFilter.subtractBackground)
VCAP.addFilter(VCF.VideoCaptureFilter.laplacianFilter)
VCAP.runCam(True)
