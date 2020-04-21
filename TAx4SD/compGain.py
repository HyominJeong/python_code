import numpy as np
import os, sys
from SD1MIPFunc import *
from datetime import date
from SDAnaFunc import GPS2CLF

if len(sys.argv) < 2:
  ct = 'km'
else:
  ct = sys.argv[1]

dirTower = "/ta/data/SD/TAx4/tower"
dirRawData = ("%s/%s/data/" % (dirTower, ct.lower()))
fileSDList = ("/ta/work/user/hyomin/GPS/%sCT_GPS_MiliArcSec.txt" % ct.upper())
fileResult = open("/ta/work/user/hyomin/tower/%sMIP.txt" % ct.lower(), 'w')

SDList = np.loadtxt(fileSDList, dtype=int)
SDMip_upper = []
SDMip_lower = []
x_km = []
y_km = []
yy, mm, dds, = [20, 02, [24, 27]]
'''
fileCompGain = open("/ta/work/user/hyomin/tower/%s/%02d%02d02%d.%02d.txt" % (ct.lower(), yy, mm, dds[0] , dds[1]), 'w')
for SDinfo in SDList:
  YYXX, xyz = GPS2CLF(SDinfo[0], SDinfo[1], SDinfo[2], SDinfo[3])

  #print xyz
  
  x_km.append(xyz[0])
  y_km.append(xyz[1])

  fig, axs = plt.subplots(2,2)

  fileCompGain.write("%s" % SDinfo[0])

  # Loop over selected two days
  for i in range(len(dds)):
    PedMP = [[],[]]
    MipMP = [[],[]]
    avgPedMP = [[],[]]
    avgMipMP = [[],[]]
    # Accumulate over hours
    for hh in range(0, 24):
      fileRaw=("/ta/work/user/hyomin/tower/%s/data/%s%02d%02d%02d.Y20%02d" % (ct.lower(), ct.upper(), mm, dds[i], hh, yy))
      MipHists, MipChans , PedHists, PedChans = read1MIPPed(fileRaw, SDinfo[0])
      pltHists(PedHists[0], PedChans[0], axs[i][0], 'black')
      pltHists(MipHists[0], MipChans[0], axs[i][1], 'black')
      pltHists(PedHists[1], PedChans[1], axs[i][0], 'red')
      pltHists(MipHists[1], MipChans[1], axs[i][1], 'red')

      # Loop over layer
      for ll in range(len(PedHists)):
        # Loop over events (1 events / 10mins)
        for jj in range(len(PedHists[ll])):
          PedMP[ll].append(calMP(PedHists[ll][jj], PedChans[ll][jj]))
          MipMP[ll].append(calMP(MipHists[ll][jj], MipChans[ll][jj]))

    PedMP = np.array(PedMP)
    MipMP = np.array(MipMP)
    fileCompGain.write("\t%02d%02d%02d" % (yy, mm, dds[i]))
    for ll in range(2):
      avgPedMP[ll] = PedMP[ll][PedMP[ll] > 0].mean()
      avgMipMP[ll] = MipMP[ll][MipMP[ll] > 0].mean()

      print("%s[%d]\t%02d%02d%02d\tMipMP - PedMP = %6.2f - %6.2f = %6.2f" % (SDinfo[0], ll, yy, mm, dds[i], avgMipMP[ll], avgPedMP[ll], avgMipMP[ll] - avgPedMP[ll]))
      fileCompGain.write("\t%6.2f\t%6.2f\t%6.2f" % (avgMipMP[ll], avgPedMP[ll], avgMipMP[ll] - avgPedMP[ll]))

  fileCompGain.write("\n")
  fig.suptitle("%s %02d%02d02%d&%02d" % (SDinfo[0], yy, mm, dds[0] , dds[1]))
  plt.savefig("%s.%02d%02d02%d.%02d.png" % (SDinfo[0], yy, mm, dds[0] , dds[1]))
  
'''
CompGains = np.loadtxt("/ta/work/user/hyomin/tower/%s/%02d%02d02%d.%02d.txt" % (ct.lower(), yy, mm, dds[0] , dds[1]), dtype=np.float)
print(CompGains[:5])
