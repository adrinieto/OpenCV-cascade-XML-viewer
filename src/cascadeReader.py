#!/usr/bin/python
import sys
import xml.etree.ElementTree as ET
import cv,cv2
from cascade import Rect, Feature, Cascade

def main():
    if len(sys.argv) != 3:
        print "Usage: python lector.py <cascade.xml> <img>"
        sys.exit(-1)
    #Reading arguments
    cascadeFile = sys.argv[1]
    imgFile = sys.argv[2]
    
    cascade = Cascade(cascadeFile, imgFile)
    
    for stageId, stage in enumerate(cascade.getStages()):
        print "<- Stage {} ->".format(stageId)
        for feat in stage:
            img = cascade.getImage()
            feat.draw(img)
            cv2.imshow("Stage {}".format(stageId), img)
            cv2.waitKey()
    
    sys.exit()
    for feat in cascade.getFeatures():
        img = cascade.getImage()
        feat.draw(img)
        cv2.imshow("Imagen original", img)
        cv2.waitKey()
        
if  __name__ =='__main__':
    main()
    
