import cv2
import numpy as np


class Line:
    def __init__(self, contour):
        self.line=contour
        self.Xmin, self.Ymin, self.W, self.H = cv2.boundingRect(contour)
        self.area = np.count_nonzero(contour)
        self.size = cv2.contourArea(contour)
        self.dens = self.calcDens()
        self.merged = False

    #return line as contour
    def getLine(self):
        return self.line

    def calcDens(self):
        if(self.size == 0):
            return 0
        return self.area / self.size

    def getDimentions(self):
        return self.Xmin, self.Ymin, self.W, self.H



class tmpLine:
    def __init__(self,x,y,Xmax,Ymax):
        self.Xmin = x
        self.Ymin = y
        self.W = Xmax-x
        self.H = Ymax-y
        self.merged=False

    def getDimentions(self):
        return self.Xmin, self.Ymin, self.W, self.H

class bar:
    def __init__(self,x,y,w):
        self.x=x
        self.y=y
        self.w=w
