from subprocess import call
import math, re
from PIL import Image

call(["casperjs", "bluescrape.js"])

with open("filename.txt", 'rb') as f:
  filename = f.readlines()

call(["wget", "-O", "dolar.png", filename[0]])

im = Image.open("dolar.png")
pix = im.load()

def colorDistance(a, b):
    return math.sqrt( (b[0] - a[0])**2 + (b[1] - a[1])**2 + (b[2] - a[2])**2 + (b[3] - a[3])**2 )

def extractTableData(column, row, outFile):
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
    try:
        region.save("tmp.png")
    except IOError:
        print "cannot save tmp.png"
        return
    call(["tesseract", "tmp.png", outFile])


extractTableData(2, 3, "valorCompra")
extractTableData(3, 3, "valorVenta")

valorCompra = 0
valorVenta = 0
try:
    with open('valorCompra.txt', 'r') as f:
        tmp = f.readlines()
        valorCompra = re.sub("[^0-9\.,]", "", tmp[0]).replace(',', '.')

    with open('valorVenta.txt', 'r') as f:
        tmp = f.readlines()
        valorVenta = re.sub("[^0-9\.,]", "", tmp[0]).replace(',', '.')
    

    print " ".join(["../bluelytics/add_blue.sh", valorCompra, valorVenta])
    call(["../bluelytics/add_blue.sh", valorCompra, valorVenta])

except IOError:
    print "Cannot read value files"