import numpy as np
import sys

SDEvtFile = sys.argv[1]
FDEvtFile = sys.argv[2]

SDEvts = np.loadtxt(SDEvtFile)
FDEvts = np.loadtxt(FDEvtFile, skiprows=1, dtype=np.str, delimiter=',')

#print(SDEvts[:5])
#print(FDEvts[:5])

# Search Hybrid Trig
for FDEvt in FDEvts:
  YYYY, MM, DD = FDEvt[1].split()[0].split('-')
  FDTime_YYMMDD = ("%2s%2s%2s" % (YYYY[-2:], MM, DD))
  hh, mm, ss = FDEvt[1].split()[-1].split('.')[0].split(':')
  FDTime_usec = int(FDEvt[1].split()[-1].split('.')[1])
  FDTime_sec = int(hh) * 3600 + int(mm) * 60 + int(ss)
  #print FDTime_YYMMDD, hh, mm, ss, FDTime_sec, FDTime_usec

  for SDEvt in SDEvts:
    SDTime_YYMMDD = str(int(SDEvt[0]))
    SDTime_sec = int(SDEvt[1])//10000*3600 + int(SDEvt[1])%10000//100*60 + int(SDEvt[1])%100
    SDTime_usec = int(SDEvt[2])
    #print SDTime_YYMMDD, ("%06d" % SDEvt[1]), SDTime_sec, SDTime_usec

    if (FDTime_YYMMDD == SDTime_YYMMDD) and (abs(FDTime_sec - SDTime_sec) < 2):
      print("SD Time is %s %06d" % (FDTime_YYMMDD, SDEvt[1]))
