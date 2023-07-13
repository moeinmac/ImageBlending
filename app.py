import cv2
import numpy as np
from scipy import ndimage

kernel = (1.0/256)*np.array([[1, 4, 6, 4, 1],[4, 16, 24, 16, 4],[6, 24, 36, 24, 6], [4, 16, 24, 16, 4],[1, 4, 6, 4, 1]])

def reduceImage(image):
  imageFilter = cv2.filter2D(image,-1,kernel)
  reduced = imageFilter[::2, ::2] 
  return reduced

def expandImage(image):
  expanded = np.zeros((2*image.shape[0], 2*image.shape[1]))
  expanded[::2, ::2] = image
  imageFilter = ndimage.convolve(expanded,4*kernel, mode='constant')
  return imageFilter

def GaussianPyramid(image):
  gp = [image]
  while image.shape[0] >= 2 and image.shape[1] >= 2:
    image = reduceImage(image)
    gp.append(image)
  return gp

def LaplacianPyramid(gp):
  lp = []
  for i in range(len(gp) - 1):
    lp.append(gp[i] - expandImage(gp[i + 1]))
  return lp


def blendingPyramid(lpA,lpB,gpMask):
  blend = []
  for i in range(len(lpA)):
    bl = gpMask[i]/255*lpA[i] + (1-gpMask[i]/255)*lpB[i]
    blend.append(bl)
  return blend

def reconstruct(pyramid):
  revPyramid = pyramid[::-1]
  image = revPyramid[0]
  for i in range(1, len(revPyramid)):
    image = expandImage(image) + revPyramid[i] 
  return image
