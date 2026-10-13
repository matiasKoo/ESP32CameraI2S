import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

params = cv.SimpleBlobDetector.Params()

# set to detect light blobs
params.blobColor = 255

# Thresholds for binarization
#params.minThreshold = 0 
params.minThreshold = 10
#params.minThreshold = 2 
params.maxThreshold = 200
#params.thresholdStep = 1

# Filter by Area
params.filterByArea = True
params.minArea = 10

# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.75 #0.1

# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.87

# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.4 #0.01

detector = cv.SimpleBlobDetector.create(params)

img = cv.imread('testikuva1.jpg')
img_gray = cv.imread('testikuva1.jpg', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"

# detect blobs
keypoints = detector.detect(img)

# Draw blobs as red circles
output = cv.drawKeypoints(img, keypoints, np.array([]), (0, 0, 255),
                           cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv.imshow("blobs detected",output)
cv.waitKey(0)
cv.destroyAllWindows()


#plt.plot()
#plt.imshow(img_gray)
#plt.show()