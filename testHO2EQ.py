import numpy as np
import HO2EQ

yymmdd = '200331'
hhmmss = '060000'
Az_deg = 101 + 51. / 60  + 15. / 3600 #(N-E)
Alt_deg = 44 + 9. / 60 + 41.2 / 3600
Ra_true_deg = 14 * 15 + 16. / 4 + 37.6 / 60 / 4
Dec_true_deg = 19 + 5. / 60 + 33.7 / 3600

theta = 90 - Alt_deg
#phi = Az_deg
phi = (90 - Az_deg) % 360 #(E-N)

print theta, phi

ra, dec = HO2EQ.HO2EQ(theta, phi, yymmdd, hhmmss)

print "Ra:", ra, Ra_true_deg #"deg", "%02d %02d %04.1f" % (ra//15, ra%15 // 4, ra % 15 % 4),"hh mm ss"
print "Dec:", dec, Dec_true_deg #"deg", dec//1, dec%1 * 60 / 100

#yymmdd = '000102'
#ra, dec = HO2EQ.HO2EQ(theta, phi, yymmdd, hhmmss)

#print ra, dec

#for hh in range(0, 24):
#  hhmmdd = ("%02d0000" % hh)
#  a, A = HO2EQ.EQ2HO(120, 0, '200101', hhmmdd)
#
#  #print a,A
