#!/usr/bin/python
import xml.etree.ElementTree as ET
import cv
import cv2

def getParams(cascade):
    params = {}
    params['width'] = cascade.find('width').text
    params['height'] = cascade.find('height').text
    params['stageNum'] = cascade.find('stageNum').text
    return params
    
def getFeatures(cascade):
    features = []
    feats = [feat for feat in cascade.find('features')]
    for idfeat, feat in enumerate(feats):  
        #print ">Feature",idfeat   
        rectList = []  
        for idrect, rect in enumerate(feat.find('rects')):         
            values = [int(x.replace('.','')) for x in rect.text.split()]
            rect = {}
            rect['x'] = values[0]
            rect['y'] = values[1]
            rect['width'] = values[2]
            rect['height'] = values[3]
            rect['weight'] = values[4]
            rectList.append(rect)
            #print idrect, rect
        features.append(rectList)
    return features
    
def drawFeature(feat):
    img = cv2.imread("data/logo_citius_crop.jpg")
    for rect in feat:
        color = (255,255,255) if (rect['weight'] > 0) else (0,0,0)
        cv2.rectangle(img, (rect['x'],rect['y']), (rect['x'] + rect['width'],rect['y'] + rect['height']), color, cv.CV_FILLED)
    cv2.imshow("Imagen original", img)
    cv2.waitKey()

def main():

    tree = ET.parse('data/cascade.xml')
    root = tree.getroot()    #<opencv_storage>
    cascade = root[0]        #<cascade_name> 

    params = getParams(cascade)
    features = getFeatures(cascade)

    drawFeature(features[1])
    #for idx, stage in enumerate(cascade.find('stages')):
        #print idx, stage.tag

    #opencv()

if  __name__ =='__main__':
    main()

