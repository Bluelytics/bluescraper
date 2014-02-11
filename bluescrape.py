from subprocess import call
import math, re
from PIL import Image, ImageEnhance

call(["casperjs", "bluescrape.js"])

with open("filename.txt", 'rb') as f:
  filename = f.readlines()

call(["wget", "-O", "dolar.png", filename[0]])

im = Image.open("dolar.png")
pix = im.load()

def colorDistance(a, b):
    return math.sqrt( (b[0] - a[0])**2 + (b[1] - a[1])**2 + (b[2] - a[2])**2 + (b[3] - a[3])**2 )



def findBorder(img, horizontal=False, reverse=False):
    impix = img.load()
    borderpix = impix[2,2]
    range_x = range(2, img.size[0])
    range_y = range(2, img.size[1])

    if reverse:
        range_x.sort(reverse=True)
        range_y.sort(reverse=True)

    if horizontal:
        for x in range_x:
            for y in range_y:
                if math.fabs(impix[x, y]-borderpix) > 10:
                    return x
    else:
        for y in range_y:
            for x in range_x:
                if math.fabs(impix[x, y]-borderpix) > 10:
                    return y
    if reverse:
        return (img.size[0], img.size[1])
    else:
        return (0,0)

def autocrop(img):
    
    top = max(0, findBorder(img)-10)
    bottom = min(findBorder(img, reverse=True)+10, img.size[1])
    left = max(0, findBorder(img, horizontal=True)-10)
    right = min(findBorder(img, reverse=True, horizontal=True)+10, img.size[0])
    
    box = (left, top, right, bottom)
    print box
    return img.crop(box)

def enhance(img, textColor):
    return img.point(lambda i: 255 if math.fabs(i-textColor) < 10 else 0)
    


def extractTableData(column, row, outFile, textColor):
    borderpix = pix[0,0]
    sepsH = []
    for i in xrange(1,im.size[0]):
        if colorDistance(pix[i, 1], borderpix) < 10:
            sepsH.append(i)


    sepsV = []
    for i in xrange(1,im.size[1]):
        if colorDistance(pix[1,i], borderpix) < 10:
            sepsV.append(i)

    leftBorder = sepsH[column-2]+1
    rightBorder = sepsH[column-1]-1
    topBorder = sepsV[row-2]
    bottomBorder = sepsV[row-1]

    box = (leftBorder, topBorder, rightBorder, bottomBorder)

    region = im.crop(box).convert('L')

    final = enhance(autocrop(region), textColor)

    try:
        final.save("tmp.png")
    except IOError:
        print "cannot save tmp.png"
        return
    call(["tesseract", "tmp.png", outFile])


extractTableData(2, 3, "valorCompra", 183)
extractTableData(3, 3, "valorVenta", 255)

valorCompra = 0
valorVenta = 0
try:
    with open('valorCompra.txt', 'r') as f:
        tmp = f.readlines()
        valorCompra = re.sub("[^0-9\.,]", "", tmp[0]).replace(',', '.')

    with open('valorVenta.txt', 'r') as f:
        tmp = f.readlines()
        valorVenta = re.sub("[^0-9\.,]", "", tmp[0]).replace(',', '.')
    

    call(["../bluelytics/add_blue.sh", valorCompra, valorVenta, "dolarblue.net"])

except IOError:
    print "Cannot read value files"
