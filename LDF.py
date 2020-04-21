import matplotlib.pyplot as plt
import numpy as np
import glob
import sys

infiles = glob.glob("*.txt")

# Input file is a list of
# rusdraw_.yymmdd, rusdraw_.hhmmss, rusdraw_.usec, rufldf_.xcore[1], rufldf_.dxcore[1], rufldf_.ycore[1], rufldf_.dycore[1], rufptn_.nstclust, rufldf_.theta, rufldf_.phi, rufldf_.chi2[1], rufldf_.energy[0], rufldf_.energy[1]
# rufptn_.xxyy[x], rufptn_.isgood[x], rufptn_.reltime[x][0], rufptn_.reltime[x][1], rufptn_.pulsa[x][0], rufptn_.pulsa[x][1]

# Define lateral distribution function
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
        xyzclf.append(np.array([float(evt[6]), float(evt[7]), float(evt[8])]))
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
        xyzclf.append(np.array([float(evt[6]), float(evt[7]), float(evt[8])]))

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
  showerDirection = np.array([np.sin(np.deg2rad(theta)) * np.cos(np.deg2rad(phi)),\
  			    np.sin(np.deg2rad(theta)) * np.sin(np.deg2rad(phi)),\
  			    np.cos(np.deg2rad(theta)) ])
  corePosition = np.array([float(xcore), float(ycore), 0.] )
  print corePosition + SD_ORIGIN
  for xyzclf_ in xyzclf:
    d = xyzclf_ - corePosition - SD_ORIGIN
    #print d
    dotp = np.dot(d, showerDirection)
    #s.append(np.sqrt(np.dot(np.dot(d, showerDirection), np.dot(d, showerDirection))))
    s.append(np.sqrt(np.dot(d, d) - dotp * dotp) * 1.2) # s in km

  #print s
  rho = VEM / 3.0
  drho = 0.53 * np.sqrt(2.0 * rho + np.power(0.15 * rho,2))

  #print s, rho
  
  fig = plt.figure()
  ax = fig.gca()

  '''
  ax.set_xscale('log')
  ax.set_yscale('log')
  ax.set_xlim([0.1, 20])
  ax.set_xlabel('Lateral distance [km]')
  ax.set_ylabel('Rho [VEM/km^2]')
  ax.set_title('Lateral Distribution Fit, %s %s.%s' % (yymmdd, hhmmss, usec))

  LD = ax.errorbar(s, rho, drho, fmt='o', color='black')


  # Draw fit function
  fit_x = np.linspace(0.1, 20, 50)
  fit_y = ldf(fit_x, theta) * float(sc)

  LDFfit = ax.plot(fit_x, fit_y, color='red')

  #plt.show()
  figName = ("%s.%s.%s.%s.LDF.pdf" % (yymmdd, hhmmss, usec, st))
  print figName, "is saved."
  plt.savefig(figName)
  '''

  TimeFit = ax.errorbar(s, reltime, 0)
  plt.show()

  #break
