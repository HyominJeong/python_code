import matplotlib.pyplot as plt
import numpy as np
import glob
import sys
import FitFunc

infiles = glob.glob("*.txt")

# Input file is a list of
# rusdraw_.yymmdd, rusdraw_.hhmmss, rusdraw_.usec, rufldf_.xcore[1], rufldf_.dxcore[1], rufldf_.ycore[1], rufldf_.dycore[1], rufptn_.nstclust, rufldf_.theta, rufldf_.phi, rufldf_.chi2[1], rufldf_.energy[0], rufldf_.energy[1]
# rufptn_.xxyy[x], rufptn_.isgood[x], rufptn_.reltime[x][0], rufptn_.reltime[x][1], rufptn_.pulsa[x][0], rufptn_.pulsa[x][1]

for infile in infiles:
  FitFunc.Footprint(infile)
