import cv2
import numpy as np
from matplotlib import pyplot as plt

cap = cv2.VideoCapture('noin.mov')
cv2.namedWindow("frame",cv2.WINDOW_NORMAL)
cv2.resizeWindow('frame', 800,800)


MIN_MATCH_COUNT = 10
sift=cv2.SIFT_create()
img1 = cv2.imread('noin.jpg',0)
kp1, des1 = sift.detectAndCompute(img1,None)

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm=FLANN_INDEX_KDTREE,tress = 5)
search_params = dict(checks=50)
flann = cv2.FlannBasedMatcher(index_params,search_params)


while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        img2 = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        kp2,des2 = sift.detectAndCompute(img2,None)
        matches = flann.knnMatch(des1,des2,k=2)
        good = []
        for m,n in matches:
            if m.distance < 0.2*n.distance:
                good.append(m)
        if len(good)>MIN_MATCH_COUNT:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1,1,2)
            dst_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1,1,2)
            M,mask = cv2.findHomography(src_pts,dst_pts,cv2.RANSAC,5.0)
            matchesMask = mask.ravel().tolist()
            h,w = img1.shape
            pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
            dst = cv2.perspectiveTransform(pts,M)
            img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)
        else:
            print("Not enough matches are found - %d/%d" %(len(good),MIN_MATCH_COUNT))
            matchesMask = None
        draw_params = dict(matchColor = (0,255,0), singlePointColor = None, matchesMask = matchesMask, flags = 2)
        img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
        cv2.imshow('frame', img3)

    else:
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

