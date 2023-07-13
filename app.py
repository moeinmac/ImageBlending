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

img1 = cv2.imread("face1.jpg")
img2 = cv2.imread("face2.jpg")
mask = cv2.imread("maskFa.jpg",0)


img1R,img1G,img1B = cv2.split(img1)
img2R,img2G,img2B = cv2.split(img2)

img1R_gp = GaussianPyramid(img1R)
img1G_gp = GaussianPyramid(img1G)
img1B_gp = GaussianPyramid(img1B)

mask_gp = GaussianPyramid(mask)

img2R_gp = GaussianPyramid(img2R)
img2G_gp = GaussianPyramid(img2G)
img2B_gp = GaussianPyramid(img2B)