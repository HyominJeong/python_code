import SDAnaFunc
import numpy as np
import sys
import matplotlib.pyplot as plt

#GPSInputs = np.loadtxt("/ta/work/user/hyomin/GPS/KMCT_GPS_MiliArcSec.txt")
GPSInputs = np.loadtxt(sys.argv[1])
Output = []
for a in GPSInputs:
  #print a
  YYXX, xyz = SDAnaFunc.GPS2CLF(a[0], a[1], a[2], a[3])
  Output.append([int(YYXX), xyz[0], xyz[1], xyz[2]])
  #print("%d 741 20121116 6899 6598 1.1 1.1 4095 4095 20121116/led741up 20121116/led741low A" % a[0]) # for ledlin_tax4.dat
  #print("%d 0.0 //" % a[0]) # for Cable delay


Output = np.array(Output, dtype=np.float)
sortInd = np.argsort(Output, axis=0).T[0]
print("Number of SDs are %2d" % len(Output))

XX = Output.T[0] % 100
YY = Output.T[0] // 100

for Ind in sortInd:
  #print(XX, YY)
  print("  %d,%.6f,%.6f,%.8f," % (Output[Ind][0], Output[Ind][1],Output[Ind][2],Output[Ind][3])) # for sdxyzclf_raw.h 
  #print("    %d," % Output[Ind][0]) # for sk_xxyy.h
  #print("%d 0.0 //" % Output[Ind][0]) # for Cable delay
  #print("%d%02d 741 20121116 6899 6598 1.1 1.1 4095 4095 20121116/led741up 20121116/led741low A" % (XX, YY)) # for ledlin_tax4.dat
plt.scatter(XX, YY)
plt.show()

