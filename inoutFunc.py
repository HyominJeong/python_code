import numpy as np
import matplotlib.pyplot as plt
import re
import os

def SDIDtoCLF(SDID, sdxyzclf_raw="/ta/work/user/hyomin/sdanalysis_2018_TALE_TAx4SingleCT_KM/inc/sdxyzclf_raw.h"):

  cmd = 'grep "^  %s" %s' % (SDID, sdxyzclf_raw)
  SDIDCLFLine = os.popen(cmd).read().split("\n")[0].split(',')[1:4]
  #print SDIDCLFLine
  return SDIDCLFLine 

def LineSDIDtoCLF(LineSDID, sdxyzclf_raw="/ta/work/user/hyomin/sdanalysis_2018_TALE_TAx4SingleCT_KM/inc/sdxyzclf_raw.h"):
  edgeLineCLF=[]
  for lineSeg in LineSDID:
    edgeLineCLF.append([SDIDtoCLF(lineSeg[0]), SDIDtoCLF(lineSeg[1])])
  return np.array(edgeLineCLF, dtype=np.float)

def SDedgeIDs(sdEdgeFile = "/ta/work/user/hyomin/sdanalysis_2018_TALE_TAx4SingleCT_KM/sduti/sdparamborder.c"):
  edEdgeLines = open(sdEdgeFile, 'r')

  eof = False
  edgeStart = False
  edgeLineSDID = []
  while ~eof:
    line=edEdgeLines.readline()
    #print line
    if line=='':
      eof=True
    if not line: break
    if line.startswith("static double sdedgelinesRAW"):
      line=edEdgeLines.readline()
      edgeStart = True
    if edgeStart:
      #print line
      if line.startswith("    {"):
        SDIDYY1, SDIDXX1, SDIDYY2, SDIDXX2 = re.findall("\d+", line)#line.strip().strip('{').strip('}').split(',')
        #edgeLineSDID.append([[SDIDYY1, SDIDXX1],[SDIDYY2, SDIDXX2]])
        edgeLineSDID.append(["%s%s" % (SDIDYY1, SDIDXX1),"%s%s" % (SDIDYY2, SDIDXX2)])

        #print SDIDYY1, SDIDXX1, SDIDYY2, SDIDXX2
        #print line.strip().strip('{').strip('}').strip("\n").split(',')
        #break
      if line.startswith("  };"):
        edgeStart = False
        eof=True
  return edgeLineSDID

def plotLoop(cLoop):
  for line in cLoop:
    plt.plot(line.T[0], line.T[1], marker='o', color='black')

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


def cross(point, lineSeg):
  # calculate a, b of y=ax+b of line segment
  delta = lineSeg[1] - lineSeg[0]
  a = delta[1]/delta[0]
  b = lineSeg[1][1] - a * lineSeg[1][0]
  print lineSeg, a, b
  # node
  x = point[0]
  y = a * x + b
  print x, y, lineSeg.T
  if y <= max(lineSeg.T[1]) and y >= min(lineSeg.T[1]):
    return 1
  else:
    return 0

def inLoop(point, cLoop):
  nofCross = 0
  for lineSeg in cLoop:
    if intersect(point, [1.e6, 0], lineSeg[0], lineSeg[1]):
      nofCross += 1
  return nofCross
