import cv2
import numpy as np


def extractclusters(mask, image):
  gray = cv2.cvtColor(mask, cv2.COLOR_RGB2GRAY)

  (contours,_) = cv2.findContours(gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

  if len(contours) > 1:
    contours = getclusters(contours)
  else:
    contours = []

  clusters = []
  for contour in contours:
      (x,y,w,h) = cv2.boundingRect(contour)

      clusters.append(crop(image,x,y,w,h)) # crop the mask if going for segmentation or the image if bounding box
      
  return clusters










def crop(image,x,y,w,h):
  return image[y-50:y+h+50, x-50:x+w+50]


def makemask(image, mask):
  return cv2.bitwise_and(image, mask)


def getclusters(contours):
  #contours = contours[1:] 
  # Remove the first one as is always not a real
  #one probs cus the image is a funny colour, if black and white would be fine

  areas = [cv2.contourArea(c) for c in contours]
  sorted = np.sort(areas)

  max = sorted[-1]
  threshold = 0 # Test different thresholding techniques

  rois = [contours[areas.index(max)]]

  for x in range(len(sorted)-2,0, -1):
    if sorted[x] > max - threshold:
      rois.append(contours[areas.index(sorted[x])])

  return rois