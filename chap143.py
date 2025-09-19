import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('dsu1.jpg')
rows,cols,ch = img.shape
pts1 = np.float32([[324,280],[760,310],[765,507],[325,530]])
pts2 = np.float32([[0,0],[2000,0],[2000,1000],[0,1000]])
M = cv2.getPerspectiveTransform(pts1,pts2)
print(M)
dst = cv2.warpPerspective(img,M,(2000,1000))
plt.subplot(121),plt.imshow(img),plt.title('Input')
plt.subplot(122),plt.imshow(dst),plt.title('Output')
plt.show()