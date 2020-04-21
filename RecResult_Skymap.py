import matplotlib.pyplot as plt
import os, sys
import numpy as np
import glob
from RecResultFunc import *

# Energy scale factor, from hybrid events with FD
enscale = 1.0 / 1.27


lines = open(sys.argv[1], 'r').readlines()

# Printed out from EvtTxt files are
#yymmdd, hhmmss, usec, nstclust, t0_geo1, dt0_geo1, xcore_geo1, dxcore_geo1, ycore_geo1, dycore_geo1, theta_geo1, dtheta_geo1, phi_geo1, dphi_geo1, chi2_geo1, ndof_geo1, energy_ldf, chi2_ldf, ndof_ldf


yymmdd = []
hhmmss = []
nstclust = []
x_core_geo1 = []
y_core_geo1 = []
theta = []
phi = []
chi2_geo1 = []
ndof_geo1 = []
chi2_ldf = []
ndof_ldf = []
energy_ldf = []
energy_ldf_log = []
energy_gldf = []
chi2_gldf = []
ndof_gldf = []

# Add every events triggered
#print "Events with Energy > 57"
for line in lines:
  #print line.strip('\n')
  evt = line.strip('\n').split()
  #print evt
  yymmdd.append(evt[0])
  hhmmss.append(evt[1])
  nstclust.append(int(evt[3]))
  x_core_geo1.append(float(evt[6]))
  y_core_geo1.append(float(evt[8]))
  theta.append(float(evt[10]))
  phi.append((180 + float(evt[12])) % 360)
  chi2_geo1.append(float(evt[14]))
  ndof_geo1.append(int(evt[15]))
  energy_ldf.append(float(evt[16]) * enscale)
  energy_ldf_log.append(float(np.log10(float(evt[16]) * enscale)))
  chi2_ldf.append(float(evt[17]))
  ndof_ldf.append(float(evt[18]))
  energy_gldf.append(float(evt[19]) * enscale)
  chi2_gldf.append(float(evt[20]))
  ndof_gldf.append(float(evt[21]))
  #if energy_ldf[-1] > 57: print yymmdd[-1], hhmmss[-1]


Evts = [\
  yymmdd, \
  hhmmss, \
  nstclust, \
  x_core_geo1, \
  y_core_geo1, \
  theta, \
  phi, \
  chi2_geo1, \
  ndof_geo1, \
  energy_ldf, \
  energy_ldf_log, \
  chi2_ldf, \
  ndof_ldf, \
  chi2_gldf, \
  ndof_gldf ]

# File name header
fHeader = sys.argv[1].split(".")[0]

#drawDist(Evts)
print 'total # of events are', len(Evts[0])
#plt.show()
#plt.savefig("%s.ALL.pdf" % fHeader)

# Quality Cut
# QC1: Chi2 < 1.e6 (meaningful chi2)
QC01_Evts = QC(Evts, 'chi2_geo1', 'GE', 1.e6)
QC01_Evts = QC(Evts, 'chi2_gldf', 'GE', 1.e6)
QC1_Evts = QC(QC01_Evts, 'chi2_ldf', 'GE', 1.e6)

#drawDist(QC1_Evts)
print 'total # of events are', len(QC1_Evts[0])
#PO(QC1_Evts, 'energy_ldf', 'GT', 57)
#plt.show()
#plt.savefig("%s.REC.png" % fHeader)

# QC2: energy > 10 >= 0
QC2_Evts = QC(QC1_Evts, 'energy_ldf', 'LT', 10)
#drawDist(QC2_Evts)
print 'total # of events are', len(QC2_Evts[0])
#PO(QC2_Evts, 'energy_ldf', 'GT', 10)
#plt.show()
#plt.savefig("%s.EnGT10.png" % fHeader)

# QC3: energy > 10 >= 0
#QC3_Evts = QC(QC2_Evts, 'energy_ldf', 'LT', 20)
#drawDist(QC3_Evts)
#print 'total # of events are', len(QC3_Evts[0])
#PO(QC2_Evts, 'energy_ldf', 'GT', 10)
#plt.show()
#plt.savefig("%s.EnGT20.png" % fHeader)

# QC4: nstclust > 3
QC3_Evts = QC(QC2_Evts, 'nstclust', 'LT', 4)
#drawDist(QC3_Evts)
#plt.show()
print 'total # of events are', len(QC3_Evts[0])
#plt.savefig("%s.EnGT10.NstGT3.png" % fHeader)

ax = plt.subplot(111, projection="aitoff")
#ax.grid(True)

QC3_Evts = QC(QC3_Evts, 'energy_ldf', 'LT', 57)
QC3_Evts = QC(QC3_Evts, 'theta', 'GT', 55)

ax = plt.subplot(111, projection="aitoff")


plot_mwd(ax)
  

plotRaDecMap(QC1_Evts, ax, 'k', 'KM')


lines = open(sys.argv[2], 'r').readlines()

# Printed out from EvtTxt files are
#yymmdd, hhmmss, usec, nstclust, t0_geo1, dt0_geo1, xcore_geo1, dxcore_geo1, ycore_geo1, dycore_geo1, theta_geo1, dtheta_geo1, phi_geo1, dphi_geo1, chi2_geo1, ndof_geo1, energy_ldf, chi2_ldf, ndof_ldf


yymmdd = []
hhmmss = []
nstclust = []
x_core_geo1 = []
y_core_geo1 = []
theta = []
phi = []
chi2_geo1 = []
ndof_geo1 = []
chi2_ldf = []
ndof_ldf = []
energy_ldf = []
energy_ldf_log = []
energy_gldf = []
chi2_gldf = []
ndof_gldf = []

# Add every events triggered
#print "Events with Energy > 57"
for line in lines:
  #print line.strip('\n')
  evt = line.strip('\n').split()
  #print evt
  yymmdd.append(evt[0])
  hhmmss.append(evt[1])
  nstclust.append(int(evt[3]))
  x_core_geo1.append(float(evt[6]))
  y_core_geo1.append(float(evt[8]))
  theta.append(float(evt[10]))
  phi.append((180 + float(evt[12])) % 360)
  chi2_geo1.append(float(evt[14]))
  ndof_geo1.append(int(evt[15]))
  energy_ldf.append(float(evt[16]) * enscale)
  energy_ldf_log.append(float(np.log10(float(evt[16]) * enscale)))
  chi2_ldf.append(float(evt[17]))
  ndof_ldf.append(float(evt[18]))
  energy_gldf.append(float(evt[19]) * enscale)
  chi2_gldf.append(float(evt[20]))
  ndof_gldf.append(float(evt[21]))
  #if energy_ldf[-1] > 57: print yymmdd[-1], hhmmss[-1]

Evts = [\
  yymmdd, \
  hhmmss, \
  nstclust, \
  x_core_geo1, \
  y_core_geo1, \
  theta, \
  phi, \
  chi2_geo1, \
  ndof_geo1, \
  energy_ldf, \
  energy_ldf_log, \
  chi2_ldf, \
  ndof_ldf, \
  chi2_gldf, \
  ndof_gldf ]

# File name header
fHeader = sys.argv[2].split(".")[0]

#drawDist(Evts)
print 'total # of events are', len(Evts[0])
#plt.show()
#plt.savefig("%s.ALL.pdf" % fHeader)

# Quality Cut
# QC1: Chi2 < 1.e6 (meaningful chi2)
QC01_Evts = QC(Evts, 'chi2_geo1', 'GE', 1.e6)
QC01_Evts = QC(Evts, 'chi2_gldf', 'GE', 1.e6)
QC1_Evts = QC(QC01_Evts, 'chi2_ldf', 'GE', 1.e6)

#drawDist(QC1_Evts)
print 'total # of events are', len(QC1_Evts[0])
#PO(QC1_Evts, 'energy_ldf', 'GT', 57)
#plt.show()
#plt.savefig("%s.REC.png" % fHeader)

# QC2: energy > 10 >= 0
QC2_Evts = QC(QC1_Evts, 'energy_ldf', 'LT', 10)
#drawDist(QC2_Evts)
print 'total # of events are', len(QC2_Evts[0])
#PO(QC2_Evts, 'energy_ldf', 'GT', 10)
#plt.show()
#plt.savefig("%s.EnGT10.png" % fHeader)

# QC3: energy > 10 >= 0
#QC3_Evts = QC(QC2_Evts, 'energy_ldf', 'LT', 20)
#drawDist(QC3_Evts)
#print 'total # of events are', len(QC3_Evts[0])
#PO(QC2_Evts, 'energy_ldf', 'GT', 10)
#plt.show()
#plt.savefig("%s.EnGT20.png" % fHeader)

# QC4: nstclust > 3
QC3_Evts = QC(QC2_Evts, 'nstclust', 'LT', 4)
#drawDist(QC3_Evts)
#plt.show()
print 'total # of events are', len(QC3_Evts[0])
#plt.savefig("%s.EnGT10.NstGT3.png" % fHeader)
QC3_Evts = QC(QC3_Evts, 'energy_ldf', 'LT', 57)
QC3_Evts = QC(QC3_Evts, 'theta', 'GT', 55)
plotRaDecMap(QC3_Evts, ax, 'r', 'SN')


lines = open(sys.argv[3], 'r').readlines()

# Printed out from EvtTxt files are
#yymmdd, hhmmss, usec, nstclust, t0_geo1, dt0_geo1, xcore_geo1, dxcore_geo1, ycore_geo1, dycore_geo1, theta_geo1, dtheta_geo1, phi_geo1, dphi_geo1, chi2_geo1, ndof_geo1, energy_ldf, chi2_ldf, ndof_ldf


yymmdd = []
hhmmss = []
nstclust = []
x_core_geo1 = []
y_core_geo1 = []
theta = []
phi = []
chi2_geo1 = []
ndof_geo1 = []
chi2_ldf = []
ndof_ldf = []
energy_ldf = []
energy_ldf_log = []
energy_gldf = []
chi2_gldf = []
ndof_gldf = []

# Add every events triggered
#print "Events with Energy > 57"
for line in lines:
  #print line.strip('\n')
  evt = line.strip('\n').split()
  #print evt
  yymmdd.append(evt[0])
  hhmmss.append(evt[1])
  nstclust.append(int(evt[3]))
  x_core_geo1.append(float(evt[6]))
  y_core_geo1.append(float(evt[8]))
  theta.append(float(evt[10]))
  phi.append((180 + float(evt[12])) % 360)
  chi2_geo1.append(float(evt[14]))
  ndof_geo1.append(int(evt[15]))
  energy_ldf.append(float(evt[16]) * enscale)
  energy_ldf_log.append(float(np.log10(float(evt[16]) * enscale)))
  chi2_ldf.append(float(evt[17]))
  ndof_ldf.append(float(evt[18]))
  energy_gldf.append(float(evt[19]) * enscale)
  chi2_gldf.append(float(evt[20]))
  ndof_gldf.append(float(evt[21]))
  #if energy_ldf[-1] > 57: print yymmdd[-1], hhmmss[-1]

Evts = [\
  yymmdd, \
  hhmmss, \
  nstclust, \
  x_core_geo1, \
  y_core_geo1, \
  theta, \
  phi, \
  chi2_geo1, \
  ndof_geo1, \
  energy_ldf, \
  energy_ldf_log, \
  chi2_ldf, \
  ndof_ldf, \
  chi2_gldf, \
  ndof_gldf ]

# File name header
fHeader = sys.argv[3].split(".")[0]

#drawDist(Evts)
print 'total # of events are', len(Evts[0])
#plt.show()
#plt.savefig("%s.ALL.pdf" % fHeader)

# Quality Cut
# QC1: Chi2 < 1.e6 (meaningful chi2)
QC01_Evts = QC(Evts, 'chi2_geo1', 'GE', 1.e6)
QC01_Evts = QC(Evts, 'chi2_gldf', 'GE', 1.e6)
QC1_Evts = QC(QC01_Evts, 'chi2_ldf', 'GE', 1.e6)

#drawDist(QC1_Evts)
print 'total # of events are', len(QC1_Evts[0])
#PO(QC1_Evts, 'energy_ldf', 'GT', 57)
#plt.show()
#plt.savefig("%s.REC.png" % fHeader)

# QC2: energy > 10 >= 0
QC2_Evts = QC(QC1_Evts, 'energy_ldf', 'LT', 10)
#drawDist(QC2_Evts)
print 'total # of events are', len(QC2_Evts[0])
#PO(QC2_Evts, 'energy_ldf', 'GT', 10)
#plt.show()
#plt.savefig("%s.EnGT10.png" % fHeader)

# QC3: energy > 10 >= 0
#QC3_Evts = QC(QC2_Evts, 'energy_ldf', 'LT', 20)
#drawDist(QC3_Evts)
#print 'total # of events are', len(QC3_Evts[0])
#PO(QC2_Evts, 'energy_ldf', 'GT', 10)
#plt.show()
#plt.savefig("%s.EnGT20.png" % fHeader)

# QC4: nstclust > 3
QC3_Evts = QC(QC2_Evts, 'nstclust', 'LT', 4)
#drawDist(QC3_Evts)
#plt.show()
print 'total # of events are', len(QC3_Evts[0])
#plt.savefig("%s.EnGT10.NstGT3.png" % fHeader)
QC3_Evts = QC(QC3_Evts, 'energy_ldf', 'LT', 57)
QC3_Evts = QC(QC3_Evts, 'theta', 'GT', 55)
plotRaDecMap(QC3_Evts, ax, 'b', 'BF')

# QC3: ndof > 0
#QC3_Evts = QC(QC2_Evts, 'nstclust', 'LT', 4)
#drawDist(QC3_Evts)
#print 'total # of events are', len(QC3_Evts[0])
#PO(QC2_Evts, 'energy_ldf', 'GT', 57, output = poFile)
#plt.show()
#plt.savefig("%s.EnGT57.NsdGE4.pdf" % fHeader) 


plt.legend()
#plt.savefig("SKYMAP.png")
plt.show()
