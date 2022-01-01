import cv2

def adaptive_threshold(image, sigma):
  # convert the image to grayscale and blur it slightly
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  blurred = cv2.GaussianBlur(gray, (sigma, sigma), 0)

  # apply simple thresholding with a hardcoded threshold value
  (T, threshInv) = cv2.threshold(blurred, 230, 255,
    cv2.THRESH_BINARY_INV)

  # apply Otsu's automatic thresholding
  (T, threshInv) = cv2.threshold(blurred, 0, 255,
    cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

  # instead of manually specifying the threshold value, we can use
  # adaptive thresholding to examine neighborhoods of pixels and
  # adaptively threshold each neighborhood
  thresh = cv2.adaptiveThreshold(blurred, 255,
    cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 10)

  # perform adaptive thresholding again, this time using a Gaussian
  # weighting versus a simple mean to compute our local threshold
  # value
  thresh = cv2.adaptiveThreshold(blurred, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 4)

  imagem = cv2.bitwise_not(thresh)

  return imagem
