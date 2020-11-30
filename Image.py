import numpy as np
from cv2 import cv2



class Image:
    def __init__(self,image):
        self.image=image.copy()
        self.gray=self.toGray()
        self.smoothed=self.smoothing()
        self.threshold,self.binary=self.binarizationInverse()
        self.contours=self.findContours()
        self.contured=image.copy()
        self.binary_text=np.copy(self.binary)
        self.binary_non_text = np.copy(self.binary)



    def toGray(self):
        return cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
    def getGray(self):
        return self.gray

    def smoothing(self):
        kernel3 = np.ones((3, 3), np.float32) / 9
        return cv2.filter2D(self.getGray(), -1, kernel3)
    def getSmoothed(self):
        return self.smoothed

    def binarizationInverse(self):
        ret, thresh= cv2.threshold(self.getSmoothed(), 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        if (ret < 100):
            # ret, thresh = cv2.threshold(self.getSmoothed(), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            thresh=cv2.bitwise_not(thresh)
        return ret,thresh
    def getBinary(self):
        return self.binary
    def getThresh(self):
        return self.threshold


    def getContured(self):
        return self.contured
    

    def findContours(self):
        (contours, _) = cv2.findContours(self.getBinary(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        return contours
    def getContours(self):
        return self.contours
