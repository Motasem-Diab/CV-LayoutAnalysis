import cv2
import numpy as np


class ConnectedComponent:
    def __init__(self, CC, contours):  # CC=cnt
        self.CC = CC
        self.Xmin, self.Ymin, self.w, self.h = cv2.boundingRect(CC)
        self.Xmax=self.Xmin+self.w
        self.Ymax = self.Ymin + self.h
        self.area = np.count_nonzero(CC)
        self.size = cv2.contourArea(CC)
        self.dens = self.calcDens()
        self.ratio = self.calcRatio()
        self.inside = self.findInside(contours)



    def calcDens(self):
        if(self.size == 0):
            return 0
        return self.area / self.size

    def calcRatio(self):
        W = self.w
        H = self.h
        ratio = min(W, H) / max(W, H)
        return ratio

    # def findSameColumn(self, contours):
    #     same = []
    #     for cnt in contours:
    #         # if(self.CC  cnt):
    #         #     continue
    #         Xmin_j, Ymin_j, Xmax_j, Ymax_j = cv2.boundingRect(cnt)
    #         if ((max(self.Xmin, Xmin_j) - min(self.Xmax, Xmax_j)) < 0):
    #             same.append(cnt)
    #     return same
    #
    # def findSameRow(self, contours):
    #     same = []
    #     for cnt in contours:
    #         # if(self.CC != cnt):
    #         Xmin_j, Ymin_j, Xmax_j, Ymax_j = cv2.boundingRect(cnt)
    #         if ((max(self.Ymin, Ymin_j) - min(self.Ymax, Ymax_j)) < 0):
    #             same.append(cnt)
    #     return same

    def findInside(self,contours):
        inside=[]
        for cnt in contours:
            # if (self.CC != cnt):
            Xmin_j, Ymin_j, w_j, h_j = cv2.boundingRect(cnt)
            if( (self.Xmin<=Xmin_j) and (self.Xmax>=Xmin_j+w_j) and (self.Ymin<=Ymin_j) and (self.Ymax>=Ymin_j+h_j) ):
                inside.append(cnt)
        return inside

    def getDimentions(self):
        return self.Xmin, self.Ymin, self.w, self.h

    
    # def take_Xmin(cnt):
    #     return cv2.boundingRect(cnt)[0]

    # def findRN(self):
    #     RN = []
    #     sameRowCopy = self.sameRow.copy()
    #     sameRowCopy.sort(key=lambda cnt: cv2.boundingRect(cnt)[0])
    #     for sr in sameRowCopy:
    #         Xmin_j, Ymin_j, Xmax_j, Ymax_j = cv2.boundingRect(sr)
    #         if( (Xmin_j - self.Xmax) > 0 ):
    #             RN.append(sr)
    #     return RN
    #
    # def findLN(self):
    #     LN = []
    #     sameRowCopy = self.sameRow.copy()
    #     sameRowCopy.sort(key=lambda cnt: cv2.boundingRect(cnt)[2])
    #     for sr in sameRowCopy:
    #         Xmin_j, Ymin_j, Xmax_j, Ymax_j = cv2.boundingRect(sr)
    #         if( (self.Xmin - Xmax_j ) > 0 ):
    #             LN.append(sr)
    #     return LN
    #
    # def findRNN(self):
    #     if(len(self.RN) != 0):
    #         RNCopy = self.RN.copy()
    #         RNCopy.sort(key=lambda x: cv2.boundingRect(x)[0])
    #         return RNCopy[0]
    #     else:
    #         return -1
    #
    # def findLNN(self):
    #     if(len(self.LN) != 0):
    #         LNCopy = self.LN.copy()
    #         LNCopy.sort(key=lambda x: cv2.boundingRect(x)[2])
    #         return LNCopy[-1]
    #     else:
    #         return -1
