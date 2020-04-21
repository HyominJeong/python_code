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


lines = open(sys.argv[1], 'r').readlines()
ct = sys.argv[2]
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
t0_gldf = []
xcore_gldf = []
ycore_gldf = []
theta_gldf = []
phi_gldf = []
energy_gldf = []
chi2_gldf = []
ndof_gldf = []
sc_gldf = []
dsc_gldf = []

# Add every events triggered
#print "Events with Energy > 57"
for line in lines:
  #print line.strip('\n')
  evt = line.strip('\n').split()
  #print evt
  yymmdd.append(float(evt[0]))
  hhmmss.append(float(evt[1]))
  nstclust.append(float((evt[3])))
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
  t0_gldf.append(float(evt[19]))
  xcore_gldf.append(float(evt[20]))
  ycore_gldf.append(float(evt[21]))
  theta_gldf.append(float(evt[22]))
  phi_gldf.append(float(evt[23]))
  energy_gldf.append(float(evt[24]) * enscale)
  chi2_gldf.append(float(evt[25]))
  ndof_gldf.append(float(evt[26]))
  sc_gldf.append(float(evt[27])) # Added temporary
  dsc_gldf.append(float(evt[28])) # Added temporary
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
  t0_gldf, \
  xcore_gldf, \
  ycore_gldf, \
  theta_gldf, \
  phi_gldf, \
  energy_gldf, \
  chi2_gldf, \
  ndof_gldf, \
  sc_gldf, \
  dsc_gldf ]

# File name header
fHeader = sys.argv[1].split(".")[0]

'''
if len(sys.argv) >2:
  poFile = open(sys.argv[2], 'w')
else:
  poFile = 'output.txt'
'''

#drawDist(Evts)
print 'total # of events are', len(Evts[0])
#plt.show()
#plt.savefig("%s.ALL.pdf" % fHeader)

# Quality Cut, reconstructed only
# QC1: Chi2 < 1.e6 (meaningful chi2)
QC01_Evts = QC(Evts, 'chi2_geo1', 'GE', 1.e6)
QC01_Evts = QC(QC01_Evts, 'chi2_gldf', 'GE', 1.e6)
QC1_Evts = QC(QC01_Evts, 'chi2_ldf', 'GE', 1.e6)
print 'total # of events are', len(QC1_Evts[0])

#drawDist(QC1_Evts, ct)
#plt.savefig("%s.REC.png" % fHeader)
# QC2: nstclust > 3
#print([Evts[2])

'''
# Draw Energy dist. plot.
# [GLDF, GLDF w/ (dsc/sc) < 0.5, GLDF w/ (dsc/sc) < 0.25]
fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = plt.subplots(3, 3, figsize = (15, 15))
NpEvts = np.array(QC1_Evts, dtype=np.float)

# Reconstructed all events of GLDF
eLogHist = np.histogram(np.log10(NpEvts[18]), bins=np.arange(-2.5, 4.0, 0.2))
ax1.set_yscale('log')
ax1.set_title('GLDF Energy')
ax1.set_xlabel('log10(E/EeV)')
ax1.set_ylabel('Number of Events')
ax1.set_ylim(0.1, 100000)
plotNpHist(eLogHist, ax1)

# dsc/sc < 0.5 events of GLDF
eLogHist = np.histogram(np.log10(NpEvts[18][NpEvts[22]/(NpEvts[21] + 1.e-8) < 0.5]), bins=np.arange(-2.5, 4.0, 0.2))
ax2.set_yscale('log')
ax2.set_title('GLDF Energy')
ax2.set_xlabel('log10(E/EeV)')
ax2.set_ylabel('Number of Events')
ax2.set_ylim(0.1, 100000)
plotNpHist(eLogHist, ax2)

# dsc/sc < 0.25 events of GLDF
eLogHist = np.histogram(np.log10(NpEvts[18][NpEvts[22]/(NpEvts[21] + 1.e-8) < 0.25]), bins=np.arange(-2.5, 4.0, 0.2))
ax3.set_yscale('log')
ax3.set_title('GLDF Energy')
ax3.set_xlabel('log10(E/EeV)')
ax3.set_ylabel('Number of Events')
ax3.set_ylim(0.1, 100000)
plotNpHist(eLogHist, ax3)

# Theta < 55 cut
QC2_Evts = QC(QC1_Evts, 'theta_gldf', 'GE', 55)
NpEvts = np.array(QC1_Evts, dtype=np.float)

eLogHist = np.histogram(np.log10(NpEvts[18]), bins=np.arange(-2.5, 4.0, 0.2))
ax4.set_yscale('log')
ax4.set_title('GLDF Energy')
ax4.set_xlabel('log10(E/EeV)')
ax4.set_ylabel('Number of Events')
ax4.set_ylim(0.1, 100000)
plotNpHist(eLogHist, ax4)

# dsc/sc < 0.5 events of GLDF
eLogHist = np.histogram(np.log10(NpEvts[18][NpEvts[22]/(NpEvts[21] + 1.e-8) < 0.5]), bins=np.arange(-2.5, 4.0, 0.2))
ax5.set_yscale('log')
ax5.set_title('GLDF Energy')
ax5.set_xlabel('log10(E/EeV)')
ax5.set_ylabel('Number of Events')
ax5.set_ylim(0.1, 100000)
plotNpHist(eLogHist, ax5)

# dsc/sc < 0.25 events of GLDF
eLogHist = np.histogram(np.log10(NpEvts[18][NpEvts[22]/(NpEvts[21] + 1.e-8) < 0.25]), bins=np.arange(-2.5, 4.0, 0.2))
ax6.set_yscale('log')
ax6.set_title('GLDF Energy')
ax6.set_xlabel('log10(E/EeV)')
ax6.set_ylabel('Number of Events')
ax6.set_ylim(0.1, 100000)
plotNpHist(eLogHist, ax6)

# Nst > 3 cut
QC3_Evts = QC(QC2_Evts, 'nstclust', 'LE', 3)
NpEvts = np.array(QC1_Evts, dtype=np.float)

eLogHist = np.histogram(np.log10(NpEvts[18]), bins=np.arange(-2.5, 4.0, 0.2))
ax7.set_yscale('log')
ax7.set_title('GLDF Energy')
ax7.set_xlabel('log10(E/EeV)')
ax7.set_ylabel('Number of Events')
ax7.set_ylim(0.1, 100000)
plotNpHist(eLogHist, ax7)

# dsc/sc < 0.5 events of GLDF
eLogHist = np.histogram(np.log10(NpEvts[18][NpEvts[22]/(NpEvts[21] + 1.e-8) < 0.5]), bins=np.arange(-2.5, 4.0, 0.2))
ax8.set_yscale('log')
ax8.set_title('GLDF Energy')
ax8.set_xlabel('log10(E/EeV)')
ax8.set_ylabel('Number of Events')
ax8.set_ylim(0.1, 100000)
plotNpHist(eLogHist, ax8)

# dsc/sc < 0.25 events of GLDF
eLogHist = np.histogram(np.log10(NpEvts[18][NpEvts[22]/(NpEvts[21] + 1.e-8) < 0.25]), bins=np.arange(-2.5, 4.0, 0.2))
ax9.set_yscale('log')
ax9.set_title('GLDF Energy')
ax9.set_xlabel('log10(E/EeV)')
ax9.set_ylabel('Number of Events')
ax9.set_ylim(0.1, 100000)
plotNpHist(eLogHist, ax9)

fig.tight_layout()
plt.show()
'''
#plt.savefig("%s.EnDist.png" % fHeader)

# Only 1 figure
fig, ax = plt.subplots(1,1)
ax.set_yscale('log')
ax.set_title('GLDF Energy')
ax.set_xlabel('log10(E/EeV)')
ax.set_ylabel('Number of Events')
ax.set_ylim(0.1, 100000)

# Quality cut
QC2_Evts = QC(QC1_Evts, 'theta_gldf', 'GE', 55)
QC3_Evts = QC(QC2_Evts, 'nstclust', 'LE', 3)
NpEvts = np.array(QC1_Evts, dtype=np.float)

eLogHist = np.histogram(np.log10(NpEvts[18][NpEvts[22]/(NpEvts[21] + 1.e-8) < 0.5]), bins=np.arange(0.9, 2.9, 0.2))
plotNpHist(eLogHist, ax)
plt.show()

# Print number of events
nOfEGLDF = NpEvts[18][NpEvts[22]/(NpEvts[21] + 1.e-8) < 0.5]
Es = [50, 10, 1]
for E in Es:
  print("Over than %d EeV: %d" % (E, len(nOfEGLDF[nOfEGLDF > E])))

'''
HEEvts = NpEvts.T[NpEvts[18]>50]
for HEEvt in HEEvts:
  np.set_printoptions(suppress=True)
  for ele in HEEvt:
    print ele,
  print
'''

'''
# Draw Energy dist. plot.
# [ LDF,  LDF w/ Nsd > 3]
# [GLDF, GLDF w/ Nsd > 3]
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, figsize = (10,10))

NpEvts = np.array(QC1_Evts, dtype=np.float)
eLogHist = np.histogram(np.log10(NpEvts[9]), bins=np.arange(-2.5, 4.0, 0.5))
ax1.set_yscale('log')
ax1.set_title('LDF Energy')
ax1.set_xlabel('log10(E/EeV)')
ax1.set_ylabel('Number of Events')
ax1.set_ylim(0.1, 100000)
plotNpHist(eLogHist, ax1)


eLogHist = np.histogram(np.log10(NpEvts[9][NpEvts[2] > 3]), bins=np.arange(-2.5, 4.0, 0.5))
ax2.set_yscale('log')
ax2.set_title('LDF Energy')
ax2.set_xlabel('log10(E/EeV)')
ax2.set_ylabel('Number of Events')
ax2.set_ylim(0.1, 100000)
plotNpHist(eLogHist, ax2)

eLogHist = np.histogram(np.log10(NpEvts[18]), bins=np.arange(-2.5, 4.0, 0.5))
ax3.set_yscale('log')
ax3.set_title('GLDF Energy')
ax3.set_xlabel('log10(E/EeV)')
ax3.set_ylabel('Number of Events')
ax3.set_ylim(0.1, 100000)
plotNpHist(eLogHist, ax3)

eLogHist = np.histogram(np.log10(NpEvts[18][NpEvts[2] > 3]), bins=np.arange(-2.5, 4.0, 0.5))
ax4.set_yscale('log')
ax4.set_title('GLDF Energy')
ax4.set_xlabel('log10(E/EeV)')
ax4.set_ylabel('Number of Events')
ax4.set_ylim(0.1, 100000)
plotNpHist(eLogHist, ax4)


plt.savefig("%s.EnDist.png" % fHeader)
#plt.show()
'''
'''


QC1_Evts = QC(QC1_Evts, 'nstclust', 'LT', 4)


# Printout most energetic events
Eindex = np.argmax(QC1_Evts[18])
for i  in range(len(QC1_Evts)):
  print QC1_Evts[i][Eindex],
print

'''
'''
# QC2: energy > 10 >= 0
QC2_Evts = QC(QC1_Evts, 'energy_ldf', 'LT', 10)
drawDist(QC2_Evts, ct)
print 'total # of events are', len(QC2_Evts[0])
#PO(QC2_Evts, 'energy_ldf', 'GT', 10)
#plt.show()
plt.savefig("%s.EnGT10.png" % fHeader)

# QC3: energy > 10 >= 0
QC3_Evts = QC(QC2_Evts, 'energy_ldf', 'LT', 20)
drawDist(QC3_Evts, ct)
print 'total # of events are', len(QC3_Evts[0])
#PO(QC2_Evts, 'energy_ldf', 'GT', 10)
#plt.show()
plt.savefig("%s.EnGT20.png" % fHeader)

# QC4: nstclust > 3
QC4_Evts = QC(QC3_Evts, 'nstclust', 'LT', 4)
drawDist(QC4_Evts, ct)
#plt.show()
print 'total # of events are', len(QC3_Evts[0])
plt.savefig("%s.EnGT20.NstGT3.png" % fHeader)

# QC3: ndof > 0
#QC3_Evts = QC(QC2_Evts, 'nstclust', 'LT', 4)
#drawDist(QC3_Evts)
#print 'total # of events are', len(QC3_Evts[0])
#PO(QC2_Evts, 'energy_ldf', 'GT', 57, output = poFile)
#plt.show()
#plt.savefig("%s.EnGT57.NsdGE4.pdf" % fHeader) 

ax =  plt.subplot(111, projection="aitoff")


plot_mwd(ax)


plotRaDecMap(QC1_Evts, ax, 'k', ct )
plt.show()

'''
