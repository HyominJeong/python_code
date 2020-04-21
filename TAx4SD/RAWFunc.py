import numpy as np
import sys, os


def readHexaEvtTime(timeFlag):
  timeFlag_bin = bin(int(timeFlag, 16))[2:].zfill(32)
  print timeFlag_bin
  trg = int(timeFlag_bin[:2], 2)
  snum = int(timeFlag_bin[2:12], 2)
  msec = int(timeFlag_bin[12:32], 2)

  print trg, snum, msec

def evtTime(YYMMDD, hh, ct):

  YY = YYMMDD // 10000
  MM = YYMMDD % 10000 // 100
  DD = YYMMDD % 100

  towerDIR = ("/ta/work/user/hyomin/tower/%s/data" % ct)
  rawFile = ("%s/%s%02d%02d%02d.Y20%02d" % (towerDIR, ct.upper(), MM, DD, hh, YY))

  cmd=("grep -n '^E' %s" % rawFile)
  print(cmd)
  lines = os.popen(cmd).read().split("\n")
  cmd=("grep -n '### DONE' %s" % rawFile)
  elines = os.popen(cmd).read().split("\n")
  print(elines)

  i = 0
  for line in lines:
    print line
    if len(line.split(":")) == 2:
      sline = line.split(":")[0]
      if len(line.split(":")[1].split(' ')) == 3:
        header, trgID, timeFlag = line.split(":")[1].split(' ')
        #print sline, header, trgID, timeFlag
        readHexaEvtTime(timeFlag)
        eline = int(elines[i].split(":")[0])
        cmd=("sed -n '%s,%sp' %s" % (sline, eline, rawFile))
        print(cmd)
        wfData = os.popen(cmd).read().split("\n")
        for wf in wfData:
          print(wf)

    i += 1
