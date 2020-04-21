import numpy as np
import matplotlib.pyplot as plt
import os, sys

import func


# Read txt file to array
evtData = np.loadtxt(sys.argv[1], dtype=np.str)

#print evtData[0][0], evtData[0][1]
#print evtData[:,0][:5]


# Set threshold of good events
ThrTheta = 5	# 5 deg
ThrPhi = 5	# 5 deg
ThrEnergy = 0.5 # ABS(RecEnergy - FDEnergy)/FDEnergy


evtDate = evtData[:,0]
evtTime = evtData[:,1]
evtTheta = evtData[:,5]
evtPhi = evtData[:,6]
evtEnergy = evtData[:,9]

evtFound = np.zeros(len(evtDate), dtype=np.int)
evtDTheta = np.zeros(len(evtDate), dtype=np.float)
evtDPhi = np.zeros(len(evtDate), dtype=np.float)
evtDEnergy = np.zeros(len(evtDate), dtype=np.float)


#with open(sys.argv[2], 'r') as lines:
for i in range(len(evtDate)):
	with open(sys.argv[2], 'r') as lines:
		for line in lines:
			recEvt = line[4:].replace('\n','').replace(' ','').split(',')

			#print recEvt#, evtDate[i]
			if recEvt[0] == evtDate[i]:

				#print recEvt[1].split('.'), evtTime[i].split('.')
				if recEvt[1].split('.')[0] == evtTime[i].split('.')[0]:
					print recEvt,'\n', evtData[i]
					evtFound[i] = 1
					evtDTheta[i] = abs(float(recEvt[5]) - float(evtTheta[i]))
					evtDPhi[i] = abs(float(recEvt[6]) - float(evtPhi[i]))
					evtDEnergy[i] = abs(float(recEvt[9]) - float(evtEnergy[i]))

					if (evtDTheta[i] > ThrTheta) or (evtDPhi[i] > ThrPhi):
						evtFound[i] = 1
						print evtDTheta[i], evtDPhi[i]
					if (evtDEnergy[i] / float(evtEnergy[i]) > ThrEnergy):
						evtFound[i] = 1
						print recEvt[9], evtEnergy[i], evtDEnergy[i] / float(evtEnergy[i])
					break
			evtFound[i] = 0


print np.sum(evtFound)

nOfDataUnder100 = 0
nOfDataOver100 = 0
nOfRecUnder100 = 0
nOfRecOver100 = 0

ErrThetaU100 = 0
ErrPhiU100 = 0
ErrEnergyU100 = 0

ErrThetaO100 = 0
ErrPhiO100 = 0
ErrEnergyO100 = 0



# Calculate Efficiency
for i in range(len(evtDate)):
	#print evtEnergy[i]
	if float(evtEnergy[i]) < 50:
		nOfDataUnder100 += 1
		if evtFound[i] == 1:
			nOfRecUnder100 += 1
			ErrThetaU100 += evtDTheta[i] ** 2
			ErrPhiU100 += evtDPhi[i] ** 2
			ErrEnergyU100 += evtDEnergy[i]


	else:
		nOfDataOver100 += 1
		if evtFound[i] == 1:
			nOfRecOver100 += 1
			ErrThetaO100 += evtDTheta[i] ** 2
			ErrPhiO100 += evtDPhi[i] ** 2
			ErrEnergyO100 += evtDEnergy[i]

ErrThetaU100 = np.sqrt(ErrThetaU100 / nOfRecUnder100)
ErrPhiU100 = np.sqrt(ErrPhiU100 / nOfRecUnder100)
ErrEnergyU100 = ErrEnergyU100 / nOfRecUnder100

ErrThetaO100 = np.sqrt(ErrThetaO100 / nOfRecOver100)
ErrPhiO100 = np.sqrt(ErrPhiO100 / nOfRecOver100)
ErrEnergyO100 = ErrEnergyO100 / nOfRecOver100

print nOfDataUnder100, type(nOfDataUnder100)

print "For Energy < 50"
print "Efficiency is %.3f" % ((1. * nOfRecUnder100) / nOfDataUnder100)
print "Error of thetas and phis are", ErrThetaU100, ErrPhiU100
print "Error of Energy is %.3f percent" % (ErrEnergyU100 / 100)
print "The number of data from FD is", nOfDataUnder100

print "For Energy > 50"
print "Efficiency is %.3f" % ((1. * nOfRecOver100 / nOfDataOver100))
print "Error of thetas and phis are", ErrThetaO100, ErrPhiO100
print "Error of Energy is %.3f percent" % (ErrEnergyO100 / 100)
print "The number of data from FD is", nOfDataOver100






