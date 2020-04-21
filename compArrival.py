import numpy as np
from matplotlib import pyplot as plt
import sys, os

def drawHist(hist, bin_center, label, canvas):
  return

def setCanvas(canvas, title):
  canvas.set_title(title)
  canvas.set_xlabel('\Delta\Omega')
  canvas.set_ylabel('N of Evt')

# Select events with energy, nst condition
def extEvt(Energy, Nst, Evt, eLow=0, eHigh=float("inf"), nstLow=0, nstHigh=float("inf")):
  if (len(Evt) == len(Energy)) and (len(Evt) == len(Nst)):
    subEvt = []
    for i in range(len(Evt)):
      if (Energy[i] >= eLow   and Energy[i] <= eHigh  ) and \
         (Nst[i]    >= nstLow and Nst[i]    <= nstHigh):
        subEvt.append(Evt[i])
        print Energy[i], Nst[i], Evt[i]
    return subEvt

  else:
    print "Wrong input. Input arrays should have same length"
    return 0

evtFile = open(sys.argv[1])

evtLines = evtFile.readlines()

MC_theta = []
MC_phi = []
Rec_plane_theta = []
Rec_plane_phi = []
Rec_linsley_theta = []
Rec_linsley_phi = []
Rec_linsley1_theta = []
Rec_linsley1_phi = []
Energy_thrown = []
NstClust = []

for line in evtLines:
  evt = line.strip('\n').split()
  #print evt
  if evt[0] == 'MC_Thr':
    #print "MC_Thrown"
    MC_theta.append(float(evt[5]))
    MC_phi.append(float(evt[6]))
    Energy_thrown.append(float(evt[2]))
    NstClust.append(float(evt[7]))

  if evt[0] == 'REC[0]' :
    Rec_plane_theta.append(float(evt[5]))
    Rec_plane_phi.append(float(evt[6]))
    #Energy_thrown.append(float(evt[2]))
    #NstClust.append(float(evt[7])

  if evt[0] == 'REC[1]' :
    Rec_linsley_theta.append(float(evt[5]))
    Rec_linsley_phi.append(float(evt[6]))
    #Energy_thrown.append(float(evt[2]))
    #NstClust.append(float(evt[7])

  if evt[0] == 'REC[2]' :
    Rec_linsley1_theta.append(float(evt[5]))
    Rec_linsley1_phi.append(float(evt[6]))
    #Energy_thrown.append(float(evt[2]))
    #NstClust.append(float(evt[7])

MC_theta		= np.array(MC_theta)
MC_phi			= np.array(MC_phi)

Rec_plane_theta		= np.array(Rec_plane_theta)
Rec_plane_phi		= np.array(Rec_plane_phi)

Rec_linsley_theta	= np.array(Rec_linsley_theta)
Rec_linsley_phi		= np.array(Rec_linsley_phi)

Rec_linsley1_theta	= np.array(Rec_linsley1_theta)
Rec_linsley1_phi	= np.array(Rec_linsley1_phi)


Delta_plane = np.sqrt(\
	np.power(MC_theta - Rec_plane_theta,2) + \
	np.power(MC_phi - Rec_plane_phi,2))

Delta_linsley = np.sqrt(\
        np.power(MC_theta - Rec_linsley_theta, 2) + \
        np.power(MC_phi - Rec_linsley_phi, 2))

#plt.hist(Delta_plane)
#plt.show()

# Set canvas
fig = plt.figure(figsize = (15,5))

# Canvas [Plane fit, Modified Linsley fit, Modified Linsley fit w/ cuvature]
ax_plane = fig.add_subplot(1,3,1)
setCanvas(ax_plane, 'Plane fit')

ax_plane = fig.add_subplot(1,3,2)
setCanvas(ax_plane, 'Linsley fit')

ax_plane = fig.add_subplot(1,3,3)
setCanvas(ax_plane, 'Linsley w/ curv. fit')


#plane_1 = extEvt(Energy_thrown, NstClust, Delta_plane, nstHigh=4)
#plt.hist(plane_1)

lins_1 = extEvt(Energy_thrown, NstClust, Delta_linsley, eLow = 10, nstLow = 5)
plt.hist(lins_1)


plt.show()
