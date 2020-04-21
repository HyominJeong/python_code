import matplotlib.pyplot as plt
import numpy as np
import glob
import sys
from FitFunc import *

infiles = sorted(glob.glob("*.txt"))

# Input file is a list of
# rusdraw_.yymmdd, rusdraw_.hhmmss, rusdraw_.usec, rufptn_.nstclust);
# GEOM1, rusdgeom_.t0[1], rusdgeom_.dt0[1], rusdgeom_.xcore[1], rusdgeom_.dxcore[1], rusdgeom_.ycore[1], rusdgeom_.dycore[1], rusdgeom_.theta[1], rusdgeom_.dtheta[1], rusdgeom_.phi[1], rusdgeom_.dphi[1], rusdgeom_.chi2[1], rusdgeom_.ndof[1]
# GEOM2 rusdgeom_.t0[2], rusdgeom_.dt0[2], rusdgeom_.xcore[2], rusdgeom_.dxcore[2], rusdgeom_.ycore[2], rusdgeom_.dycore[2], rusdgeom_.theta[2], rusdgeom_.dtheta[2], rusdgeom_.phi[2], rusdgeom_.dphi[2], rusdgeom_.a, rusdgeom_.da, rusdgeom_.chi2[2], rusdgeom_.ndof[2]
# LDF, rufldf_.xcore[0], rufldf_.dxcore[0], rufldf_.ycore[0], rufldf_.dycore[0], rufldf_.sc[0], rufldf_.dsc[0], rufldf_.chi2[0], rufldf_.ndof[0]);
# GLDF, rufldf_.t0, rufldf_.dt0, rufldf_.xcore[1], rufldf_.dxcore[1], rufldf_.ycore[1], rufldf_.dycore[1], rufldf_.theta, rufldf_.dtheta, rufldf_.phi, rufldf_.dphi, rufldf_.sc[1], rufldf_.dsc[1], rufldf_.chi2[1], rufldf_.ndof[1]);
# And data from each SDs
# rufptn_.xxyy[x], rufptn_.isgood[x], rufptn_.reltime[x][0], rufptn_.reltime[x][1], rufptn_.pulsa[x][0], rufptn_.pulsa[x][1]
Draw = False
print sys.argv
# Draw or not
if len(sys.argv) > 1:
  Draw = True
else:
  # Print out reconstruction result on file
  recResult = open("recResult.rec", 'w')

# Read from infiles
for file in infiles:
  #print file
  infile = open(file, 'r')

  # Read reconstruction results
  # RAW, RUFPTN
  evtInfo = infile.readline().split()
  yymmdd	= evtInfo[1]
  hhmmss	= evtInfo[2]
  usec		= evtInfo[3]
  nstclust      = evtInfo[4]

  # GEOM1 - Linsley fit
  evtInfo = infile.readline().split()
  t0_geo1	= evtInfo[1]
  dt0_geo1	= evtInfo[2]
  xcore_geo1	= evtInfo[3] #-12.2435 need to convert TAx4 coordinate
  dxcore_geo1	= evtInfo[4] #-16.4406
  ycore_geo1	= evtInfo[5]
  dycore_geo1	= evtInfo[6]
  theta_geo1	= evtInfo[7]
  dtheta_geo1	= evtInfo[8]
  phi_geo1	= evtInfo[9]
  dphi_geo1	= evtInfo[10]
  chi2_geo1	= evtInfo[11]
  ndof_geo1	= evtInfo[12]

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
  a_geo2	= evtInfo[11]
  da_geo2	= evtInfo[12]
  chi2_geo2     = evtInfo[13]
  ndof_geo2     = evtInfo[14]

  # LDF
  evtInfo = infile.readline().split()
  xcore_ldf	= evtInfo[1]
  dxcore_ldf	= evtInfo[2]
  ycore_ldf	= evtInfo[3]
  dycore_ldf	= evtInfo[4]
  sc_ldf	= evtInfo[5]
  dsc_ldf	= evtInfo[6]
  energy_ldf	= evtInfo[7]
  chi2_ldf	= evtInfo[8]
  ndof_ldf	= evtInfo[9]

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
      '''
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
      '''
      # Show only S-T cluster SDs
      evt = inline.split()
      #if (int(evt[1]) >= 3) and (int(evt[1]) <= 4):
      if int(evt[1]) == 4:
        #print evt
        xx.append(int(evt[0][:2]))
        yy.append(int(evt[0][2:]))
        isgood.append(int(evt[1]))
        reltime_upper.append(float(evt[2]))
        reltime_lower.append(float(evt[3]))
        VEM_upper.append(float(evt[4]))
        VEM_lower.append(float(evt[5]))
        xyzclf.append([float(evt[6]), float(evt[7]), float(evt[8])])

      #print xx, yy, status

  if Draw:
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
  
    # Draw only if chi2 of geom1, ldf, gldf < 100000
    if (float(chi2_geo1) < 1.e6) and (float(chi2_geo2) < 1.e6) and (float(chi2_ldf) < 1.e6) and (float(chi2_gldf) < 1.e6):
      # Draw Timeing Fit
      fig = plt.figure(figsize = (15, 5))
      ax1 = fig.add_subplot(1,3,1)
      ax2 = fig.add_subplot(1,3,2)
      ax3 = fig.add_subplot(1,3,3)
      
      #ax4 = fig.add_subplot(2,4,5)
      #ax5 = fig.add_subplot(2,4,6)
      #ax6 = fig.add_subplot(2,4,7)

      geoFit2(xyzclf, reltime, VEM, t0_geo1, xcore_geo1, ycore_geo1, float(theta_geo1), float(phi_geo1), sc_ldf, energy_ldf, chi2_geo1, ndof_geo1, ax1, "Linsley")
      #geoFit2(xyzclf, reltime, VEM, t0_geo2, xcore_geo2, ycore_geo2, float(theta_geo2), float(phi_geo2), sc_ldf, energy_ldf, chi2_geo2, ndof_geo2, ax2, "Lins. w/ curvature", a_geo2)
      geoFit2(xyzclf, reltime, VEM, t0_gldf, xcore_gldf, ycore_gldf, float(theta_gldf), float(phi_gldf), sc_gldf, energy_gldf, chi2_gldf, ndof_gldf, ax2, "Lins. + LDF")

      #geoFit(xyzclf, reltime, VEM, t0_geo1, xcore_geo1, ycore_geo1, float(theta_geo1), float(phi_geo1), sc_ldf, energy_ldf, chi2_geo1, ndof_geo1, ax4, "Linsley")
      #geoFit(xyzclf, reltime, VEM, t0_geo2, xcore_geo2, ycore_geo2, float(theta_geo2), float(phi_geo2), sc_ldf, energy_ldf, chi2_geo2, ndof_geo2, ax5, "Lins. w/ curvature", a_geo2)
      #geoFit(xyzclf, reltime, VEM, t0_gldf, xcore_gldf, ycore_gldf, float(theta_gldf), float(phi_gldf), sc_gldf, energy_gldf, chi2_gldf, ndof_gldf, ax6, "Lins. + LDF")



      #plt.show()
      #figName = ("%s.%s.%s.TimeFit.pdf" % (yymmdd, hhmmss, usec))
      #print figName, "is saved."
      #plt.savefig(figName)


      # Draw LDF fit
      #fig = plt.figure(figsize = (10,5))
      #ax1 = fig.add_subplot(1,2,1)
      #ax2 = fig.add_subplot(1,2,2)
      #ldfFit(xyzclf, reltime, VEM, t0_geo1, xcore_geo1, ycore_geo1, float(theta_geo1), float(phi_geo1), sc_ldf, energy_ldf, chi2_ldf, ndof_ldf, ax3, "LDF")
      ldfFit(xyzclf, reltime, VEM, t0_gldf, xcore_gldf, ycore_gldf, float(theta_gldf), float(phi_gldf), sc_gldf, energy_gldf, chi2_gldf, ndof_gldf, ax3, "GLDF")
      #plt.show()
      figName = ("%s.%s.%s.FIT.png" % (yymmdd, hhmmss, usec))
      print figName, "is saved."
      plt.savefig(figName)
    
    '''
    print>>recResult, yymmdd, hhmmss, usec, nstclust, t0_geo1, dt0_geo1, xcore_geo1, dxcore_geo1, ycore_geo1, dycore_geo1, theta_geo1, dtheta_geo1, phi_geo1, dphi_geo1, chi2_geo1, ndof_geo1, energy_ldf, chi2_ldf, ndof_ldf, energy_gldf, chi2_gldf, ndof_gldf
    '''
  else:
    print>>recResult, yymmdd, hhmmss, usec, nstclust, t0_geo1, dt0_geo1, xcore_geo1, dxcore_geo1, ycore_geo1, dycore_geo1, theta_geo1, dtheta_geo1, phi_geo1, dphi_geo1, chi2_geo1, ndof_geo1, energy_ldf, chi2_ldf, ndof_ldf, t0_gldf, xcore_gldf, ycore_gldf, theta_gldf, phi_gldf, energy_gldf, chi2_gldf, ndof_gldf, sc_gldf, dsc_gldf
