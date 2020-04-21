import numpy as np
import os
from matplotlib import pyplot as plt
from datetime import date

def Landau(x):
  return 1. / np.sqrt(2 * np.pi) * np.exp(-(x + np.exp(-x) / 2))

def hex2dec(hexArr):
  decArr = []
  for i in range(len(hexArr)):
    decArr.append(int(hexArr[i], 16))
  return np.array(decArr)

def readHV(fileRaw, SDID):
  cmd = ('grep %s %s' % (SDID, fileRaw))
  data = op.popen(cmd).read().split("\n")
  return data[0].split(' ')[8:10]

def read1MIPPed(fileRaw, SDID):
  cmd = ('grep "L %s " %s' % (SDID, fileRaw))
  #print cmd
  data = os.popen(cmd).read().split("\n")
  #print data 
  #print(data[:5])
  
  #if len(data) != 3600:
  #  print("Wrong raw data, have %d lines", fileRaw, SDID, len(data))
  #  return 0, 0

  # Split 1 hour data to 6 * 10mins data
  MipHist_upp = []
  MipHist_low = []
  MipChan_upp = []
  MipChan_low = []
  PedHist_upp = []
  PedHist_low = []
  PedChan_upp = []
  PedChan_low = []

  tmpsnum = 600
  for line in data:
    if len(line.split(' ')) != 12:
      #print(line)
      a = 1 
    else:
      snum = int(line.split(' ')[4])
      v1 = int(line.split(' ')[8], 16)
      v2 = int(line.split(' ')[9], 16)
      v3 = int(line.split(' ')[10], 16)
      v4 = int(line.split(' ')[11], 16)

      if snum < tmpsnum:
        MipHist_upp.append([])
        MipHist_low.append([])
        MipChan_upp.append([])
        MipChan_low.append([])
        PedHist_upp.append([])
        PedHist_low.append([])
        PedChan_upp.append([])
        PedChan_low.append([])
        tmpsnum = snum
      else:
        tmpsnum = snum

      if snum < 128:
        MipChan_upp[-1].extend(range(snum*4, snum*4+4))
        MipHist_upp[-1].extend([v1, v2, v3, v4])

      if snum >= 128 and snum < 256: 
        MipChan_low[-1].extend(range((snum-128)*4, (snum-128)*4+4))
        MipHist_low[-1].extend([v1, v2, v3, v4])

      if snum >= 256 and snum < 320:
        PedChan_upp[-1].extend(range((snum-256)*4, (snum-256)*4+4))
        PedHist_upp[-1].extend([v1, v2, v3, v4])

      if snum >= 320 and snum < 384:
        PedChan_low[-1].extend(range((snum-320)*4, (snum-320)*4+4))
        PedHist_low[-1].extend([v1, v2, v3, v4])

  return [MipHist_upp, MipHist_low], [MipChan_upp, MipChan_low],\
         [PedHist_upp, PedHist_low], [PedChan_upp, PedChan_low]
    
  '''
  data10min = [data[:600], data[600:1200], data[1200:1800], data[1800:2400], data[2400:3000], data[3000:3600]]

  pMinNum = 15
  pMaxNum = 30

  nOfMIPChan = 512
  nOfPedChan = 256
  nOfLinChan = 128

  MIPHist = []
  PedHist = []

  for data in data10min: 

    print(data[pMinNum:pMaxNum])
    secNum = []
    HistData_hex = data.T[8:].T.flatten()
    HistData = hex2dec(HistData_hex)
    print(HistData[pMinNum*4:pMaxNum*4])

    MIPHist.append(HistData[0:nOfMIPChan])
    MIPHist.append(HistData[1 * nOfMIPChan:2 * nOfMIPChan])

    PedHist.append(HistData[2 * nOfMIPChan:2 * nOfMIPChan + nOfPedChan])
    PedHist.append(HistData[2 * nOfMIPChan + nOfPedChan :2 * nOfMIPChan + 2 * nOfPedChan])

  return MIPHist, PedHist
  '''

def pltHists(Hists, Chans, ax, c='black'):
  if len(Hists) == len(Chans):
    for i in range(len(Hists)):
      ax.plot(Chans[i], Hists[i], color=c)


def calMP(MipHist, MipChan):
  if len(MipHist) > 100:
  #print MipChan[np.argmax(MipHist)]
  #plt.plot(MipChan, MipHist)
  #plt.show()
    return MipChan[np.argmax(MipHist[:-1])]
  else:
    return 0

def dailyMIP(yymmdd_from, yymmdd_to, ct, SDID):
  yy_from = yymmdd_from // 10000
  mm_from = yymmdd_from % 10000 // 100
  dd_from = yymmdd_from % 100

  yy_to = yymmdd_to // 10000
  mm_to = yymmdd_to % 10000 // 100
  dd_to = yymmdd_to % 100

  days_upp = []
  days_low = []
  MipMP_upp = []
  MipMP_low = []

  for yy in range(yy_from, yy_to +1):
    for mm in range(mm_from, mm_to +1):
      for dd in range(dd_from, dd_to +1):
        for hh in range(0, 24):
          fileRaw=("/ta/work/user/hyomin/tower/%s/data/%s%02d%02d%02d.Y20%02d" % (ct.lower(), ct.upper(), mm, dd, hh, yy))

          MipHist, MipChan , PedHist, PedChan = read1MIPPed(fileRaw, SDID)
 
          yymmdd = 191200
          yymmdd_ref = 190401
          day = date(yymmdd // 10000 + 2000, yymmdd % 10000 // 100, dd % 100)
          day_ref = date(yymmdd_ref // 10000 + 2000, yymmdd_ref % 10000 // 100, yymmdd_ref % 100)

          delta = day - day_ref

          for i in range(len(MipChan[0])):
            days_upp.append(delta.days + 1. / 24 * hh + 1./ 24 / 6 * i)
            MipMP_upp.append(calMP(MipHist[0][i], MipChan[0][i]) - calMP(PedHist[0][i], PedChan[0][i]))

            days_low.append(delta.days + 1. / 24 * hh + 1./ 24 / 6 * i)
            MipMP_low.append(calMP(MipHist[1][i], MipChan[1][i]) - calMP(PedHist[1][i], PedChan[1][i]))

            #print MipMP_upp[-1], MipMP_low[-1]
            if MipMP_upp[-1] > 400 or MipMP_upp[-1] < 100:
              print dd, hh, i, SDID, MipMP_upp[-1]
            if MipMP_low[-1] > 400 or MipMP_low[-1] < 100:
              print dd, hh, i, SDID, MipMP_low[-1]

  return [MipMP_upp, MipMP_low], [days_upp, days_low]

def avgMIP(MipMP, days):

  # Neglect MP > hThr or MP < lThr
  lThr = 50
  hThr = 500

  avg = 0
  n = 0

  for MP in MipMP:
    if MP < hThr and MP > lThr:
      avg += MP
      n += 1
  if n != 0:
    return 1. * avg / n
  else:
    return 0

def read1MIP(datafileName):
  data = np.loadtxt(datafileName, dtype=np.str)[:600]
  pMinNum = 15
  pMaxNum = 30
  print(data[pMinNum:pMaxNum])
  secNum = []
  MIPHist_hex = data.T[8:].T.flatten()
  MIPHist = hex2dec(MIPHist_hex)
  print(MIPHist[pMinNum*4:pMaxNum*4])

  fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (10,5))
  
  nOfMIPChan = 512 
  nOfPedChan = 256
  nOfLinChan = 128

  ax1.plot(MIPHist[0:nOfMIPChan], label='Upper')
  ax1.plot(MIPHist[1 * nOfMIPChan:2 * nOfMIPChan], label='Lower')
  #ax1.plot(MIPHist)
  ax1.set_title('1MIP histogram')
  ax1.set_yscale('log')
  ax1.legend()

  ax2.plot(MIPHist[2 * nOfMIPChan:2 * nOfMIPChan + nOfPedChan], label='Upper')
  ax2.plot(MIPHist[2 * nOfMIPChan + nOfPedChan :2 * nOfMIPChan + 2 * nOfPedChan], label='Lower')
  ax2.set_yscale('log')
  ax2.set_title('Pedestal Histogram')
  ax2.legend()
  '''
  ax3.plot(MIPHist[2 * nOfMIPChan + 2 * nOfPedChan:2 * nOfMIPChan + 2 * nOfPedChan + nOfLinChan], label='Upper')
  ax3.plot(MIPHist[2 * nOfMIPChan + 2 * nOfPedChan + nOfLinChan:2 * nOfMIPChan + 2 * nOfPedChan + 2 * nOfLinChan], label='Lower')
  ax3.set_yscale('log')
  ax3.set_title('Linearity Histogram')
  ax3.legend()
  '''

  fig.suptitle("TAx4 SD %s" % data[0][1], fontsize=15)
  plt.show()
