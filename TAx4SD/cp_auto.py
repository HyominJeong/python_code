import sys, os

cts = ['km', 'bf', 'sn', 'sr', 'sc', 'dm']
towerDir = "/ta/work/user/hyomin/tower/"
rawDir = "/ta/data/SD/TAx4/tower/"
for ct in cts:
  # read start & end of the event number
  cmd = ("tail -n 1 %s%sct/file.lst" % (towerDir, ct))
  print cmd
  os.system(cmd)

  digFrom = int(os.popen(cmd).read().split("\n")[0].split(".")[-3][-8:])

  cmd = ("ls %s%s/DATA/ |grep Y.bz2|tail -n 1" % (rawDir, ct))
  print cmd
  os.system(cmd)
  digTo   = int(os.popen(cmd).read().split("\n")[0].split(".")[-3][-8:])
  print digFrom, digTo

  if digFrom < digTo:
    # Copy raw files
    cmd = "bash /ta/work/user/hyomin/bash_code/cp_from_to.sh %d %d %s" % (digFrom, digTo, ct)
    print cmd
    os.system(cmd)
    
    # Extract
    cmd = "bash %sscript/Extract.sh %s" % (towerDir, ct)
    print(cmd)
    os.system(cmd)

    # Change file name
    cmd = "bash %sscript/OldFileName.sh %s" % (towerDir, ct)
    print(cmd)
    os.system(cmd)

    # Delete temporary files
    cmd = "rm %s%sct/DATA/*" % (towerDir, ct)
    print(cmd)
    os.system(cmd)

  else:
    print("%s is omitted, Evt number is %d(done), %d(recent)" % (ct, digTo, digFrom))

  
