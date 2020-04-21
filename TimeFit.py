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
  ndof          = evtInfo[17]

  print evtInfo
  inlines = infile.readlines()
  print inlines
  xx = []
  yy = []
  isgood = []
  reltime_upper = []
  reltime_lower = []
  VEM_upper = []
  VEM_lower = []
  xyzclf = []
  


  for inline in inlines:
    if (st == 'all'):
      evt = inline.split()
      if (int(evt[1]) >= 1) and (int(evt[1]) <= 4):
        print evt
        xx.append(int(evt[0][:2]))
        yy.append(int(evt[0][2:]))
        isgood.append(int(evt[1]))
        reltime_upper.append(float(evt[2]))
        reltime_lower.append(float(evt[3]))
        VEM_upper.append(float(evt[4]))
        VEM_lower.append(float(evt[5]))
        xyzclf.append([float(evt[6]), float(evt[7]), float(evt[8])])
    else:
      evt = inline.split()
      if (int(evt[1]) >= 3) and (int(evt[1]) <= 4):
        print evt
        xx.append(int(evt[0][:2]))
        yy.append(int(evt[0][2:]))
        isgood.append(int(evt[1]))
        reltime_upper.append(float(evt[2]))
        reltime_lower.append(float(evt[3]))
        VEM_upper.append(float(evt[4]))
        VEM_lower.append(float(evt[5]))
        xyzclf.append([float(evt[6]), float(evt[7]), float(evt[8])])

    #print xx, yy, status

  xx = np.array(xx)
  yy = np.array(yy)
  isgood = np.array(isgood)
  reltime_upper = np.array(reltime_upper)
  reltime_lower = np.array(reltime_lower)
  VEM_upper = np.array(VEM_upper)
  VEM_lower = np.array(VEM_lower)

  reltime = 0.5 * (reltime_upper + reltime_lower)
  VEM = 0.5 * (VEM_upper + VEM_lower)
  xyzclf = np.array(xyzclf)

  '''
  # Set Canvas
  fig = plt.figure()
  ax = fig.gca()

  ## set X, Y ranges
  x_range = np.arange(int(np.mean(xx))-7,int(np.mean(xx))+7, 1)
  y_range = np.arange(int(np.mean(yy))-7,int(np.mean(yy))+7, 1)
  ax.set_xticks(x_range)
  ax.set_yticks(y_range)
  ax.set_xlim([x_range[0], x_range[-1]])
  ax.set_ylim([y_range[0], y_range[-1]])
  ax.set_xlabel('X position ID [2.08 km]')
  ax.set_ylabel('Y position iD [2.08 km]')

  plt.grid()

  plt.scatter(xx, yy, s=np.sqrt(VEM)*500, c=reltime*4, edgecolors = 'w')
  cbar = plt.colorbar()


  #plt.scatter(xcore, ycore, s=100, marker='*')

  cbar.set_label('relative time [us]', rotation=270)

  props = dict(boxstyle='round', facecolor='None', alpha=0.5, edgecolor='blue')

  ax.text(x_range[1]-0.4, y_range[1]-0.4, '\n\n      1VEM size', fontsize=12, va = 'bottom', bbox=props)
  plt.scatter(x_range[1], y_range[1], s=np.sqrt(1)*500, c='w')

  props_time = dict(boxstyle='round', facecolor='None', alpha=1, edgecolor='black')
  ax.text(x_range[1], y_range[-2], ("%s %s.%s" % (yymmdd, hhmmss, usec)), fontsize=12, bbox=props_time)

  #plt.show()
  figName = ("%s.%s.%s.%s.pdf" % (yymmdd, hhmmss, usec, st))
  print figName
  plt.savefig(figName)

  #break
  '''
  #define SD_ORIGIN_X_CLF -12.2435
  #define SD_ORIGIN_Y_CLF -16.4406

  SD_ORIGIN_X_CLF = -12.2435
  SD_ORIGIN_Y_CLF = -16.4406
  SD_ORIGIN = np.array([SD_ORIGIN_X_CLF, SD_ORIGIN_Y_CLF, 0.])

  s = []
  dotp_ = []
  showerDirection = np.array([np.sin(np.deg2rad(theta)) * np.cos(np.deg2rad(phi)),\
  			    np.sin(np.deg2rad(theta)) * np.sin(np.deg2rad(phi)),\
  			    np.cos(np.deg2rad(theta)) ])
  corePosition = np.array([float(xcore), float(ycore), 0.] )
  print (corePosition + SD_ORIGIN)
  for xyzclf_ in xyzclf:
    d = xyzclf_ - corePosition - SD_ORIGIN
    #print d
    dotp = np.dot(d, showerDirection)
    #s.append(np.sqrt(np.dot(np.dot(d, showerDirection), np.dot(d, showerDirection))))
    s.append(np.sqrt(np.dot(d, d) - dotp * dotp) * 1.2) # s in km
    #tau.append((reltime - dotp) * 4.) # tau in us
    dotp_.append(dotp)

  #print s
  s = np.array(s)
  rho = np.array(VEM) / 3.0
  drho = 0.53 * np.sqrt(2.0 * rho + np.power(0.15 * rho,2))

  #print s, rho

  # Plot LDF and Timing fit

  #fig = plt.figure()
  #ax = fig.gca()
  fig = plt.figure(figsize = (12, 5))
  #fig.suptitle('%s %s.%s' % (yymmdd, hhmmss, usec), fontsize = 18)


  # Draw LDF on the left subplot
  ax1 = fig.add_subplot(1,2,1)

  
  ax1.set_xscale('log')
  ax1.set_yscale('log')
  ax1.set_xlim([0.1, 20])
  ax1.set_xlabel('Lateral distance [km]')
  ax1.set_ylabel('Rho [VEM/m^2]')
  ax1.set_title('Lateral Distribution Fit') 

  LD = ax1.errorbar(s, rho, drho, fmt='o', color='black')


  # Draw fit function
  fit_x = np.linspace(0.1, 20, 50)
  fit_y = ldf(fit_x, theta) * float(sc)
  fit_y_pe = ldf(fit_x, theta) * (float(sc) + float(dsc))
  fit_y_me = ldf(fit_x, theta) * (float(sc) - float(dsc))

  LDFfit = ax1.plot(fit_x, fit_y, color='red')
  LDFfit_pe = ax1.plot(fit_x,fit_y_pe, 'r--')
  LDFfit_me = ax1.plot(fit_x,fit_y_me, 'r--')

  props = dict(boxstyle='round', facecolor='None', alpha=0.5, edgecolor='blue')

  ax1.text(0.05, 0.05, "sc  = %9s\ndsc = %9s" % (sc, dsc), fontsize=12, ha = 'left', va = 'bottom', transform = ax1.transAxes, bbox=props)

  #plt.show()
  #figName = ("%s.%s.%s.%s.LDF.pdf" % (yymmdd, hhmmss, usec, st))
  #print figName, "is saved."
  #plt.savefig(figName)
  

  ax2 = fig.add_subplot(1,2,2)
  #par = np.array(theta, phi, xcore, ycore, float(t0), sc)

  #tau = 4. * (reltime - tvsx_plane() - float(t0))
  #print xyzclf[:,2]
  print 'reltime, dotp, t0, z cos(theta)'
  print reltime, dotp_, float(t0), xyzclf[:,2] * np.cos(np.deg2rad(theta))
  tau = 4. * (reltime - dotp_ - float(t0) + xyzclf[:,2] * np.cos(np.deg2rad(theta))) # in us
  #td_exp, ts_exp = ltdts(rho, s, theta)
  print 's[km] and taw[us] of data'
  print s
  print tau
  tauErrorbar = ax2.errorbar(s, tau, 0.02, fmt='.', color='black')

  fit_s = np.arange(0.1, 5, 0.1)
  fit_rho = ldf(fit_s, theta) * float(sc)
  fit_td, fit_ts = ltdts(fit_rho, fit_s, theta)
  # Convert td, ts to us
  fit_td = fit_td / 1.e3
  fit_ts = fit_ts / 1.e3
  #print fit_td
  TimeFit = ax2.plot(fit_s, fit_td, 'r-')
  TimeFit_err1 = ax2.plot(fit_s, fit_td + fit_ts, 'r--')
  TimeFit_err2 = ax2.plot(fit_s, fit_td - fit_ts, 'r--')

  # Plot ltd, lts used on fitting
  #print rho, s
  #ltd, lts = ltdts(rho[0], s[0], theta) / 1.e3
  #ltd, lts = ltdts(rho, s, theta)
  #ltd = ltd / 1.e3
  #lts = lts / 1.e3
  #LtfErrorbar = ax2.errorbar(s, ltd, lts, fmt='^', color='blue')

  ax2.set_title('Timing Fit')
  ax2.set_xlabel('Lateral distance [km]')
  ax2.set_ylabel('tau [us]')
  
  props = dict(boxstyle='round', facecolor='None', alpha=0.5, edgecolor='blue')

  ax2.text(0.05, 0.95, \
    "Energy = %s\nChi2/ndof = %5.2f/%s\nTheta = %f\nPhi = %f" % \
    (energy, float(chi2), ndof, theta, phi), \
    fontsize=12, ha = 'left', va = 'top', transform = ax2.transAxes, bbox=props)
  #plt.text(0.1, 0.9, "TEST")


  fig.suptitle('%s %s.%s' % (yymmdd, hhmmss, usec), fontsize = 18)

  #plt.show()
  figName = ("%s.%s.%s.Fit.pdf" % (yymmdd, hhmmss, usec))
  print figName, "is saved."
  plt.savefig(figName)


  #break
