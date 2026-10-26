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

# testing using contours of blobs
params.collectContours = True

img  = cv.imread('img/leds_far.png', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"

detector = cv.SimpleBlobDetector.create(params)

# try adding thresholding pre detections; getBlobContours returns all contours regardless of params?
# this seems a little doomed. Early testing showed ok results with naive thresholding on 127 cutoff
# binarizing image that way seems not smart though

#blur = cv.GaussianBlur(img,(5,5),0)
#ret_otsu, img_otsu = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

#plt.plot()
#plt.imshow(img_otsu)
#plt.show()

# detect blobs
keypoints = detector.detect(img)
# returns a tuple
conts = detector.getBlobContours()
print("conts type:",type(conts))
print("conts[0]:",type(conts[0])," conts[1]:",type(conts[1]))
print("shape 0:", np.shape(conts[0])," shape 1:",np.shape(conts[1]))

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
#cv.line(output,pt1,pt2,(0,255,0),2)

# testing contours
cv.drawContours(output,conts,-1, (0,255,0), 1)

mask = np.zeros(img.shape,np.uint8)
cv.drawContours(mask,conts,-1,255,thickness=cv.FILLED)

# need to experiment or just figure out what sort of kernel to use. kernel dimensions should be dynamic?
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(10,8))

mask = cv.morphologyEx(mask,cv.MORPH_OPEN,kernel)

cv.imshow("mask",mask)

img_height, img_width = mask.shape
pixelpoints = cv.findNonZero(mask)
pixelpoints = pixelpoints[:,np.newaxis,:]

# returns an array of 3d vectors (votes, rho, theta) that describe lines
lines_polar = cv.HoughLinesPointSet(
    point=pixelpoints,
    lines_max=20,
    threshold=70,
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