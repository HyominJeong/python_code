import matplotlib.pyplot as plt
import numpy as np
import glob
import sys

infiles = glob.glob("*.txt")

# Input file is a list of
# rusdraw_.yymmdd, rusdraw_.hhmmss, rusdraw_.usec, rufldf_.xcore[1], rufldf_.dxcore[1], rufldf_.ycore[1], rufldf_.dycore[1], rufptn_.nstclust, rufldf_.theta, rufldf_.phi, rufldf_.chi2[1], rufldf_.energy[0], rufldf_.energy[1]
# rufptn_.xxyy[x], rufptn_.isgood[x], rufptn_.reltime[x][0], rufptn_.reltime[x][1], rufptn_.pulsa[x][0], rufptn_.pulsa[x][1]

# Define lateral distribution function
# s in km
# theta in degree
def ldf(s, theta):
  #Double_t r0; // Moliere radius
  #Double_t alpha; // Constant slope parameter
  #Double_t beta; // Another constant slope parameter
  #Double_t eta; // Zenith angle dependent slope parameter
  #Double_t rsc; // Scaling factor for r in quadratic term in power

  r = s * 1.e3

  r0 = 91.6
  alpha = 1.2
  beta = 0.6
  eta = 3.97-1.79*(1.0/np.cos(np.deg2rad(theta))-1.0)
  rsc = 1000.0

  return np.power(r/r0, -alpha) * np.power((1.0+r/r0), -(eta-alpha)) * np.power((1.0 + r*r/rsc/rsc), -beta)

# Define shower front curvature function
# rho: VEM/m^2
# s: in km
# theta: in degree
# td, ts in ns
def ltdts(rho, s, theta):
  if (theta < 25.0):
    a = 3.3836 - 0.01848 * theta
  elif (theta >=25.0) and (theta < 35.0):
    a = (0.6511268210e-4*(theta-.2614963683))*(theta*theta-134.7902422*theta+4558.524091)
  else:
     a = np.exp( -3.2e-2 * theta + 2.0)
  td = 0.80 * a * np.power( (1.0 + s * 1.e3 / 30.0), 1.5) * np.power(rho, -0.5)
  ts = 0.70 * a * np.power( (1.0 + s * 1.e3 / 30.0), 1.5) * np.power(rho, -0.3)
  return td, ts

# Define plane fit
#/* ARGUMENTS: x,y is counter location in counter separation units in CLF frame with respect
# * to SD origin.  z is the counter height above CLF plane (in counter separation units)
# (PARAMETERS):
# par[0] - zenith angle, degrees
# par[1] - azimuthal angle, degrees
# par[2] - x-position of the core, counter separation units
# par[3] - y-position of the core, counter separation units
# par[4] - time of the core hit, relative to earliest hit time, counter separation units
# RETURNS: time for a given position in counter separation units
# */

def tvsx_plane(x, y, z, par):
  d = np.array((x-par[2]), (y-par[3])) # vector distance from the core in xy - plane */
  #// Dot product of distance from core and shower axis vector
  dotp = np.sin(np.deg2rad(par[0]))*(cos(np.deg2rad(par[1]))*d[0] + \
	sin(np.deg2rad(par[1]))*d[1])

  return par[4]+dotp - z * cos(np.deg2rad(par[0]))
  

if int(sys.argv[1]) == 0:
  st = 'all'
else:
  st = 'st'
chi_ndof = []
for file in infiles:
  print file
  infile = open(file, 'r')

  evtInfo = infile.readline().split()
  yymmdd	= evtInfo[0]
  hhmmss	= evtInfo[1]
  usec		= evtInfo[2]
  xcore		= evtInfo[3] #-12.2435 need to convert TAx4 coordinate
  dxcore	= evtInfo[4] #-16.4406
  ycore		= evtInfo[5]
  dycore	= evtInfo[6]
  nstclust	= evtInfo[7]
  theta		= float(evtInfo[8])
  phi		= float(evtInfo[9])
  chi2		= evtInfo[10]
  
  energy	= evtInfo[12]
  sc		= evtInfo[13]
  dsc		= evtInfo[14]
  t0		= evtInfo[15]
  dt0		= evtInfo[16]
  ndof		= evtInfo[17]
  
  chi_ndof.append(float(chi2) / int(ndof))
  print chi2, ndof, float(chi2) / int(ndof)

chi_ndof = np.array(chi_ndof)
#chiNdofHist, chiNdofBin = np.hist(chi_ndof)
print "Mean: %08.4f, Std: %08.4f" % (np.mean(chi_ndof), np.std(chi_ndof))
plt.hist(chi_ndof)
plt.show()

