import numpy as np
import cv2
from matplotlib import pyplot as plt

sift = cv2.xfeatures2d.SIFT_create()
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)
flann = cv2.FlannBasedMatcher(index_params, search_params)

def getSIFTdes(filename):
    img = cv2.imread(filename,0)
    des = sift.detectAndCompute(img,None)[1]
    return des

def findhouse(peyzajename, houselist):
    rez = {}
    peyzajdes = getSIFTdes(peyzajename)
    for housefile, housetype in houselist:
        des1 = getSIFTdes(housefile)
        matches = flann.knnMatch(des1,peyzajdes,k=2)
        good = 0
        for m,n in matches:
            if m.distance < 0.7*n.distance:
                good += 1
        try:
            if rez[housetype] < good:
                rez[housetype] = good
        except KeyError:
            rez[housetype] = good
    if len([ rez[_] for _ in rez if rez[_] > 10 ]) == 0:
        return 'неизвестный'
    maxht = max([ rez[_] for _ in rez ])
    for htype in rez:
        if rez[htype] == maxht:
            return htype


if __name__ == '__main__':
    import sys
    house = findhouse(sys.argv[1],
        [
            ('house0.png', 'городской'),
            ('house1.png', 'городской'),
            ('house2.png', 'деревенский'),
            ('house3.png', 'деревенский')
        ])
    if house == 'деревенский':
        print('пейзаж - деревня')
    elif house == 'городской':
        print('пейзаж - город')
    else:
        print('неизвестный пейзаж')
