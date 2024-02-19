import cv2, time
import numpy as np


# Placeholder queue for audio stream
# q = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]



# load image
img = cv2.imread("testing/test_photo.JPG", cv2.IMREAD_UNCHANGED)


# bgr channels
bgr = img[:,:,0:3]

# convert to HSV
# h is [0, 179]
# s is [0, 255]
# v is [0, 255]
hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(hsv)


def imageLoop(offset):
    # Hue shift
    # hnew = np.mod(h + q.pop(), 180).astype(np.uint8)

    # recombine
    # hsv_new = cv2.merge([hnew, s, v])
    hsv[:,:,0] = np.mod(h + offset, 180).astype(np.uint8)

    # back to bgr
    bgr_new = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # save output
    # cv2.imwrite('testing/output.png', bgr_new)

    # Display various images to see the steps
    # time.sleep(1)

    cv2.imshow('bgr_new',bgr_new)
    cv2.waitKey(1)
# cv2.destroyAllWindows()
