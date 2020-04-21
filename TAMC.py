import os, sys
from time import sleep

#print sys.argv[1]
wantList = open(sys.argv[1], 'r').readlines()
doneList = open("done.lst", 'rw')
for inDST in wantList:
  MCDST = inDST.strip('\n')
  os.system("rufptn.run %s" % MCDST)
  os.system("echo %s >> done.lst" % MCDST)
  MCrufptn = MCDST.split('/')[-1].split('.')
  MCrufptn = '.'.join(MCrufptn[:2] + ['rufptn'] + MCrufptn[2:])
  #print MCrufptn
  os.system("rufldf.run %s" % MCrufptn)
  #break
  sleep(300)
