from PIL import Image, ImageFilter
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import radon, rescale, rotate
import statistics

def jopa(PATH):

    gray_im = cv2.imread(PATH, 0)

    pixels = gray_im
    width, heigth = len(sum(rotate(gray_im, 0))), len(gray_im)

    def mute_im(n):
        pix = np.zeros((heigth, width), dtype='float64')
        for i in range(heigth - 1):
            for j in range(width - 1):
                if i < n:
                    first_i = 0
                else:
                    first_i = i - n

                if j < n:
                    first_j = 0
                else:
                    first_j = j - n

                if j + n >= width:
                    last_j = width - 1
                else:
                    last_j = j + n

                if i + n >= heigth:
                    last_i = heigth - 1
                else:
                    last_i = i + n

                sred = 0
                for a in range(first_i, last_i + 1):
                    for b in range(first_j, last_j + 1):
                        sred += pixels[a][b]

                sred -= pixels[i][j]
                sred = sred // ((last_i - first_i + 1) * (last_j - first_j + 1) - 1)
                pix[i][j] = sred


        return pix

    muted_image = mute_im(6)

    def discrete_radon_transform(image):
        steps = len(sum(rotate(image, 0)))
        R = np.zeros((len(image), steps), dtype='float64')
        image = np.transpose(image)
        for s in range(steps):
            # rotation = rotate(image, -s*180/steps)
            rotation = rotate(image, 0)
            R[:, s] = sum(rotation)
        return R

    sinogram = discrete_radon_transform(muted_image)
    sinogram = sinogram[:-1]

    points = []
    for i in sinogram:
        points.insert(len(points), i[0])

    strings = []
    strings_points = []
    max = sorted(points)
    max = max[len(max)-1] * 0.98

    for i in range(len(points)):
        if i > 0 and i < len(points)-1:
            if points[i - 1] > points[i] and points[i] < points[i + 1] and points[i] < max:
                strings.insert(len(strings), i)
                strings_points.insert(len(strings_points), points[i])

    intervals = []
    for i in range(len(strings)):
        if i != 0:
            intervals.insert(len(intervals), strings[i] - strings[i-1])


    mean = statistics.mean(intervals)
    std = statistics.stdev(intervals)
    max = sorted(intervals)[len(intervals)-1]


    if std < 0.4:

        return 0

    whatermark = ""
    for i in intervals:
        if i > mean + std:
            whatermark += "1"
        else:
            whatermark += "0"

    #plt.imshow(sinogram, cmap=plt.cm.Greys_r, aspect='auto')
    return whatermark
    #Whatermark =  010010000101001101000101

