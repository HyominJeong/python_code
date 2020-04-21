import matplotlib.pyplot as plt
import os, sys
import numpy as np
import glob
from RecResultFunc import *

# Energy scale factor, from hybrid events with FD
enscale = 1.0 / 1.27

if len(sys.argv) != 3:
  print "Usage:"
  print "python RecResult.py Evtlist.rec"


lines = []

lines = open(sys.argv[1], 'r').readlines()

# Printed out from EvtTxt files are
# yymmdd, hhmmss, usec, nstclust, 
# t0_geo1, dt0_geo1, xcore_geo1, dxcore_geo1, ycore_geo1, dycore_geo1, theta_geo1, dtheta_geo1, phi_geo1, dphi_geo1, chi2_geo1, ndof_geo1, 
# energy_ldf, chi2_ldf, ndof_ldf,
# energy_gldf, chi2_gldf, ndof_gldf, \
# xcore_MC, ycore_MC, zcore_MC, t0_MC, energy_MC

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
xcore_MC = []
ycore_MC = []
energy_MC = []
theta_MC = []
phi_MC = []

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
  phi.append((float(evt[12])) % 360)
  chi2_geo1.append(float(evt[14]))
  ndof_geo1.append(int(evt[15]))
  energy_ldf.append(float(evt[16]) * enscale)
  energy_ldf_log.append(float(np.log10(float(evt[16]) * enscale)))
  chi2_ldf.append(float(evt[17]))
  ndof_ldf.append(float(evt[18]))
  energy_gldf.append(float(evt[19]) * enscale)
  chi2_gldf.append(float(evt[20]))
  ndof_gldf.append(float(evt[21]))
  xcore_MC.append(float(evt[22]))
  ycore_MC.append(float(evt[23])) # Need to check!
  energy_MC.append(float(evt[25])) # Need to check!
  theta_MC.append(np.rad2deg(float(evt[26])))
  phi_MC.append(np.rad2deg(float(evt[27]))%360)
  #if energy_ldf[-1] > 57: print yymmdd[-1], hhmmss[-1]

# convertarray to np hist
theta_hist = np.histogram(theta, bins=10, range=(0, 90))
phi_hist = np.histogram(phi, bins=10, range=(0, 360))
energy_ldf_log_hist = np.histogram(energy_ldf_log, bins=10, range=(-1.5, 3.5))

#print "THETA histogram \n", theta_hist
#print "PHI histogram \n", phi_hist
#print "ENERGY_LOG10 histogram \n", energy_ldf_log_hist

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
  ndof_gldf, \
  xcore_MC, \
  ycore_MC, \
  energy_MC, \
  theta_MC, \
  phi_MC ]

# File name header
fHeader = sys.argv[1].split(".")[0]

if len(sys.argv) >2:
  poFile = open(sys.argv[2], 'w')
else:
  poFile = 'output.txt'


# Canvas for theta dist & trig. eff.
fig, (ax1, ax2) = plt.subplots(2)

# QC0, only energy 10 EeV < E < 50 EeV
Evts = QC(Evts, 'energy_MC', 'GT', 50)
print("Number of Events is %d" % len(Evts[0]))
#Evts = QC(Evts, 'nstclust', 'GT', 3)
#print("Number of Events is %d" % len(Evts))

theta_thr = np.histogram(Evts[18], bins = np.arange(0, 61, 10))
plotNpHist(theta_thr, ax1, col='black', lab='Thr')

# Quality Cut - reconstructed
# QC1: Chi2 < 1.e6 (meaningful chi2) and Chi2 > 0
Evts = QC(Evts, 'chi2_geo1', 'GE', 1.e6)
Evts = QC(Evts, 'chi2_gldf', 'GE', 1.e6)
Evts = QC(Evts, 'chi2_ldf', 'GE', 1.e6)

QC01_Evts = QC(Evts, 'chi2_geo1', 'LE', 0)
QC02_Evts = QC(QC01_Evts, 'chi2_gldf', 'LE', 0)
QC1_Evts = QC(QC02_Evts, 'chi2_ldf', 'LE', 0)

print("Number of Events is %d" % len(QC1_Evts[0]))

theta_rec = np.histogram(QC1_Evts[18], bins = np.arange(0, 61, 10))
plotNpHist(theta_rec, ax1, col='red', lab='Rec')
theta_rec_cal = np.histogram(QC1_Evts[5], bins = np.arange(0, 61, 10))
plotNpHist(theta_rec_cal, ax1, col='blue', lab='Rec, cal')

ax2.plot(0.5 * (theta_rec[1][1:] + theta_rec[1][:-1]),1. * theta_rec[0] / theta_thr[0])
ax1.legend()
plt.show()
