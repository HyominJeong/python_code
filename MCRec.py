from RecResultFunc import *
import glob
import sys, os

EvtDict, DataStrt = ReadDicStructure()
SDORIGINCLF = np.array([-12.2435, -16.4406])
EvtFiles = glob.glob("%s/*.txt" % sys.argv[1])

enscale = 1./1.27
nof = len(EvtFiles)
iof = 0
percent = 0
for EvtFile in EvtFiles:
  EvtDict = FillDicFromTXT(EvtDict, DataStrt, EvtFile)
  iof += 1
  if (1. * iof / nof * 100) > percent:
    print("%d percent, %d files read" % (percent, iof))
    percent += 1

# Check in SD area or not
SDIDLine = SDedgeIDs()
edgeSDCLF = LineSDIDtoCLF(SDIDLine).T[:2].T

fig, ax = plt.subplots(1,2, figsize = (8, 4))

# ax[0], all events
plotLoop(edgeSDCLF * 1.2, ax[0])
xcore_MC = (np.array(EvtDict['xcore_MC'], dtype=np.float) - 12.2435) * 1.2
ycore_MC = (np.array(EvtDict['ycore_MC'], dtype=np.float) - 16.4406) * 1.2

ax[0].scatter(xcore_MC, ycore_MC)

plotLoop(edgeSDCLF * 1.2, ax[1])
EvtDict['inDetArea'] = []

# add inDetArea key
for i in range(len(EvtDict[EvtDict.keys()[0]])):
  EvtDict['inDetArea'].append(inLoop([float(EvtDict['xcore_MC'][i]) - 12.2435, float(EvtDict['ycore_MC'][i])- 16.4406], edgeSDCLF))

inDetArea = np.array(EvtDict['inDetArea'])
# Quality cut for outside of detection area
EvtDict = QC(EvtDict, 'inDetArea', 'EQ', 1)
xcore_MC = (np.array(EvtDict['xcore_MC'], dtype=np.float) - 12.2435) * 1.2
ycore_MC = (np.array(EvtDict['ycore_MC'], dtype=np.float) - 16.4406) * 1.2

ax[1].scatter(xcore_MC, ycore_MC)

#plt.show()

fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(10,15))

# Trigger Efficiency
log10Ebin = np.arange(-2, 4, 0.20)
energy_GLDF = np.array(EvtDict['energy_GLDF'], dtype=np.float) * enscale
energy_MC = np.array(EvtDict['energy_MC'], dtype=np.float)
sc_GLDF = np.array(EvtDict['sc_GLDF'], dtype = np.float)
dsc_GLDF = np.array(EvtDict['dsc_GLDF'], dtype = np.float)


nOfThrHist = np.histogram(np.log10(energy_MC), bins = log10Ebin)
nOfRecHist = np.histogram(np.log10(energy_MC[energy_GLDF > 0]), bins = log10Ebin)

# Rec Fine means dsc/sc < 0.5 & sc, dsc > 0
energy_MCFine = energy_MC[sc_GLDF > 0]
energy_GLDFFine = energy_GLDF[sc_GLDF > 0]
nOfRecFineHist = np.histogram(np.log10(energy_MCFine[dsc_GLDF[dsc_GLDF > 0] / sc_GLDF[sc_GLDF > 0] < 0.5]), bins = log10Ebin)

plotNpHist(nOfThrHist, ax1, 'black', lab='Thr')
plotNpHist(nOfRecHist, ax1, 'blue', lab = 'GLDF')
plotNpHist(nOfRecFineHist, ax1, 'red', lab = 'dsc cut')
ax1.legend()


effGLDF = 1. * nOfRecHist[0] / (nOfThrHist[0] - 1.e-6)
effGLDFFine = 1. * nOfRecFineHist[0] / (nOfThrHist[0] - 1.e-6)
#print 0.5 * (log10Ebin[:-1] + log10Ebin[1:]), effGLDF
ax2.plot(0.5 * (log10Ebin[:-1] + log10Ebin[1:]), effGLDF, color='blue', label = 'GLDF')
ax2.plot(0.5 * (log10Ebin[:-1] + log10Ebin[1:]), effGLDFFine, color='red', label = 'dsc cut')
ax2.legend()

# ax3, ax4 for energy resolution
# ax5, ax6 for openal angle resolution
# log10(E/EeV) > 1.0
# log10(E/EeV) > 1.5
# log10(E/EeV) > 2.0

eThs = [1.0, 1.5, 2.0]
eThsCol = ['black', 'blue', 'red']

for eTh in eThs:

  # Energy Resolution

  tmpEvtDict = QC(EvtDict, 'energy_MC', 'GT', eTh)

  energy_MC = np.array(tmpEvtDict['energy_MC'], dtype = np.float)
  energy_GLDF = np.array(tmpEvtDict['energy_GLDF'], dtype=np.float) * enscale
  sc_GLDF = np.array(tmpEvtDict['sc_GLDF'], dtype = np.float)
  dsc_GLDF = np.array(tmpEvtDict['dsc_GLDF'], dtype = np.float)
  energy_MCFine = energy_MC[sc_GLDF > 0]
  energy_GLDFFine = energy_GLDF[sc_GLDF > 0]

  eRes_GLDF = (energy_GLDF[energy_GLDF > 0] - energy_MC[energy_GLDF > 0]) / (energy_MC[energy_GLDF > 0] + 1.e-6)
  eRes_GLDFFine = (energy_GLDFFine[dsc_GLDF[dsc_GLDF > 0] / sc_GLDF[sc_GLDF > 0] < 0.5] - \
                   energy_MCFine[dsc_GLDF[dsc_GLDF > 0] / sc_GLDF[sc_GLDF > 0] < 0.5])\
                    / (energy_MCFine[dsc_GLDF[dsc_GLDF > 0] / sc_GLDF[sc_GLDF > 0] < 0.5] + 1.e-6)

  eRes_GLDFHist = np.histogram(eRes_GLDF, bins = np.arange(-2, 2, 0.2))
  eRes_GLDFFineHist = np.histogram(eRes_GLDFFine, bins = np.arange(-2, 2, 0.2))

  print "Energy Resolution is", np.mean(eRes_GLDF), '+/-', np.std(eRes_GLDF)
  print "Energy Resolution w/ QC is", np.mean(eRes_GLDFFine), '+/-', np.std(eRes_GLDFFine)


  plotNpHist(eRes_GLDFHist, ax3, col = eThsCol[eThs.index(eTh)], lab=("logE > %.2f" % eTh))
  plotNpHist(eRes_GLDFFineHist, ax4, col = eThsCol[eThs.index(eTh)], lab=("logE > %.2f w/ QC" % eTh))

  ax3.legend()
  ax4.legend()

  # Openal angle
  tmpEvtDict = QC(EvtDict, 'energy_GLDF', 'GT', 0) # reconstructed only
  theta_MC = np.array(tmpEvtDict['theta_MC'], dtype = np.float) # MC theta in radian
  phi_MC = np.array(tmpEvtDict['phi_MC'], dtype = np.float) # MC phi in radian

  theta_GLDF = np.deg2rad(np.array(tmpEvtDict['theta_GLDF'], dtype = np.float)) # GLDF theta in radian
  phi_GLDF = np.deg2rad(np.array(tmpEvtDict['phi_GLDF'], dtype = np.float)) # GLDF phi in radian
  sc_GLDF = np.array(tmpEvtDict['sc_GLDF'], dtype = np.float)
  dsc_GLDF = np.array(tmpEvtDict['dsc_GLDF'], dtype = np.float)

  ds2 = np.power((np.sin(theta_MC) * np.cos(phi_MC) - np.sin(theta_GLDF) * np.cos(phi_GLDF)),2) + \
       np.power((np.sin(theta_MC) * np.sin(phi_MC) - np.sin(theta_GLDF) * np.sin(phi_GLDF)),2) + \
       np.power((np.cos(theta_MC) - np.cos(theta_GLDF)),2)

  for ind in range(len(ds2)):
    print theta_MC[ind], phi_MC[ind], theta_GLDF[ind], phi_GLDF[ind], ds2[ind]

  opAn = np.arccos(1 - 0.5 * ds2)
  opAnFine = opAn[dsc_GLDF / sc_GLDF < 0.5]

  opAnHist = np.histogram(opAn)
  opAnFineHist = np.histogram(opAnFine)
  plotNpHist(opAnHist, ax5, col = eThsCol[eThs.index(eTh)], lab=("logE > %.2f w/ QC" % eTh))
  plotNpHist(opAnFineHist, ax6, col = eThsCol[eThs.index(eTh)], lab=("logE > %.2f w/ QC" % eTh))

  print "Openal angle is", np.mean(opAn), '+/-', np.std(opAn)
  print "Openal angle is w/ QC is ", np.mean(opAnFine), '+/-', np.std(opAnFine)


  ax5.legend()
  ax6.legend()

plt.show()

#Energy resolution

