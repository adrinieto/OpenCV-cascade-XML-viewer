#!/usr/bin/python
import sys
import xml.etree.ElementTree as ET
import cv,cv2
import math
import numpy as np
from cascade import Rect, Feature, Cascade

def main():
    if len(sys.argv) != 3:
        print "Usage: python lector.py <cascade.xml> <img>"
        sys.exit(-1)
    #Reading arguments
    cascadeFile = sys.argv[1]
    imgFile = sys.argv[2]
    
    cascade = Cascade(cascadeFile, imgFile)
    params = cascade.getParams()
    
    #Features by stage
    for stageId, stage in enumerate(cascade.getStages()):
        print "<- Stage {} ({} weak classifiers) ->".format(stageId,len(stage))
        #print params['height']*(len(stage)+1)/2
        featuresPerRow = int(math.sqrt(len(stage)))
        height = params['height'] * ((len(stage) + (featuresPerRow - 1)) / featuresPerRow)
        width = params['width'] * featuresPerRow
        allFeatures = np.zeros((height,width,3), np.uint8)
        for idf,feat in enumerate(stage):
            img = cascade.getImage()
            feat.draw(img)
            yStart = params['height'] * (idf / featuresPerRow)
            yEnd = yStart + img.shape[0]
            xStart = params['width'] * (idf % featuresPerRow)
            xEnd = xStart + img.shape[1]
            allFeatures[yStart : yEnd, xStart : xEnd] = img
            #cv2.imshow("Stage {}".format(stageId), img)
            #cv2.waitKey()
        cv2.namedWindow("allFeat stage {}".format(stageId),cv.CV_WINDOW_NORMAL)
        cv2.imshow("allFeat stage {}".format(stageId),allFeatures)
        cv2.waitKey()
    
    sys.exit()
    #All features
    for feat in cascade.getFeatures():
        img = cascade.getImage()
        feat.draw(img)
        cv2.imshow("Imagen original", img)
        cv2.waitKey()
        
if  __name__ =='__main__':
    main()
    
