import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# probably stupid? idk it works
def line_func(func_slope,func_x,func_b):
    ret = func_slope*func_x+func_b
    return ret

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

img  = cv.imread('img/leds_near.png', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"

# detect blobs
keypoints = detector.detect(img)

# Draw blobs as red circles
output = cv.drawKeypoints(img, keypoints, np.array([]), (0, 0, 255),
                           cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# cv KeyPoints are of their own format, need this for numpy
points = cv.KeyPoint.convert(keypoints)
fit_line = cv.fitLine(points , cv.DIST_L2 , 0 , 0.01 , 0.01)

# fit_line is in 4D vector with shape (4,1) because of channels in MAT types etc etc 
# important part is that the 4 rows are values for (vx,vy,x0,y0), where vx,vy define a normalized vector (i.e. length = 1)
# that is colinear to found line, and x0,y0 is a point on that line.
# So we basically know the slope (and if it's pos or neg) and a point on the line.

# we get slope with vy/vx, high level maths
slope = fit_line[1][0] / fit_line[0][0]
# given point on line
p0 = (fit_line[2][0],fit_line[3][0])

# line is y = mx + b meaning for point x1,y1, y-intercept is found at y1-m*x1 (b = y-mx)
intercept_y = fit_line[3][0] - slope * fit_line[2][0]

img_dim = np.shape(img)

x1 = -img_dim[1]
y1 = line_func(slope,x1,intercept_y)
pt1 = (int(x1),int(y1))
x2 = img_dim[1]
y2 = line_func(slope,x2,intercept_y)
pt2 = (int(x2),int(y2))

# this was unsurprisingly not amazing since the line detected is based on all lines. Still works on some lvl
cv.line(output,pt1,pt2,(0,255,0),2)

cv.imshow("blobs detected",output)
cv.waitKey(0)
cv.destroyAllWindows()

