import Image
from subprocess import call
import math

#call(["casperjs", "bluescrape.js"])

#with open("filename.txt", 'rb') as f:
#  filename = f.readlines()

#call(["wget", "-O", "dolar.png", filename[0]])

im = Image.open("dolar.png")
pix = im.load()

def colorDistance(a, b):
    return math.sqrt( (b[0] - a[0])**2 + (b[1] - a[1])**2 + (b[2] - a[2])**2 + (b[3] - a[3])**2 )

def cropColumnRow(column, row):
    borderpix = pix[0,0]
    sepsH = []
    for i in xrange(1,im.size[0]):
        if colorDistance(pix[i, 1], borderpix) < 10:
            sepsH.append(i)


    sepsV = []
    for i in xrange(1,im.size[1]):
        if colorDistance(pix[1,i], borderpix) < 10:
            sepsV.append(i)

    print sepsV
    leftBorder = sepsH[column-2]+1
    rightBorder = sepsH[column-1]-1
    topBorder = sepsV[row-2]
    bottomBorder = sepsV[row-1]

    box = (leftBorder, topBorder, rightBorder, bottomBorder)
    print box
    region = im.crop(box)
    region.show()

cropColumnRow(3, 3)