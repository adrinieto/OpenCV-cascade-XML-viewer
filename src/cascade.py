#!/usr/bin/python

import xml.etree.ElementTree as ET
import sys
import cv, cv2

class Rect:
  
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
            sys.exit()

    def readNewStyle(self, cascadeNode):
        self._params = {}
        self._params['width'] = int(cascadeNode.find('width').text)
        self._params['height'] = int(cascadeNode.find('height').text)
        self._params['stageNum'] = int(cascadeNode.find('stageNum').text)
    
        #Getting all features 
        self._features = []
        feats = [feat for feat in cascadeNode.find('features')]
        for feat in feats:  
            rectList = []  
            for rect in feat.find('rects'):         
                values = [int(x.replace('.','')) for x in rect.text.split()]
                rect = Rect(values)
                rectList.append(rect)
            self._features.append(Feature(rectList))
            
        #Getting features for each stage
        self._stages = []
        stages = [stage for stage in cascadeNode.find('stages')]
        for stage in stages:
            classifiers = stage.find('weakClassifiers')
            features = []
            for cl in classifiers:
                featId = int(cl[0].text.split()[2])
                features.append(self._features[featId])
            self._stages.append(features)
        #print self._stages
        
    def readOldStyle(self, cascadeNode):
        size = cascadeNode.find('size').text.split()
        self._params = {}
        self._params['width'] = int(size[0])
        self._params['height'] = int(size[1])
        
        #Getting features for each stage
        self._features = []
        self._stages = []
        stages = [stage for stage in cascadeNode.find('stages')]
        for stage in stages:
            features = []
            for cl in stage.find('trees'):
                rectList = []  
                for rect in cl[0][0].find('rects'):  #_/feature/rects
                    values = [int(x.replace('.','')) for x in rect.text.split()]
                    rect = Rect(values)
                    rectList.append(rect)
                self._features.append(Feature(rectList))
                features.append(self._features[len(self._features)-1])
            self._stages.append(features)
            
        self._params['stageNum'] = len(self._stages)
        self._params['featuresNum'] = len(self._features)
    
    def readFile(self, cascadeFile):
        tree = ET.parse(cascadeFile)
        root = tree.getroot()    #<opencv_storage>
        cascade = root[0]        #<cascade_name> 
        if cascade.find('features') is None:
            self.readOldStyle(cascade)
        else:
            self.readNewStyle(cascade)

    def getFeatures(self):
        return self._features
        
    def getStages(self):
        return self._stages
        
    def getParams(self):
        return self._params
    
    def getImage(self):
        return self._img.copy()
    
        
        
