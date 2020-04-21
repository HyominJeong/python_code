import inoutFunc
import matplotlib.pyplot as plt
import numpy as np
'''
cLoop = np.array([\
  [[-1, -1], [-1+1.e-6, 1]],\
  [[-1+1.e-6,  1], [ 1, 1]],\
  [[ 1,  1], [ 1-1.e-6,-1]],\
  [[ 1-1.e-6, -1], [-1,-1]]\
  ])

inoutFunc.plotLoop(cLoop)
plt.xlim(-2,2)
plt.ylim(-2,2)

point = [0, 0]

nOfCross = inoutFunc.inLoop(point, cLoop)

print nOfCross

plt.scatter(point[0], point[1], marker='*')
plt.show()
  

'''

SDIDLine = inoutFunc.SDedgeIDs()
print SDIDLine

edgeSDCLF = inoutFunc.LineSDIDtoCLF(SDIDLine).T[:2].T

inoutFunc.plotLoop(edgeSDCLF)

samplePoints = [[0, 32],[0, 40]]
#plt.scatter(samplePoints, color=red)
for point in samplePoints:
  print point, inoutFunc.inLoop(point, edgeSDCLF) % 2
  if (inoutFunc.inLoop(point, edgeSDCLF) % 2):
    inside=True
  else:
    inside=False
  plt.scatter(point[0],point[1], label=inside, color='black')

#plt.show()
plt.legend()
plt.show()
