import numpy as np
import glob
import matplotlib.pyplot as plt
from matplotlib.pyplot import text

def plotWF(XXYY, upper, lower, relTime):
  t = np.arange(0,128,1)
  t_upper = t + relTime
  t_lower = t + relTime

  ax.plot(t_upper, upper + wf_step)
  ax.plot(t_lower, lower + wf_step)

  ax.text(108 + relTime, 15 + wf_step, XXYY)

  return 0

infiles = glob.glob("*.wf")
for infile in infiles:
  inlines = open(infile, 'r').readlines()

  if len(inlines) % 3 != 0:
    print "Strange WF data input from", infile
  else:
    print len(inlines) // 3, "WF data drawing"

    # Initialize to read WF data
    XXYY = []
    #isgood = []
    #relTime_upper = []
    #relTime_lower = []
    cntclk = []
    mcntclk = []
    relTime_20ns = []

    wf_upper = []
    wf_lower = []
    
    # Read WF data and SD information
    nofline = 0
    for inline in inlines:
      if nofline % 3 == 0:
        data = inline.split()
        XXYY.append(data[0][-2:] + data[0][:2]) # Raw data format is YYXX
        #isgood.append(int(data[1]))
        #relTime_upper.append(float(data[2]) * 2.e2) # in [20 ns]
        #relTime_lower.append(float(data[3]) * 2.e2) # in [20 ns]
        relTime_20ns.append(1. * int(data[1]) / int(data[2]) * 1.e9 / 20) # Convert to 20ns init
        
      elif nofline % 3 == 1:
        data = inline.split()
        wf_upper.append(np.array(data,dtype=np.int))
      elif nofline % 3 == 2:
        data = inline.split()
        wf_lower.append(np.array(data,dtype=np.int))
 
      nofline += 1

    # Plot WF data
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    #relTime = 0.5 * (np.array(relTime_upper) + np.array(relTime_lower))
    relTime_20ns = np.array(relTime_20ns)
    wf_step = 0
    for i in relTime_20ns.argsort():
      if 1:#isgood[i] >= 3:      
        plotWF(XXYY[i], wf_upper[i], wf_lower[i], relTime_20ns[i])
        wf_step += 50
    YYMMDD, hhmmss, usec = infile.split('.')[:3]
    ax.set_title("Wave form of %s %s.%s" % (YYMMDD, hhmmss, usec))
    ax.set_xlabel("Time slice [20ns]")
    ax.set_ylabel("ADC value")
    #plt.show()
    plt.savefig("%s.%s.%s.WF.pdf" % (YYMMDD, hhmmss, usec))
