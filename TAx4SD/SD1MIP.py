import numpy as np
import os, sys
from SD1MIPFunc import *
from datetime import date
from SDAnaFunc import GPS2CLF


ct = sys.argv[1]

dirTower = "/ta/work/user/hyomin/tower"
dirRawData = ("%s/%s/data/" % (dirTower, ct.lower()))
fileSDList = ("/ta/work/user/hyomin/GPS/%sCT_GPS_MiliArcSec.txt" % ct.upper())
fileResult = open("/ta/work/user/hyomin/tower/%sMIP.txt" % ct.lower(), 'w')

SDList = np.loadtxt(fileSDList, dtype=int)
SDMip_upper = []
SDMip_lower = []
x_km = []
y_km = []
for SDinfo in SDList:
  YYXX, xyz = GPS2CLF(SDinfo[0], SDinfo[1], SDinfo[2], SDinfo[3])

  #print xyz
  
  x_km.append(xyz[0])
  y_km.append(xyz[1])
  
  MipMP, days = dailyMIP(191201, 191231, ct, SDinfo[0])

  SDMip_upper.append(avgMIP(MipMP[0], days[0]))
  SDMip_lower.append(avgMIP(MipMP[1], days[0]))
  
  #SDMip_upper.append(0)
  #SDMip_lower.append(1)
  fileResult.write("%s %05.2f %05.2f %06.2f %06.2f\n" % (YYXX, xyz[0], xyz[1], SDMip_upper[-1], SDMip_lower[-1]))

fileResult.write("Wrong communication SDs are")
SDMipMP_upper = np.array(SDMip_upper)
SDMipMP_lower = np.array(SDMip_lower)
SDPos = np.array(SDList).T[0]

print(SDPos[SDMipMP_upper == 0])
print(SDPos[SDMipMP_lower == 0])
print("mean and std of good SDs are")
print("%6.2f +- %5.2f" % (SDMipMP_upper[SDMipMP_upper > 0].mean(), SDMipMP_upper[SDMipMP_upper > 0].std()))
print("%6.2f +- %5.2f" % (SDMipMP_lower[SDMipMP_lower > 0].mean(), SDMipMP_lower[SDMipMP_lower > 0].std()))


fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (10,5))
im = ax1.scatter(x_km, y_km, c = SDMip_upper, label="Upper", vmin=0, vmax = 200)
im = ax2.scatter(x_km, y_km, c = SDMip_lower, label="Lower", vmin=0, vmax = 200)

fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
fig.colorbar(im, cax=cbar_ax)

#ax1.colorbar(label='color')
#ax2.colorbar(label='color')

#ax1.plot(days[1], MipMP[1], label="Lower")
#ax1.legend()

#print(SDList)

#ax2.plot(PedHist[0])
#ax2.plot(PedHist[1])
#fig.suptitle(SDID)
plt.show()

