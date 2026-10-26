import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# probably stupid? idk it makes my brain less hurt
def line_func(func_slope,func_x,func_b):
    ret = func_slope*func_x+func_b
    return ret

img  = cv.imread('img/leds_near.png', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"
img_width = np.shape(img)[1]
img_height = np.shape(img)[0]

params = cv.SimpleBlobDetector.Params()

# set to detect light blobs
params.blobColor = 255

# Thresholds for binarization
params.minThreshold = 10
params.maxThreshold = 200

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

# detect blobs
keypoints = detector.detect(img)

# Draw blobs as red circles
output = cv.drawKeypoints(img, keypoints, np.array([]), (0, 0, 255),
                           cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# cv KeyPoints are of their own format, need this for numpy
points = cv.KeyPoint.convert(keypoints)
# futhermore doing a point set hough transform line fitting needs an extra dimension for possible channels
points =  points[:, np.newaxis, :]

print("KEYPOINTS be like:---------------")
print(type(points), type(points[0][0][0]))
print(points[0], np.shape(points))
print("---------------------------------")

# returns an array of 3d vectors (votes, rho, theta) that describe lines
lines_polar = cv.HoughLinesPointSet(
    point=points,
    lines_max=20,
    threshold=1,
    min_rho=0,
    max_rho=img_height,
    rho_step=1,
    min_theta=0,
    max_theta=np.pi/2,
    theta_step=np.pi/360
)

print("LINES BE LIKE:-------------------")
print(type(lines_polar), type(lines_polar[0][0]))
print(lines_polar[0],np.shape(lines_polar))
print("---------------------------------")

for i in range(len(lines_polar)):
    votes = lines_polar[i][0]
    rho = lines_polar[i][1]
    theta = lines_polar[i][2]

    # start with getting a point on the line, x0 = rho*cos(theta), y0 = rho*sin(theta)
    x0 = rho*np.cos(theta)
    y0 = rho*np.sin(theta)

    # y-intercept is found at y1-m*x1 (b = y-mx)
    # slope is simply -1/tan(theta)
    if np.tan(theta) == 0:
        slope = 0   # hackerman way of avoiding dividing by zero
    elif theta == np.pi/2:
        slope = 100**100 # avoid undefined with arbitrarily large slope, sign doesnt matter
    else:
        slope = -1/np.tan(theta)
    y_intercept = y0-slope*x0

    #draw lines
    x1 = -img_width
    y1 = line_func(slope,x1,y_intercept)
    pt1 = (int(x1),int(y1))
    x2 = img_width
    y2 = line_func(slope,x2,y_intercept)
    pt2 = (int(x2),int(y2))

    cv.line(output,pt1,pt2,(0,255,0),1)


cv.imshow("blobs detected",output)
cv.waitKey(0)
cv.destroyAllWindows()
