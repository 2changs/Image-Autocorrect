'''
COMMENTS + THINGS TO DO:
	-HORIZONTAL LINES DONT WORK!!KAJHFALKJDSHF
	-being to work on rectangles 
		+ find perimeter of image 
		+ do something with the perimeter
		+ how do we determine if is circle vs rectangle????/
		+ contour approximation!!!!!
		+ possibly redo lines 
'''


import sys
import cv2
import cv2.cv as cv
import numpy
import numpy as np
import math
from collections import Counter


# from scipy.cluster.vq import kmeans, whiten
# import json
# import cgi

# data = {
#     'foo': 'hello',
#     'bar': None
# }

# print json.dumps(data)

array = sys.argv[1]
size  = sys.argv[2]



def stringToArray(array):
	arr = []
	num = ""
	if array != "":
		for i in range(len(array)):
			#print array[i];
			if array[i]==',':
				intNum = int(float(num))
				arr.append(num)
				num = ""
			else:
				num+=array[i]
		intNum = int(float(num))
		arr.append(num)
	return arr			


def lineOfBestFit(array):
	count = len(array)
	sumX = 0
	sumY = 0
	sumXSquared = 0
	sumXY = 0
	
	for i in range(0, len(array), 2):
		x = int(array[i])
		y = int(array[i+1])
		sumX += int(x)
		sumY += int(y)
		sumXSquared += (x*x)
		sumXY += (x * y)
	
	xMean = sumX/count
	yMean = sumY/count
	slope = (sumXY - sumX * yMean) / (sumXSquared - sumX * xMean)
	yInt = yMean - slope * xMean
	
	#equation of line: y = slope * x + yInt
	
	newLine = []
	for i in range(0, len(array), 2):
		x = int(array[i])
		newLine.append(x)
		y = (slope * x) + yInt
		newLine.append(y)
	return newLine
	
	

def createImage(array, width, height):

	color = (0,0,0)
	size = 3
	img = np.zeros((height, width, 3), np.uint8)
	img[:] = (255,255,255)
	cv2.imwrite('ellipse.jpg', img)
	cv2.imwrite('rectangle.jpg', img)
	for n in range(0, len(array)-2, 2):
		x = array[n]
		y = array[n+1]
		nextX = array[n+2]
		nextY = array[n+3]

		img[y, x] = (0,0,0)
		cv2.line(img, (int(x),int(y)), (int(nextX),int(nextY)),(0,0,0),1) #USE LINES NOT CIRCLES

	cv2.imwrite('oldImage.jpg',img)


def detectShapes(array, width, height):
	#CHECK IF IT IS A LINE
	lines = detectLines()
	lineResults = detectLines2(lines, array, width, height)
	if(lineResults == "Not A Line"):				#if it's not a line
		detectOtherShapes(width,height)

	else:											#if it is a line
		drawDetectedLine(array, lineResults[0], lineResults[1], lineResults[2], lineResults[3], width, height)


def detectLines():
	img = cv2.imread('oldImage.jpg')
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray,50,150,apertureSize = 3)

	minLineLength = 50
	maxLineGap = 10

	lines = cv2.HoughLinesP(edges,1,np.pi/270,10,minLineLength,maxLineGap)	#probablistic hough lines: if lines is empty, use circle detection
	if (lines != None):
		for x1,y1,x2,y2 in lines[0]:
			cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
	else:
		img[:] = (0,255,255)

	cv2.imwrite('hough.jpg',img)
	return lines

def detectLines2(lines, array, width, height):												#second step: so is it really a line??									
	img = cv2.imread('oldImage.jpg')
	lineImg = np.zeros((width, height, 3), np.uint8)
	lineImg[:] = (255,255,255)
	b = getYIntercept(array)
	numLines = 0
	numVerticalLines = 0
	avgSlope = 0
	slopes = []
	for x1, y1, x2, y2 in lines[0]:
		if (x2-float(x1))!=0:
			slope =(y2 - y1)/(x2 - float(x1))
			slopes.append(slope)

			avgSlope = avgSlope + slope

			numLines +=1
		else:
			numVerticalLines +=1
	#print(slopes)

	firstPointX = int(array[0])
	lastPointX  = int(array[len(array)-2])
	firstPointY = int(array[1])
	lastPointY  = int(array[len(array)-1])
	if(numLines > numVerticalLines):
		avgSlope = avgSlope/numLines
		#print "numLines", numLines
		#print "avgSlope ", avgSlope

		sumDifferences = 0									#calculate standard deviation
		for i in slopes:
			sumDifferences+=pow(i-avgSlope, 2)
		standardDev = math.sqrt(sumDifferences/len(slopes))
		outliers = 0
		for slope in slopes:
			if slope > 0:
				if slope > standardDev+avgSlope: 
					outliers+=1
				elif slope < standardDev-avgSlope: 
					outliers+=1
			else:
				if abs(slope) > abs(standardDev-avgSlope):
					outliers+=1
				elif abs(slope) < abs(standardDev+avgSlope):
					outliers+=1

		if(outliers > len(slopes)/1.5):
			#print "not a line"
			return "Not A Line"

		firstPointY = int(avgSlope * firstPointX) + b
		lastPointY  = int(avgSlope * lastPointX) + b

	else:
		lastPointX  = firstPointX
	
	return firstPointX, firstPointY, lastPointX, lastPointY

	#return listOfSlopes[abs(listOfSlopes-np.mean(listOfSlopes)) < m*np.std(listOfSlopes)]



def drawDetectedLine(array, firstPointX, firstPointY, lastPointX, lastPointY, width, height):
	img = cv2.imread('oldImage.jpg')
	lineImg = np.zeros((width, height, 3), np.uint8)
	lineImg[:] = (255,255,255)

	firstPointX = int(firstPointX)
	firstPointY = int(firstPointY)
	lastPointX = int(lastPointX)
	lastPointY = int(lastPointY)

	originalY   = int(array[1])							#correct the shift
	yDifference = abs(originalY-firstPointY)
	if(firstPointY > originalY): 
		firstPointY = firstPointY - yDifference
		lastPointY  = lastPointY - yDifference
	else: 
		firstPointY = firstPointY + yDifference
		lastPointY  = lastPointY  + yDifference

	cv2.line(img, (firstPointX, firstPointY), (lastPointX, lastPointY), (0,255,0), 1)
	#cv2.line(lineImg, (firstPointX, firstPointY), (lastPointX, lastPointY), (0,0,0), 2)
	#cv2.imwrite('newImage.jpg', img)
	#cv2.imwrite('hough.jpg', lineImg)
	print "Line"
	print firstPointX, firstPointY, lastPointX, lastPointY


def getLineLength(lines):
	totalLineLength = 0;
	for i in range(0, len(lines[0])):
		line = lines[0][i]
		length = pow((pow((line[0]-line[2]),2) + pow((line[1]-line[3]),2)), 1/2)
		totalLineLength+=length

	return totalLineLength


def getYIntercept(array):
	count = len(array)
	sumX = 0
	sumY = 0
	sumXSquared = 0
	sumXY = 0
	
	for i in range(0, len(array), 2):
		x = int(array[i])
		y = int(array[i+1])
		sumX += int(x)
		sumY += int(y)
		sumXSquared += (x*x)
		sumXY += (x * y)
	
	xMean = sumX/count
	yMean = sumY/count
	slope = (sumXY - sumX * yMean) / (sumXSquared - sumX * xMean)
	yInt = (yMean - slope * xMean)
	return yInt
	
def drawLine(lines):
	img = cv2.imread('oldImage.jpg')
	firstX = lines[0]
	firstY = lines[1]
	lastX  = lines[len(lines)-2]
	lastY  = lines[len(lines)-1]

	cv2.line(img,(firstX,firstY),(lastX,lastY),(0,255,0),2)
	#cv2.imwrite('newImage.jpg',img)


def detectCircles():
    im = cv2.imread('oldImage.jpg')
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    imgray_Blur = cv2.GaussianBlur(imgray, (15,15), 0)
    thresh = cv2.adaptiveThreshold(imgray_Blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 1)
    kernel = np.ones((3,3), np.uint8)
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations = 4)
    cont_img = closing.copy()
    
    
    
    #ret, thresh = cv2.threshold(imgray, 127, 255, 0    
    contours, hierarcy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  

    for cnt in contours:
        area = cv2.contourArea(cnt)
        '''if area < 2000 or area > 4000:
            continue
            if len(cnt) < 5:
            continue
        '''
        ellipse = cv2.fitEllipse(cnt)		#returns array [(centerx, centery), (radiusx, radiusy), rotation]
        #cv2.ellipse(im, ellipse, (0,0,255), 2)

    centerx = ellipse[0][0]
    centery = ellipse[0][1]
    radiusx = ellipse[1][0]
    radiusy = ellipse[1][1]
    rotation = ellipse[2]

    print "Ellipse "
    print centerx, centery, radiusx, radiusy, rotation


    #cv2.imwrite("hough.jpg", im)


#time for da polygons
def detectPerimeter(height, width):
	h = height
	w = width
	# im = cv2.imread('oldImage.jpg', 0)
	# ret, thresh = cv2.threshold(img, 127, 255, 0)
	# contours, hierarchy = cv2.findContours(thresh, 1, 2)

	# cnt = contours[0]
	# M = cv2.moments(cnt)
	# #print M

	# cx = int(M['m10']/M['m00'])
	# cy = int(M['m01']/M['m00'])
	# area = cv2.contourArea(cnt)
	# perimeter = cv2.arcLength(cnt,True)
	# epsilon = 0.1*cv2.arcLength(cnt,True)
	# approx = cv2.approxPolyDP(cnt,epsilon,True)

	# print "detect perimeter"
	im = cv2.imread('oldImage.jpg')
	invertColors(im)
	im = cv2.imread('oldImage.jpg')
	imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(imgray,127,255,0)
	contours, hierarcy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	
	# listOfFiles = ['newImage1.jpg', 'newImage2.jpg', 'newImage3.jpg', 'newImage4.jpg', 'newImage5.jpg']
	# for n in range(0,4):
	img = cv2.drawContours(im, contours, 0, (0,255,0), 1)

	cv2.imwrite('newImage.jpg', im)
	detectCorners(h, w)
	#print("draw new image")



def invertColors(im):
    im = (255-im)
    cv2.imwrite("oldImage.jpg", im)


def detectCorners(height, width, numCorners):

	img = cv2.imread('oldImage.jpg')
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	gray = np.float32(gray)
	dst = cv2.cornerHarris(gray,2,3,0.1)
	dst = cv2.dilate(dst,None)

	img[dst>0.10*dst.max()] = [255,0,255]
	cornersBool = dst>0.05*dst.max()
	cornersPerRow = []
  	for h in range(len(cornersBool)):
  		if [(h,i) for i,val in enumerate(cornersBool[h]) if val==(True)] != []:
  			cornersPerRow.append([[i, h] for i,val in enumerate(cornersBool[h]) if val==(True)])

  	corners = []
  	for i in cornersPerRow:
  		for ii in i:
  			corners.append(ii)

  	cv2.imwrite("newImage.jpg", img)
 	centers = kmeans(img, corners, width, numCorners)
 	return centers
	#eliminateExtraCorners(img, centers)
 	# eliminateExtraCorners(centers)



def kmeans(img, corners, width, numCorners):
	k = numCorners
	corners = np.float32(corners)
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
	flags = cv2.KMEANS_RANDOM_CENTERS
	ret,labels,centers=cv2.kmeans(corners,k,criteria,10,flags)

	for c in centers:
		cv2.circle(img, (int(c[0]), int(c[1])), 5, (255,255,255),1) 

	# print "Rectangle"
	# print int(centers[0][0]), int(centers[0][1]), int(centers[1][0]), int(centers[1][1]), int(centers[2][0]), int(centers[2][1]), int(centers[3][0]), int(centers[3][1])

	# print "drew circle"
 	cv2.imwrite('newImage.jpg', img)
 	return centers

# def findK(corners):
# 	#square root of the number of data pointws divded by two
# 	#elbow method

# 	length = len(corners)
# 	k = int(math.sqrt(length)/2)
# 	return k


def eliminateExtraCorners(img, corners):
	avg = 0
	totalNumOfCorners = pow(len(corners)-1,2)
	outliers = []
	allDistances = []

	for c1 in corners:
		distances = []
		for c2 in corners:
			if((c1[0] != c2[0]) and (c1[1] != c2[1])):
				d = distanceBetweenPoints(c1, c2)
				allDistances.append(d)
				avg+=d
				distances.append(d)

		# print distances


		# mean_duration = np.mean(distances)
		# std_dev_one_test = np.std(distances)
		# if abs(distances - mean_duration) <= std_dev_one_test:
		# 	print distances
		# print distances
	avg = avg/totalNumOfCorners
	# print avg
	print avg*0.5

	for i in range(len(corners)):
		for j in range(len(corners)):
			if((corners[i][0] != corners[j][0]) and (corners[i][1] != corners[j][1])):
				d = distanceBetweenPoints(corners[i], corners[j])
				print "....." + str(d)
				if(avg*0.5 > d):
					print d
					outliers.append(i)
					outliers.append(j)
					#outliers.append([corners[i][0], corners[i][1]])
					#outliers.append([corners[j][0], corners[j][1]])
					#cv2.circle(img, (int(c1[0]), int(c1[1])), 5, (255,0,255),1) 
					#cv2.circle(img, (int(c2[0]), int(c2[1])), 5, (255,0,255),1) 
					




	print outliers
	outlierIndex = findMaxOccurrences(outliers)
	cv2.circle(img, (int(corners[1][0]), int(corners[1][1])), 5, (255,0,255),1)
	print "colored" 
	# cv2.circle(img, (int(c1[0]), int(c1[1])), 5, (255,0,255),1) 
	# cv2.circle(img, (int(c2[0]), int(c2[1])), 5, (255,0,255),1) 
 	cv2.imwrite('newImage.jpg', img)


def distanceBetweenPoints(point1, point2):
	return math.sqrt(math.pow(point1[0]-point2[1], 2) + math.pow(point1[1]-point2[1], 2))


def median(lst):
    sortedLst = sorted(lst)
    lstLen = len(lst)
    index = (lstLen - 1) // 2

    if (lstLen % 2):
        return sortedLst[index]
    else:
        return (sortedLst[index] + sortedLst[index + 1])/2.0

def findMaxOccurrences(lst):
    return max(set(lst), key=lst.count)

def detectOtherShapes(width, height):
	im = cv2.imread("oldImage.jpg")
	imEllipse = cv2.imread("ellipse.jpg")
	imRect = cv2.imread("rectangle.jpg")
	imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	imgray_Blue = cv2.GaussianBlur(imgray, (15,15),0)
	thresh = cv2.adaptiveThreshold(imgray_Blue, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11,1)
	kernel = np.ones((3,3), np.uint8)
	closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations = 4)
	cont_img = closing.copy()

	contours, hierarcy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	areaOfShape = 0
	areaOfRotRectangle = 0
	areaOfRectangle = 0
	areaOfCircle = 0
	areaOfEllipse = 0
	areaOfTriangle = 0
	rect = 0
	box = 0
	center = 0
	radius = 0
	ellipse = 0
	x = 0
	y = 0
	w = 0
	h = 0

	for cnt in contours:
		#area of drawn shape
		areaOfShape = int(cv2.contourArea(cnt))

		#straight rectangle
		x,y,w,h = cv2.boundingRect(cnt)
		cv2.rectangle(imRect,(x,y),(x+w,y+h),(0,255,0),2)
		cv2.imwrite("rectangle.jpg", imRect)
		areaOfRectangle = findAreaOfShape("rectangle.jpg")

		#rotated rectangle
		rect = cv2.minAreaRect(cnt)
		box = cv2.cv.BoxPoints(rect)
		box = np.int0(box)
		areaOfRotRectangle = int(cv2.contourArea(box))

		#circle
		(x, y),radius = cv2.minEnclosingCircle(cnt)
		center = (int(x), int(y))
		radius = int(radius)
		areaOfCircle = int(math.pi * math.pow(radius, 2))

		#ellipse
		ellipse = cv2.fitEllipse(cnt)
		cv2.ellipse(imEllipse, ellipse, (0,0,0), 2)
		cv2.imwrite("ellipse.jpg", imEllipse)
		areaOfEllipse = findAreaOfShape("ellipse.jpg")

		areaOfTriangle = areaOfRotRectangle/2

	areas = [areaOfRectangle, areaOfRotRectangle, areaOfCircle, areaOfEllipse, areaOfTriangle]
	closestArea = (min(areas, key=lambda x:abs(x-areaOfShape)))


	##	print "Line"
	## print firstPointX, firstPointY, lastPointX, lastPointY

	#cv2.drawContours(im,contours,0,(0,0,255),2)
	#cv2.imwrite("newImage.jpg", im)

	if(areaOfRectangle == closestArea):
		print "Rectangle"
		print x, y, w, h
		with open("shapes.txt", 'a') as f:
			f.write("Triangle" + ' ')
			f.write(str(int(x)) + ' ')
			f.write(str(int(y)) + ' ')
			f.write(str(int(w)) + ' ')
			f.write(str(int(h)) + ' ')
		#cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
	if(areaOfRotRectangle == closestArea):
		print "Rotated Rectangle"
		print box[0][0], box[0][1], box[1][0], box[1][1], box[2][0], box[2][1], box[3][0], box[3][1]
		with open("shapes.txt", 'a') as f:
			f.write("Triangle" + '\n')
			f.write(str(int(box[0][0])) + ' ')
			f.write(str(int(box[0][1])) + ' ')
			f.write(str(int(box[1][0])) + ' ')
			f.write(str(int(box[1][1])) + ' ')
			f.write(str(int(box[2][0])) + ' ')
			f.write(str(int(box[2][1])) + ' ')
			f.write(str(int(box[3][0])) + ' ')
			f.write(str(int(box[3][1])) + ' ')
		#cv2.drawContours(im, [box], 0, (255,0,0),2)

	if(areaOfCircle == closestArea):
		print "Circle"
		#cv2.circle(im, center,radius,(0,255,0),2)

	if(areaOfEllipse == closestArea):
		centerX = ellipse[0][0]
		centerY = ellipse[0][1]
		radiusX = ellipse[1][0]
		radiusY = ellipse[1][1]
		rotation = ellipse[2]

		print "Ellipse"
		print centerX, centerY, radiusX, radiusY, rotation
		with open("shapes.txt", 'a') as f:
			f.write("Ellipse" + ' ')
			f.write(str(centerX) + ' ')
			f.write(str(centerY) + ' ')
			f.write(str(radiusX) + ' ')
			f.write(str(radiusY) + ' ')
			f.write(str(rotation) + ' ')
		#cv2.ellipse(im, ellipse, (0,0,0), 2)

	if(areaOfTriangle == closestArea):
		print "Triangle"
		corners = detectCorners(height, width, 3)
		print int(corners[0][0]), int(corners[0][1]), int(corners[1][0]), int(corners[1][1]), int(corners[2][0]), int(corners[2][1])
		with open("shapes.txt", 'a') as f:
			f.write("Triangle" + '\n')
			f.write(str(int(corners[0][0])) + ' ')
			f.write(str(int(corners[0][1])) + ' ')
			f.write(str(int(corners[1][0])) + ' ')
			f.write(str(int(corners[1][1])) + ' ')
			f.write(str(int(corners[2][0])) + ' ')
			f.write(str(int(corners[2][1])) + ' ')






def findAreaOfShape(file):
	imEllipse = cv2.imread(file)
	imgray = cv2.cvtColor(imEllipse, cv2.COLOR_BGR2GRAY)
	imgray_Blue = cv2.GaussianBlur(imgray, (15,15),0)
	thresh = cv2.adaptiveThreshold(imgray_Blue, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11,1)
	kernel = np.ones((3,3), np.uint8)
	closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations = 4)
	cont_img = closing.copy()

	contours, hierarcy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	areaOfShape = 0
	for cnt in contours:
		areaOfShape = int(cv2.contourArea(cnt))
	return areaOfShape



arr = stringToArray(array)
sizeArray = stringToArray(size)
width = int(sizeArray[0])
height = int(sizeArray[1])
# print "create Img"
createImage(arr, width, height)
detectShapes(arr, width, height)
#detectPerimeter(height, width)
#detectCorners()
#houghLines = detectLines()					#detect lines
#drawDetectedLine(houghLines, arr, width, height)
#detectShapes(arr)
#contour()

