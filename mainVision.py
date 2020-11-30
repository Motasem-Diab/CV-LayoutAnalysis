import os
import statistics
import numpy as np
import cv2
from ConnectedComponent import ConnectedComponent
from Image import Image
from Line import Line, tmpLine


def heuristicFilter(listOfCC):
    listOfText = []
    listOfNonText = []
    for cc in listOfCC:
        if (cc.area < T_area):
            listOfNonText.append(cc)
            continue
        elif (cc.dens < T_dens):
            listOfNonText.append(cc)
            continue
        elif ((cc.ratio < T_ratio)):  # and H < W removed
            listOfNonText.append(cc)
            continue
        elif (len(cc.inside) > T_ins):
            listOfNonText.append(cc)
            continue
        listOfText.append(cc)
    return listOfText, listOfNonText


def linesNoiseFilter(listOfLines):
    listOfLinesNoNoise = []
    for line in listOfLines:
        # histo = np.sum(line.line,axis=1,keepdims=True)/255
        # print(histo[2])
        # if(line.Xmin < 50 and 1500<line.Ymin<1600  ):
        #     print()
        if (line.dens > L_den):
            continue
        if (line.size < 500):
            continue
        listOfLinesNoNoise.append(line)
    return listOfLinesNoNoise


def mergeWords(listOfLines):
    diffThresh = 30  # pixels
    listOfMerged = []
    for line in listOfLines:
        X, Y, W, H = line.getDimentions()
        Xmax = X + W
        Ymax = Y + H
        if (line.merged == False):
            for mayMerge in listOfLines:
                if (abs(mayMerge.Xmin - (line.Xmin + line.W)) > 20):
                    continue
                if (mayMerge.Xmin < line.Xmin):  # (line.Xmin - mayMerge.Xmin) > 2
                    continue
                if (mayMerge.Ymin >= (Y - diffThresh) and mayMerge.Ymin <= Y + diffThresh):
                    mayMerge.merged = True
                    X = min(X, mayMerge.Xmin)
                    Y = min(Y, mayMerge.Ymin)
                    Xmax = max(Xmax, mayMerge.Xmin + mayMerge.W)
                    Ymax = max(Ymax, mayMerge.Ymin + mayMerge.H)
            listOfMerged.append(tmpLine(X, Y, Xmax, Ymax))
    return listOfMerged


def filterNonText(list):
    newList = []
    for objjj in list:
        if objjj.size < 2000000:
            continue
        newList.append(objjj)
    # for part1 in newList:
    #     if(part1.Xmin<250):
    #         print()
    #     for part2 in newList:
    #         if isInside(part1, part2):
    #             newList.remove(part2)
    # return newList


def isInside(cc1, cc2):
    if cc2.Xmin > cc1.Xmin and cc2.Xmax < cc1.Xmax and cc2.Ymax < cc1.Ymax:
        return True



mypath = os.getcwd()
readingPath = os.path.join(mypath, "input/")
writingPath = os.path.join(mypath, "output/")
os.chdir(readingPath)
arr = os.listdir()
#arr2=["input220.jpg","input243.jpg","input245.jpg","input261.jpg","input297.jpg","input312.jpg","input397.jpg","input13.jpg","input32.jpg"]
arr2=["input15.jpg"]
arr.remove(".DS_Store")

levelOfMergingWords = 0
T_area = 6
T_dens = 0.15  # .06
T_ratio = 0.06  # .06
T_ins = 4
L_den = 0.4

for example in arr:

    img = cv2.imread(readingPath+example)

    image = Image(img)
    cv2.imwrite(writingPath + "Binary" + example, image.binary)
    # compute all CCs to determine its props
    listOfCC = []
    for cnt in image.getContours():
        listOfCC.append(ConnectedComponent(cnt, image.getContours()))

    # classify the contours to text and non-text
    listOfTextCC, listOfNonTextCC = heuristicFilter(listOfCC)

    # to make binary text
    nonTextCnts = []
    for cnt in listOfNonTextCC:
        nonTextCnts.append(cnt.CC)
    cv2.drawContours(image.binary_text, nonTextCnts, -1, (0, 0, 0), -1)
    # cv2.imwrite("output/partest/texitBinary"+str(number)+".jpg", image.binary_text)   # debugging purpose


    # making binary of non-text
    for cnt in listOfTextCC:
        x, y, w, h = cv2.boundingRect(cnt.CC)
        cv2.rectangle(image.binary_non_text, (x, y), (x + w, y + h), (0, 0, 0), thickness=-1)
    # cv2.imwrite("output/partest/texitNonBinary"+str(number)+".jpg", image.binary_non_text)    # debugging purpose
    ###############################################
    # work on non-text
    kernel = np.ones((6, 6), 'uint8')
    image.binary_non_text = cv2.morphologyEx(image.binary_non_text, cv2.MORPH_OPEN, kernel)  # noise removing (salt noise)
    kernel = np.ones((9, 13), 'uint8')
    image.binary_non_text = cv2.dilate(image.binary_non_text, kernel, iterations=3)  # noise filling
    # cv2.imwrite("output/partest/NonTextBinary"+str(number)+".jpg", image.binary_non_text)


    ######### improving on non text

    (contours, _) = cv2.findContours(image.binary_non_text, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    listOfNonTextCC = []
    for cnt in contours:
        listOfNonTextCC.append(Line(cnt))

    # listOfNonTextCC = filterNonText(listOfNonTextCC)


    kernel = np.ones((2, 9), 'uint8')
    di = cv2.dilate(image.binary_text, kernel, iterations=3)
    (contours, _) = cv2.findContours(di, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # make a list of lines
    listOfLines = []
    for cnt in contours:
        listOfLines.append(Line(cnt))

    listOfLines = linesNoiseFilter(listOfLines)

    # ysort
    print(len(listOfLines))
    listOfLines = sorted(listOfLines, key=lambda lin: (lin.Ymin, lin.Xmin))

    # # print list of lines sorted ( debugging )
    # for i, line in enumerate(listOfLines):
    #     if 320 < line.Ymin < 350:
    #         print(i)

    for i in range(0, levelOfMergingWords):
        listOfLines = mergeWords(listOfLines)

    ###### FINISH lines

    heights = []  # for future work like the average heights
    Ys = []
    for line in listOfLines:
        x, y, w, h = line.getDimentions()
        heights.append(h)
        Ys.append(y)
        cv2.rectangle(image.binary_text, (x - 1, y - 5), (x + w, y + h), (255, 255, 255), -1)

    kernel = np.ones((9, 1), 'uint8')
    di = cv2.dilate(image.binary_text, kernel, iterations=3)
    (contours, _) = cv2.findContours(di, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(image.binary_text, contours, -1, (255, 255, 255), -1)
    (contours, _) = cv2.findContours(image.binary_text, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # cv2.imwrite("output/partest/outputTextCon" + str(number) + ".jpg", image.binary_text)

    cont = []
    conNoise = []
    for cnt in contours:
        if cv2.contourArea(cnt) > 10000:
            cont.append(cnt)
        else:
            conNoise.append(cnt)
    cv2.drawContours(image.binary_text, conNoise, -1, (0, 0, 0), -1)
    cv2.drawContours(image.contured, cont, -1, (0, 255, 0), 3)
    # cv2.imwrite("output/partest/outputTextCon" + str(number) + ".jpg", image.contured)

    # drawing non-text
    contours = []
    for cnt in listOfNonTextCC:
        if cnt.size > 30000:
            contours.append(cnt.line)
    cv2.drawContours(image.contured, contours, -1, (0, 0, 255), 2)

    # # drawing non-text as rectangle
    # for cnt in listOfNonTextCC:
    #     x, y, w, h = cnt.getDimentions()
    #     cv2.rectangle(image.contured, (x - 1, y - 5), (x + w, y + h), (0,0,255), 3)
    # cv2.imwrite("output/partest/outputBinary" + str(number) + ".jpg", image.getContured())
    cv2.imwrite(writingPath+"OutPut"+example, image.getContured())
    print(example + " finished")
    # ########################################### TO HERE ##########################################################################
    #
    # ########################################### FUTURE WORK ##########################################################################
    # # # cv2.imwrite("output/partest/outputText" + str(number) + ".jpg", image.binary_text)
    # # # print(statistics.median(heights))
    # # print(min(Ys))
    # # median = int(statistics.median(heights) / 2)
    # # for i in range(0, int(img.shape[0]/median)):
    # #     imageTest = cv2.line(image.binary_text, (0, i*median), (img.shape[1], i*median), (0, 0, 0), 1)
    # # cv2.imwrite("output/partest/outputLines" + str(number) + ".jpg", imageTest)
    # # (contours, _) = cv2.findContours(imageTest, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # # # cv2.drawContours(image.contured, contours, -1, (0, 0, 255), 1)
    # # # cv2.imwrite("output/partest/outputBinary" + str(number) + ".jpg", image.getContured())
    # # newLines = []
    # # for cnt in contours:
    # #     newLines.append(Line(cnt))
    # #
    # # for i, line1 in enumerate(newLines):
    # #     diff=int(line1.W/4)
    # #     if(line1.merged == True):
    # #         continue
    # #     for j, line2 in enumerate(newLines):
    # #         if (abs(line1.Xmin - line2.Xmin) > diff):
    # #             continue
    #
    #
    #
    #
    #
    #
