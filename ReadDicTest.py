import RecResultFunc

EvtDict, DataStrt = RecResultFunc.ReadDicStructure()

#for EvtKey in EvtDict:
#  print EvtKey

#print DataStrt

print EvtDict

EvtDict = RecResultFunc.FillDicFromTXT(EvtDict, DataStrt, "/ta/work/user/hyomin/TAx4_rec/MC_KM/dumptest10/200215.183633.461929.txt")
EvtDict = RecResultFunc.FillDicFromTXT(EvtDict, DataStrt, "/ta/work/user/hyomin/TAx4_rec/MC_KM/dumptest10/200219.072258.332194.txt")

for Keys in DataStrt:
  for Key in Keys:
    print Key, EvtDict[Key]

#for EvtKey in EvtDict:
#  print EvtKey, EvtDict[EvtKey]
