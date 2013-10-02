#!/usr/bin/python

import xml.etree.ElementTree as ET
import sys
import cv,cv2

class Rect:

    def __init__(self, x, y, width, height, weight):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._weight = weight
        
    def __init__(self, values):
        self._x = values[0]
        self._y = values[1]
        self._width = values[2]
        self._height = values[3]
        self._weight = values[4]
        
    def draw(self, img):
        color = (245,245,245) if (self._weight > 0) else (10,10,10)
        cv2.rectangle(img, (self._x,self._y), (self._x + self._width - 1, self._y + self._height - 1), color, cv.CV_FILLED)
        
########################

class Feature:

    def __init__(self, rects):
        self._rects = rects
        
        
    def draw(self, img):
        for rect in self._rects:
            rect.draw(img)
            
########################

class Cascade:

    def __init__(self, cascadeFile, imgFile):
        self.readFile(cascadeFile)
        self.readImg(imgFile)
        
        
    def readImg(self, imgFile):
        self._img = cv2.imread(imgFile)  
        height, width, _ = self._img.shape
        if width != self._params['width'] or height != self._params['height']:
            print "Cascade and image dimensions are different"
            sys.exit(-1)
          
    def readFile(self, cascadeFile):
        tree = ET.parse(cascadeFile)
        #New version of cascade XML
        root = tree.getroot()    #<opencv_storage>
        cascade = root[0]        #<cascade_name> 

        self._params = {}
        self._params['width'] = int(cascade.find('width').text)
        self._params['height'] = int(cascade.find('height').text)
        self._params['stageNum'] = int(cascade.find('stageNum').text)

        #Getting all features 
        self._features = []
        feats = [feat for feat in cascade.find('features')]
        for feat in feats:  
            rectList = []  
            for rect in feat.find('rects'):         
                values = [int(x.replace('.','')) for x in rect.text.split()]
                rect = Rect(values)
                rectList.append(rect)
            self._features.append(Feature(rectList))
            
        #Getting features for each stage
        self._stages = []
        stages = [stage for stage in cascade.find('stages')]
        for stage in stages:
            classifiers = stage.find('weakClassifiers')
            features = []
            for cl in classifiers:
                featId = int(cl[0].text.split()[2])
                features.append(self._features[featId])
            self._stages.append(features)
        #print self._stages
            
    def getFeatures(self):
        return self._features
        
    def getStages(self):
        return self._stages
        
    def getParams(self):
    	return self._params
    	
    def getImage(self):
        return self._img.copy()
    
        
        
