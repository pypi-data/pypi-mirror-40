'''
Created on Aug 14, 2017

@author: hammonds
'''
from pyimm.GetImmStartIndex import GetStartPositions
from pyimm.immheader import readAllHeaders
from pyimm.immheader import getNumberOfImages
from pyimm.OpenMultiImm import OpenMultiImm


filename = "/Users/hammonds/RSM/Dufresne/S139/bnt5bt.spec_s139_dark_00001-00005.imm"

fp = open(filename, "rb")

numImages = getNumberOfImages(fp)

print ("Number of images %d" % numImages)

hdrs = readAllHeaders(fp, numImages)
 
print (hdrs[0].keys())
for h in hdrs:
    print ("Header[%d] %s" % (int(h), hdrs[h]))

startPos, dlen = GetStartPositions(filename, numImages)


print ("Start Positions %s" % startPos)
print ("dataLength %s "  % dlen)

imgs = OpenMultiImm(filename, 0, numImages, startPos, dlen)
import matplotlib.pyplot as plt
for i in range(numImages):
    plt.imshow(imgs[i])
    plt.show()