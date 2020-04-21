import os, sys
import numpy as np

def readDUMP(DUMPTXT, energy = 0):
  infile = open(DUMPTXT, 'r')
  while 1:
    line = infile.readline().strip('\n')
    if (line == "START OF EVENT ***********************************************************"):
      #print line
      #break
      while 1:
        evtline = infile.readline().strip('\n')
        if (evtline == "END OF EVENT *************************************************************"):
          break
        txt2lst = evtline.split()
        if (len(txt2lst) != 1):
          #print txt2lst
          if txt2lst[0:5] == "Total Energy of Primary Particle:".split():
            if (float(txt2lst[5]) > 10):
              print txt2lst[5]
            break

readDUMP(sys.argv[1])  
