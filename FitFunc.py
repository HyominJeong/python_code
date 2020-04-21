import numpy as np
import matplotlib.pyplot as plt

# Energy scale factor, should be calculated by hybrid event with FD
enscale = 1.0/1.27


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


# Alternative time delay / fluctuation function based on Linsley's but with variable
# curvature parameter and shower development factor.
# rho: VEM/m^2
# s: in km
# a
# theta: in degree
# td, ts in ns
def ltdts1(rho, s, usintheta, a, theta):
  #usintheta = s * np.tan(np.deg2rad(theta))
  #usintheta = dotp
  td = a * np.power((1.- usintheta/12), 1.05) * np.power((1 + s * 1.e3 / 30.0), 1.35) * np.power(rho, -0.5) 
  ts = 1.56 * np.power((1. - usintheta/12), 1.05) * np.power( (1 + s * 1.e3 / 30.0), 1.5) * np.power(rho, -0.3)
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

# Define function to convert from u, n, theta to s
# u: distance from shower core along the shower direction on the ground, in km
# n: distance from shower core along the perpendicular direction to u on the ground, in km
# theta: in degree, Zenith angle
# s: distance from shower core along the shower direction, in km
def un2s(u, n, theta):
  return np.sqrt(np.power(u * np.cos(np.deg2rad(theta)),2) + np.power(n,2)) 

# Function to calculate d, dotp, rho, td, ts

def geoFit(xyzclf, reltime, VEM, t0, xcore, ycore, theta, phi, sc, energy, chi2, ndof, ax, name, a = 0): 
  # Calculate core position
  SD_ORIGIN_X_CLF = -12.2435
  SD_ORIGIN_Y_CLF = -16.4406
  SD_ORIGIN = np.array([SD_ORIGIN_X_CLF, SD_ORIGIN_Y_CLF, 0.])

  s = []
  dotp = []
  u = []
  showerDirection = np.array([np.sin(np.deg2rad(theta)) * np.cos(np.deg2rad(phi)),\
                              np.sin(np.deg2rad(theta)) * np.sin(np.deg2rad(phi)),\
                              np.cos(np.deg2rad(theta)) ])
  uDirection = np.array([-np.cos(phi), -np.sin(phi), 0])

  corePosition = np.array([float(xcore), float(ycore), 0.] )
  #print "Core position,", float(xcore), float(ycore), "for", name 
  # Calculate s
  for xyzclf_ in xyzclf:
    d = xyzclf_ - corePosition - SD_ORIGIN
    dotp_ = np.dot(d, showerDirection)
    s.append(np.sqrt(np.dot(d, d) - dotp_ * dotp_) * 1.2) # s in km
    u_ = np.dot(d, uDirection)
    dotp.append(dotp_)
    u.append(u_)

  # Calculate Rho, dRho
  s = np.array(s)
  rho = np.array(VEM) / 3.0
  drho = 0.53 * np.sqrt(2.0 * rho + np.power(0.15 * rho,2))

  # Calculate tau, observed, and ts, expected
  dotp = np.array(dotp)
  tau = 4. * (reltime - dotp - float(t0) + xyzclf[:,2] * np.cos(np.deg2rad(theta))) # in us
  td_exp, ts_exp = ltdts(rho, s, theta) # in ns
  td_exp = td_exp * 1.e-3 # in us
  ts_exp = ts_exp * 1.e-3 # in us
  delta_tau = np.sqrt(np.power(ts_exp,2) + np.power(0.02,2))

  # Draw result
  tauErrorbar = ax.errorbar(s, tau, delta_tau, fmt='.', color='black')
  #tau_exp_Errorbar = ax.errorbar(s, td_exp, delta_tau, fmt='^', color='blue')

  fit_u = np.arange(-8, 8, 0.1)
  fit_n = 0
  fit_usintheta = fit_u * np.sin(np.deg2rad(theta)) # usintheta = l in thesis
  fit_s = un2s(fit_u, fit_n, theta)
  #fit_s = np.sqrt(np.power(fit_u,2) + np.power(fit_n,2)) * np.sin(np.deg2rad(theta))
  fit_rho = ldf(fit_s, theta) * float(sc)
  if a == 0:
    fit_td, fit_ts = ltdts(fit_rho, fit_s, theta)
  else:
    a_float = float(a)
    fit_td, fit_ts = ltdts1(fit_rho, fit_s, np.abs(fit_usintheta), a_float, theta)

  # Convert td, ts to us
  fit_td = fit_td / 1.e3
  fit_ts = fit_ts / 1.e3
  #print fit_td
  TimeFit = ax.plot(fit_s, fit_td, 'r-')

  ax.set_title('Timing Fit(%s)' % name)
  ax.set_xlabel('Lateral distance [km]')
  ax.set_ylabel('tau [us]')

  props = dict(boxstyle='round', facecolor='None', alpha=0.5, edgecolor='blue')

  ax.text(0.05, 0.95, \
    "Energy = %6.2f\nChi2/ndof = %5.2f/%s\nTheta = %6.2f\nPhi = %6.2f" % \
    (float(energy) * enscale, float(chi2), ndof, theta, phi), \
    fontsize=12, ha = 'left', va = 'top', transform = ax.transAxes, bbox=props)

def geoFit2(xyzclf, reltime, VEM, t0, xcore, ycore, theta, phi, sc, energy, chi2, ndof, ax, name, a = 0):
  # Calculate core position
  SD_ORIGIN_X_CLF = -12.2435
  SD_ORIGIN_Y_CLF = -16.4406
  SD_ORIGIN = np.array([SD_ORIGIN_X_CLF, SD_ORIGIN_Y_CLF, 0.])

  phi = 180 + phi
  s = []
  dotp = []
  u = []
  showerDirection = np.array([-np.sin(np.deg2rad(theta)) * np.cos(np.deg2rad(phi)),\
                              -np.sin(np.deg2rad(theta)) * np.sin(np.deg2rad(phi)),\
                              -np.cos(np.deg2rad(theta)) ])
  uDirection = np.array([-np.cos(np.deg2rad(phi)), -np.sin(np.deg2rad(phi)), 0])

  corePosition = np.array([float(xcore), float(ycore), 0.] )
  #print "Core position,", float(xcore) + SD_ORIGIN_X_CLF, float(ycore) + SD_ORIGIN_Y_CLF, "for", name

  # Calculate s
  for xyzclf_ in xyzclf:
    d = xyzclf_ - corePosition - SD_ORIGIN
    dotp_ = np.dot(d, showerDirection)
    s.append(np.sqrt(np.dot(d, d) - dotp_ * dotp_) * 1.2) # s in km
    u_ = np.dot(d, uDirection) * 1.2 # u in km 
    dotp.append(dotp_)
    u.append(u_)
    #print d, uDirection, u_

  # Calculate Rho, dRho
  s = np.array(s)
  rho = np.array(VEM) / 3.0
  drho = 0.53 * np.sqrt(2.0 * rho + np.power(0.15 * rho,2))
  dotp = np.array(dotp)

  # Calculate tau, observed, and ts, expected
  tau = 4. * (reltime - dotp - float(t0) + xyzclf[:,2] * np.cos(np.deg2rad(theta))) # in us
  td_exp, ts_exp = ltdts(rho, s, theta) # in ns
  td_exp = td_exp * 1.e-3 # in us
  ts_exp = ts_exp * 1.e-3 # in us
  delta_tau = np.sqrt(np.power(ts_exp,2) + np.power(0.02,2))

  # Draw result
  #tauErrorbar = ax.errorbar(s, tau, delta_tau, fmt='.', color='black')
  reltimeErrorbar = ax.errorbar(u, 4. * reltime, delta_tau, fmt='.', color='black', label="Rel. Time")

  #fit_u = np.arange(-5, 5, 0.1)
  fit_u = np.arange(np.min(u) - 0.5,np.max(u) + 0.5, 0.1)

  for fit_n in [0, 2, 4]:
    fit_s = un2s(fit_u, fit_n, theta)
    fit_rho = ldf(fit_s, theta) * float(sc)
    if a == 0:
      fit_td, fit_ts = ltdts(fit_rho, fit_s, theta)
    else:
      a_float = float(a)
      fit_usintheta = fit_u * np.sin(np.deg2rad(theta))
      fit_td, fit_ts = ltdts1(fit_rho, fit_s, fit_usintheta, a_float, theta)

    # Convert td, ts to us
    fit_td = fit_td / 1.e3
    fit_ts = fit_ts / 1.e3
    #print fit_td
    # Calculate fit rel. Time = l/c + t0 + tau
    fit_relTime = fit_u * np.sin(np.deg2rad(theta)) * 10 / 3 + fit_td  + 4. * float(t0)
    relTimeFit = ax.plot(fit_u, fit_relTime, label=("n=%dkm" % fit_n), color='red', dashes=[10-fit_n,fit_n])

  # Draw plane fit
  fit_planeTime = fit_u * np.sin(np.deg2rad(theta)) * 10 / 3 + 4. * float(t0)
  #planeTimeFit = ax.plot(fit_u, fit_planeTime, label="Plane", color='blue', dashes = [5,5])

  ax.set_title('Timing Fit(%s)' % name)
  ax.set_xlabel('Distance along u [km]')
  ax.set_ylabel('Rel. Time [us]')

  props = dict(boxstyle='round', facecolor='None', alpha=0.5, edgecolor='blue')

  if a == 0:
    ax.text(0.05, 0.95, \
      "Energy = %6.2f\nChi2/ndof = %5.2f/%s\nTheta = %6.2f\nPhi = %6.2f" % \
      (float(energy) * enscale, float(chi2), ndof, theta, phi), \
      fontsize=12, ha = 'left', va = 'top', transform = ax.transAxes, bbox=props)
  else:
    ax.text(0.05, 0.95, \
      "Energy = %6.2f\nChi2/ndof = %5.2f/%s\nTheta = %6.2f\nPhi = %6.2f\na = %5.3f" % \
      (float(energy) * enscale, float(chi2), ndof, theta, phi, a_float), \
      fontsize=12, ha = 'left', va = 'top', transform = ax.transAxes, bbox=props)


  #ax.legend(loc=4, prop={'size': 10})
  ax.legend(loc='upper right', prop={'size': 10})


def ldfFit(xyzclf, reltime, VEM, t0, xcore, ycore, theta, phi, sc, energy, chi2, ndof, ax, name):
  # Calculate s
  SD_ORIGIN_X_CLF = -12.2435
  SD_ORIGIN_Y_CLF = -16.4406
  SD_ORIGIN = np.array([SD_ORIGIN_X_CLF, SD_ORIGIN_Y_CLF, 0.])

  s = []
  dotp_ = []
  showerDirection = np.array([np.sin(np.deg2rad(theta)) * np.cos(np.deg2rad(phi)),\
                            np.sin(np.deg2rad(theta)) * np.sin(np.deg2rad(phi)),\
                            np.cos(np.deg2rad(theta)) ])
  corePosition = np.array([float(xcore), float(ycore), 0.] )
  #print (corePosition + SD_ORIGIN)
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

  # Draw on ax
  ax.set_xscale('log')
  ax.set_yscale('log')
  ax.set_xlim([0.1, 20])
  ax.set_xlabel('Lateral distance [km]')
  ax.set_ylabel('Rho [VEM/m^2]')
  ax.set_title('Lateral Distribution Fit')

  LD = ax.errorbar(s, rho, drho, fmt='o', color='black')


  # Draw fit function
  fit_x = np.linspace(0.1, 20, 50)
  fit_y = ldf(fit_x, theta) * float(sc)
  #fit_y_pe = ldf(fit_x, theta) * (float(sc) + float(dsc))
  #fit_y_me = ldf(fit_x, theta) * (float(sc) - float(dsc))

  LDFfit = ax.plot(fit_x, fit_y, color='red')
  #LDFfit_pe = ax1.plot(fit_x,fit_y_pe, 'r--')
  #LDFfit_me = ax1.plot(fit_x,fit_y_me, 'r--')

  props = dict(boxstyle='round', facecolor='None', alpha=0.5, edgecolor='blue')

  ax.text(0.05, 0.05,\
    "sc  = %9s\nEnergy = %6.2f\nChi2/ndof = %5.2f/%s" %\
    (sc, float(energy) * enscale, float(chi2), ndof),\
    fontsize=12, ha = 'left', va = 'bottom', transform = ax.transAxes, bbox=props)

# Function to dawr Footprint
# evtData = np.array(xx, yy, reltime_upper, reltime_lower, VEM_upper, VEM_lower)
# rec = [xcore_geo1, ycore_geo1, theta_geo1, phi_geo1, energy_ldf]

def DrawFootprint(evtData, rec, ax, layer = 0):

  if layer == 0:
    reltime = 0.5 * (np.array(evtData[2]) + np.array(evtData[3]))
    VEM = 0.5 * (np.array(evtData[4]) + np.array(evtData[5]))
  elif layer == 1:
    reltime = np.array(evtData[2])
    VEM = np.array(evtData[4])
  elif layer == 2:
    reltime = np.array(evtData[3])
    VEM = np.array(evtData[5])

  '''
  ## set X, Y ranges
  x_range = np.arange(int(np.min(evtData[0]))-2,int(np.max(evtData[0]))+2, 1)
  y_range = np.arange(int(np.min(evtData[1]))-2,int(np.max(evtData[1]))+2, 1)
  ax.set_xticks(x_range)
  ax.set_yticks(y_range)
  ax.set_xlim([x_range[0], x_range[-1]])
  ax.set_ylim([y_range[0], y_range[-1]])
  ax.set_xlabel('X position ID [2.08 km]')
  ax.set_ylabel('Y position iD [2.08 km]')

  ax.grid()
  '''

  scat = ax.scatter(evtData[0], evtData[1], s=np.sqrt(VEM)*500, c=reltime*4, edgecolors = 'w')

  cbar = plt.colorbar(scat, ax = ax)
  cbar.set_label('relative time [us]', rotation=270)

  SD_ORIGIN_X_CLF = -12.2435
  SD_ORIGIN_Y_CLF = -16.4406

  xcore_km = 1.2 * (float(rec[0]) + SD_ORIGIN_X_CLF)
  ycore_km = 1.2 * (float(rec[1]) + SD_ORIGIN_Y_CLF)

  xcore_sdID = xcore_km / 2.08 + 4.34807
  ycore_sdID = ycore_km / 2.08 + 54.6365

  ax.scatter(xcore_sdID, ycore_sdID, marker = '*', s = 100, c = 'black')

  dx = 2 * np.cos(np.deg2rad(float(rec[3])))
  dy = 2 * np.sin(np.deg2rad(float(rec[3])))

  ax.arrow(xcore_sdID - dx, ycore_sdID - dy, 2 * dx, 2 * dy, head_width = 0.5, head_length = 1)

  return scat

# Draw Footprint from given event data
def Footprint(EvtFile):

  print EvtFile
  infile = open(EvtFile, 'r')

  # Read reconstruction results
  # RAW, RUFPTN
  evtInfo = infile.readline().split()
  yymmdd        = evtInfo[1]
  hhmmss        = evtInfo[2]
  usec          = evtInfo[3]
  nstclust      = evtInfo[4]

  # GEOM1 - Linsley fit
  evtInfo = infile.readline().split()
  t0_geo1       = evtInfo[1]
  dt0_geo1      = evtInfo[2]
  xcore_geo1    = evtInfo[3] #-12.2435 need to convert TAx4 coordinate
  dxcore_geo1   = evtInfo[4] #-16.4406
  ycore_geo1    = evtInfo[5]
  dycore_geo1   = evtInfo[6]
  theta_geo1    = evtInfo[7]
  dtheta_geo1   = evtInfo[8]
  phi_geo1      = evtInfo[9]
  dphi_geo1     = evtInfo[10]
  chi2_geo1     = evtInfo[11]
  ndof_geo1     = evtInfo[12]

  # GEOM2 - Linsley w/ curvature
  evtInfo = infile.readline().split()
  t0_geo2       = evtInfo[1]
  dt0_geo2      = evtInfo[2]
  xcore_geo2    = evtInfo[3] #-12.2435 need to convert TAx4 coordinate
  dxcore_geo2   = evtInfo[4] #-16.4406
  ycore_geo2    = evtInfo[5]
  dycore_geo2   = evtInfo[6]
  theta_geo2    = evtInfo[7]
  dtheta_geo2   = evtInfo[8]
  phi_geo2      = evtInfo[9]
  dphi_geo2     = evtInfo[10]
  a_geo2        = evtInfo[11]
  da_geo2       = evtInfo[12]
  chi2_geo2     = evtInfo[13]
  ndof_geo2     = evtInfo[14]

  # LDF
  evtInfo = infile.readline().split()
  xcore_ldf     = evtInfo[1]
  dxcore_ldf    = evtInfo[2]
  ycore_ldf     = evtInfo[3]
  dycore_ldf    = evtInfo[4]
  sc_ldf        = evtInfo[5]
  dsc_ldf       = evtInfo[6]
  energy_ldf    = evtInfo[7]
  chi2_ldf      = evtInfo[8]
  ndof_ldf      = evtInfo[9]

  # GLDF
  evtInfo = infile.readline().split()
  t0_gldf       = evtInfo[1]
  dt0_gldf      = evtInfo[2]
  xcore_gldf    = evtInfo[3] #-12.2435 need to convert TAx4 coordinate
  dxcore_gldf   = evtInfo[4] #-16.4406
  ycore_gldf    = evtInfo[5]
  dycore_gldf   = evtInfo[6]
  theta_gldf    = evtInfo[7]
  dtheta_gldf   = evtInfo[8]
  phi_gldf      = evtInfo[9]
  dphi_gldf     = evtInfo[10]
  sc_gldf       = evtInfo[11]
  dsc_gldf      = evtInfo[12]
  energy_gldf   = evtInfo[13]
  chi2_gldf     = evtInfo[14]
  ndof_gldf     = evtInfo[15]

  # Read data of each SD
  inlines = infile.readlines()
  #print inlines
  xx = []
  yy = []
  isgood = []
  reltime_upper = []
  reltime_lower = []
  VEM_upper = []
  VEM_lower = []
  xyzclf = []

  for inline in inlines:
    evt = inline.split()
    if 1:#(int(evt[1]) >= 3) and (int(evt[1]) <= 4):
      #print evt
      xx.append(int(evt[0][:2]))
      yy.append(int(evt[0][2:]))
      isgood.append(int(evt[1]))
      reltime_upper.append(float(evt[2]))
      reltime_lower.append(float(evt[3]))
      VEM_upper.append(float(evt[4]))
      VEM_lower.append(float(evt[5]))
      xyzclf.append([float(evt[6]), float(evt[7]), float(evt[8])])

  # Define canvas
  fig = plt.figure(figsize = (7,3))
  ax1 = fig.add_subplot(1,2,1) # Canvas for all signal
  ax2 = fig.add_subplot(1,2,2) # Canvas for S-T signal only

  evtData = [xx, yy, reltime_upper, reltime_lower, VEM_upper, VEM_lower]
  rec = [xcore_geo1, ycore_geo1, theta_geo1, phi_geo1, energy_ldf] 

  ## set X, Y ranges
  x_range = np.arange(int(np.mean(evtData[0]))-4,int(np.mean(evtData[0]))+5, 1)
  y_range = np.arange(int(np.mean(evtData[1]))-4,int(np.mean(evtData[1]))+5, 1)

  ax1.set_xticks(x_range)
  ax1.set_yticks(y_range)
  ax1.set_xlim([x_range[0], x_range[-1]])
  ax1.set_ylim([y_range[0], y_range[-1]])
  ax1.set_xlabel('X position ID [2.08 km]')
  ax1.set_ylabel('Y position iD [2.08 km]')
  ax1.grid()

  ax2.set_xticks(x_range)
  ax2.set_yticks(y_range)
  ax2.set_xlim([x_range[0], x_range[-1]])
  ax2.set_ylim([y_range[0], y_range[-1]])
  ax2.set_xlabel('X position ID [2.08 km]')
  ax2.set_ylabel('Y position iD [2.08 km]')
  ax2.grid()

  allScat = DrawFootprint(evtData, rec, ax1)

  print evtData
  print rec

  # Select S-T only
  cutOutIndex = []
  for i in range(len(isgood)):
    if isgood[i] <= 3:
      cutOutIndex.append(i)
  if len(cutOutIndex) != 0:
    for delIndex in reversed(cutOutIndex):
      for j in range(len(evtData)):
        evtData[j].pop(delIndex)

  STScat = DrawFootprint(evtData, rec, ax2)
  
  #fig.subplots_adjust(right=0.8)
  #cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
  #cbar = plt.colorbar(allScat, cax = cbar_ax)

  plt.tight_layout()
  #plt.show()
  figname='.'.join(EvtFile.split('.')[:-1])
  plt.savefig("%s.Footprint.pdf" % figname)
