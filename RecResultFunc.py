import numpy as np
import matplotlib.pyplot as plt
import HO2EQ
import re
import os, sys

def posSD(tower='KM'):
  if tower == 'KM':
    SD_POS_CLF = np.array([\
      372,-2.23655,30.0087,-0.0126319,\
      472,-0.518876,30.0453,-0.0270613,\
      473,-0.518738,31.7573,-0.0271477,\
      474,-0.590131,33.5066,-0.0122202,\
      475,-0.661486,35.2373,-0.00580588,\
      572,1.19876,30.1378,-0.0353633,\
      573,1.1269,31.8129,-0.0364999,\
      574,1.1266,33.5435,-0.0360407,\
      575,1.1263,35.2742,-0.0303383,\
      576,1.05451,37.0142,-0.0155926,\
      672,2.9164,30.1198,-0.0418,\
      673,2.91563,31.832,-0.0377101,\
      674,2.84331,33.581,-0.0439683,\
      675,2.84255,35.3209,-0.0391644,\
      676,2.77028,37.0886,-0.0256963,\
      677,3.0556,38.4864,-0.00241321,\
      772,4.70554,30.2321,-0.0207275,\
      773,4.63277,31.8885,-0.0417005,\
      774,4.55999,33.619,-0.0518194,\
      775,4.55877,35.3496,-0.0489738,\
      776,4.48606,37.0895,-0.0404554,\
      777,4.48486,38.8388,-0.023037,\
      872,6.35162,30.2337,0.0115378,\
      873,6.42139,31.9919,-0.0348718,\
      874,6.34818,33.6575,-0.0552708,\
      875,6.27497,35.3787,-0.0697395,\
      876,6.2733,37.1187,-0.0531159,\
      877,6.20015,38.8586,-0.0463455,\
      878,6.34187,40.1268,-0.0214162,\
      972,8.14084,30.2172,0.0173046,\
      973,8.06704,31.9567,-0.0254826,\
      974,8.06482,33.6964,-0.0628502,\
      975,7.99118,35.3805,-0.0806182,\
      976,7.98897,37.1573,-0.0920025,\
      977,7.91537,38.8879,-0.0871108,\
      978,7.91329,40.6281,-0.0489134,\
      1072,9.85833,30.2936,0.00304025,\
      1073,9.85569,31.9963,-0.0251734,\
      1074,10.3537,33.6066,-0.141242,\
      1075,9.77875,35.4661,-0.103516,\
      1076,9.70461,37.1965,-0.120954,\
      1077,9.702,38.9271,-0.127639\
    ], dtype=float)
  elif tower =='SN':
    SD_POS_CLF = np.array([\
      368,-2.107605,23.077671,0.01443476,\
      369,-1.697650,25.006109,-0.01419653,\
      370,-2.196760,26.534711,-0.00242511,\
      371,-2.225743,28.270407,-0.00124909,\
      467,-0.336054,21.292526,-0.01263958,\
      468,-0.383604,23.099894,-0.02426734,\
      469,-0.423651,24.841896,-0.02427923,\
      470,-0.455603,26.567981,-0.02204988,\
      471,-0.490380,28.309000,-0.02274595,\
      566,1.422665,19.678700,-0.01500884,\
      567,1.385632,21.413106,-0.03027004,\
      568,1.351825,23.144941,-0.03998009,\
      569,1.314775,24.875955,-0.03929291,\
      570,1.274206,26.609590,-0.03076664,\
      571,1.239383,28.343183,-0.03346707,\
      665,3.194467,17.978031,-0.02167133,\
      666,3.157106,19.713279,-0.03400016,\
      667,3.121006,21.444290,-0.03973070,\
      668,3.083907,23.183085,-0.04207670,\
      669,3.043332,24.913218,-0.04041709,\
      670,3.006974,26.647136,-0.04011873,\
      671,2.973243,28.371171,-0.03976120,\
      764,4.961696,16.280718,-0.02564169,\
      765,4.926846,18.012685,-0.03115210,\
      766,4.886673,19.750181,-0.03677752,\
      767,4.851323,21.482111,-0.04167112,\
      768,4.815848,23.218802,-0.04716808,\
      769,4.780063,24.950854,-0.04554526,\
      770,4.711887,26.695660,-0.02049859,\
      771,4.643820,28.379628,-0.02767643,\
      864,6.695372,16.321311,-0.03138135,\
      865,6.658642,18.055069,-0.03595574,\
      866,6.622073,19.787034,-0.04059082,\
      867,6.587787,21.522013,-0.04597363,\
      868,6.549067,23.255595,-0.04800443,\
      869,6.516325,25.031221,-0.02318262,\
      870,6.475938,26.720933,-0.00777103,\
      871,6.429235,28.448706,0.01235549,\
      964,8.453119,16.356181,-0.03639809,\
      965,8.391959,18.088764,-0.04170419,\
      966,8.359252,19.816201,-0.04584418,\
      967,8.327020,21.558063,-0.05105654,\
      968,8.281064,23.291565,-0.05518322,\
      969,8.246505,25.025052,-0.01278570,\
      970,8.238519,26.726107,0.01730067,\
      971,8.123770,28.500620,0.05497787,\
      1065,10.125572,18.126349,-0.04577274,\
      1066,10.088919,19.864305,-0.05153792,\
      1067,10.053330,21.593758,-0.05808207,\
      1068,10.015783,23.315661,-0.06351200,\
      1069,9.979758,25.061989,-0.06458624,\
      1070,9.945522,26.794044,-0.02351647,\
      1165,11.845465,18.187414,-0.04775604,\
      1166,11.862728,19.901653,-0.05464353,\
      1167,11.787604,21.632279,-0.06244678,\
      1168,11.747474,23.371417,-0.06788057,\
      1169,11.717089,25.098124,-0.07598105,\
      1170,11.810201,26.832082,-0.05848620,\
      1266,13.551677,20.071126,-0.05898894,\
      1267,13.521509,21.658288,-0.06593303,\
      1268,13.485382,23.408110,-0.07319460,\
      1269,13.448330,25.134134,-0.08000201,\
      1270,13.411266,26.864329,-0.08683432,\
      1271,13.710143,28.251539,-0.09369744,\
      1367,15.084951,21.709457,-0.06794300,\
      1368,15.197021,23.435103,-0.07349157,\
      1369,15.181598,24.946185,-0.08098352,\
      1370,14.771037,26.814852,-0.08928318,\
      1371,15.099900,28.783670,-0.09846182\
    ], dtype=float)
  elif tower == 'BF':
    SD_POS_CLF = np.array([\
      844,7.499640,-21.818123,-0.04495004,\
      845,7.461805,-20.078344,-0.04111452,\
      944,9.247049,-21.778328,-0.04760170,\
      945,9.198536,-20.046980,-0.03668016,\
      946,9.165618,-18.310309,-0.03969968,\
      1044,10.972769,-21.746203,-0.04965561,\
      1045,10.851273,-19.996529,-0.04621882,\
      1046,11.153172,-18.270904,-0.04049024,\
      1047,10.854928,-16.548869,-0.03731075,\
      1144,12.700056,-21.706669,-0.05457593,\
      1145,12.662825,-19.977331,-0.04955577,\
      1146,12.632123,-18.237414,-0.04363735,\
      1147,12.596507,-16.508830,-0.04008043,\
      1148,12.554171,-14.776087,-0.03737657,\
      1244,14.433792,-21.671173,-0.05712430,\
      1245,14.397645,-19.939510,-0.04328100,\
      1246,14.369227,-18.193595,-0.04709233,\
      1247,14.300178,-16.477787,-0.04436286,\
      1248,14.284421,-14.737853,-0.04103184,\
      1344,16.246102,-21.654981,-0.06361397,\
      1345,16.128714,-19.908990,-0.06042151,\
      1346,16.094414,-18.166313,-0.05680186,\
      1347,16.064234,-16.431846,-0.05353478,\
      1348,16.021947,-14.699150,-0.04198701,\
      1444,17.899185,-21.596963,-0.06822069,\
      1445,17.819444,-19.800589,-0.05285654,\
      1446,17.826546,-18.172880,-0.04959294,\
      1447,17.791965,-16.394131,-0.05705385,\
      1448,17.753480,-14.660951,-0.05286608,\
      1544,19.635688,-21.561886,-0.05773313,\
      1545,19.599373,-19.827985,-0.07018987,\
      1546,19.573752,-18.095109,-0.06108974,\
      1548,20.111926,-14.707110,-0.05922353,\
      1644,21.301478,-21.473043,-0.07096114,\
      1645,21.498079,-19.788774,-0.07632267,\
      1646,21.482446,-17.855089,-0.06854479,\
      1647,21.253150,-16.323655,-0.06708818,\
      1744,23.122919,-21.522746,-0.07335451,\
      1745,23.046635,-19.779573,-0.07094224,\
      1746,23.006860,-18.006821,-0.05827783,\
      1747,22.991213,-16.289845,-0.04886509,\
      1844,24.838684,-21.444758,-0.06682591,\
      1845,24.802092,-19.724893,-0.05719435,\
      1846,24.741787,-17.997917,-0.05361166,\
      1944,26.573589,-21.418467,-0.05590544,\
      1945,26.567961,-19.669069,-0.03326503\
    ], dtype=float)

  elif tower == 'MC':
    SD_POS_CLF = np.array([\
      101.0, -7.800000000, -7.800000000, 0.021000000,\
      102.0, -7.800000000, -6.066666667, 0.023333333,\
      103.0, -7.800000000, -4.333333333, 0.025000000,\
      104.0, -7.800000000, -2.600000000, 0.026166667,\
      105.0, -7.800000000, -0.866666667, 0.026666667,\
      106.0, -7.800000000, 0.866666667, 0.026666667,\
      107.0, -7.800000000, 2.600000000, 0.026166667,\
      108.0, -7.800000000, 4.333333333, 0.025000000,\
      109.0, -7.800000000, 6.066666667, 0.023333333,\
      110.0, -7.800000000, 7.800000000, 0.021000000,\
      201.0, -6.066666667, -7.800000000, 0.023333333,\
      202.0, -6.066666667, -6.066666667, 0.025583333,\
      203.0, -6.066666667, -4.333333333, 0.027250000,\
      204.0, -6.066666667, -2.600000000, 0.028416667,\
      205.0, -6.066666667, -0.866666667, 0.029000000,\
      206.0, -6.066666667, 0.866666667, 0.029000000,\
      207.0, -6.066666667, 2.600000000, 0.028416667,\
      208.0, -6.066666667, 4.333333333, 0.027250000,\
      209.0, -6.066666667, 6.066666667, 0.025583333,\
      210.0, -6.066666667, 7.800000000, 0.023333333,\
      301.0, -4.333333333, -7.800000000, 0.025000000,\
      302.0, -4.333333333, -6.066666667, 0.027250000,\
      303.0, -4.333333333, -4.333333333, 0.029000000,\
      304.0, -4.333333333, -2.600000000, 0.030083333,\
      305.0, -4.333333333, -0.866666667, 0.030666667,\
      306.0, -4.333333333, 0.866666667, 0.030666667,\
      307.0, -4.333333333, 2.600000000, 0.030083333,\
      308.0, -4.333333333, 4.333333333, 0.029000000,\
      309.0, -4.333333333, 6.066666667, 0.027250000,\
      310.0, -4.333333333, 7.800000000, 0.025000000,\
      401.0, -2.600000000, -7.800000000, 0.026166667,\
      402.0, -2.600000000, -6.066666667, 0.028416667,\
      403.0, -2.600000000, -4.333333333, 0.030083333,\
      404.0, -2.600000000, -2.600000000, 0.031250000,\
      405.0, -2.600000000, -0.866666667, 0.031833333,\
      406.0, -2.600000000, 0.866666667, 0.031833333,\
      407.0, -2.600000000, 2.600000000, 0.031250000,\
      408.0, -2.600000000, 4.333333333, 0.030083333,\
      409.0, -2.600000000, 6.066666667, 0.028416667,\
      410.0, -2.600000000, 7.800000000, 0.026166667,\
      501.0, -0.866666667, -7.800000000, 0.026666667,\
      502.0, -0.866666667, -6.066666667, 0.029000000,\
      503.0, -0.866666667, -4.333333333, 0.030666667,\
      504.0, -0.866666667, -2.600000000, 0.031833333,\
      505.0, -0.866666667, -0.866666667, 0.032333333,\
      506.0, -0.866666667, 0.866666667, 0.032333333,\
      507.0, -0.866666667, 2.600000000, 0.031833333,\
      508.0, -0.866666667, 4.333333333, 0.030666667,\
      509.0, -0.866666667, 6.066666667, 0.029000000,\
      510.0, -0.866666667, 7.800000000, 0.026666667,\
      601.0, 0.866666667, -7.800000000, 0.026666667,\
      602.0, 0.866666667, -6.066666667, 0.029000000,\
      603.0, 0.866666667, -4.333333333, 0.030666667,\
      604.0, 0.866666667, -2.600000000, 0.031833333,\
      605.0, 0.866666667, -0.866666667, 0.032333333,\
      606.0, 0.866666667, 0.866666667, 0.032333333,\
      607.0, 0.866666667, 2.600000000, 0.031833333,\
      608.0, 0.866666667, 4.333333333, 0.030666667,\
      609.0, 0.866666667, 6.066666667, 0.029000000,\
      610.0, 0.866666667, 7.800000000, 0.026666667,\
      701.0, 2.600000000, -7.800000000, 0.026166667,\
      702.0, 2.600000000, -6.066666667, 0.028416667,\
      703.0, 2.600000000, -4.333333333, 0.030083333,\
      704.0, 2.600000000, -2.600000000, 0.031250000,\
      705.0, 2.600000000, -0.866666667, 0.031833333,\
      706.0, 2.600000000, 0.866666667, 0.031833333,\
      707.0, 2.600000000, 2.600000000, 0.031250000,\
      708.0, 2.600000000, 4.333333333, 0.030083333,\
      709.0, 2.600000000, 6.066666667, 0.028416667,\
      710.0, 2.600000000, 7.800000000, 0.026166667,\
      801.0, 4.333333333, -7.800000000, 0.025000000,\
      802.0, 4.333333333, -6.066666667, 0.027250000,\
      803.0, 4.333333333, -4.333333333, 0.029000000,\
      804.0, 4.333333333, -2.600000000, 0.030083333,\
      805.0, 4.333333333, -0.866666667, 0.030666667,\
      806.0, 4.333333333, 0.866666667, 0.030666667,\
      807.0, 4.333333333, 2.600000000, 0.030083333,\
      808.0, 4.333333333, 4.333333333, 0.029000000,\
      809.0, 4.333333333, 6.066666667, 0.027250000,\
      810.0, 4.333333333, 7.800000000, 0.025000000,\
      901.0, 6.066666667, -7.800000000, 0.023333333,\
      902.0, 6.066666667, -6.066666667, 0.025583333,\
      903.0, 6.066666667, -4.333333333, 0.027250000,\
      904.0, 6.066666667, -2.600000000, 0.028416667,\
      905.0, 6.066666667, -0.866666667, 0.029000000,\
      906.0, 6.066666667, 0.866666667, 0.029000000,\
      907.0, 6.066666667, 2.600000000, 0.028416667,\
      910.0, 6.066666667, 7.800000000, 0.023333333,\
      1001.0, 7.800000000, -7.800000000, 0.021000000,\
      1002.0, 7.800000000, -6.066666667, 0.023333333,\
      1003.0, 7.800000000, -4.333333333, 0.025000000,\
      1004.0, 7.800000000, -2.600000000, 0.026166667,\
      1005.0, 7.800000000, -0.866666667, 0.026666667,\
      1006.0, 7.800000000, 0.866666667, 0.026666667,\
      1007.0, 7.800000000, 2.600000000, 0.026166667,\
      1008.0, 7.800000000, 4.333333333, 0.025000000,\
      1009.0, 7.800000000, 6.066666667, 0.023333333,\
      1010.0, 7.800000000, 7.800000000, 0.021000000\
    ], dtype=float)
  else:
    return 0

  SD_POS_CLF = SD_POS_CLF.reshape(len(SD_POS_CLF)/4,4).T

  SD_POS_CLF[1] = 1.2 * (SD_POS_CLF[1])
  SD_POS_CLF[2] = 1.2 * (SD_POS_CLF[2])

  return SD_POS_CLF[0], SD_POS_CLF[1], SD_POS_CLF[2]

def plotNpHist(npHist, ax, col = 'black', lab = '', txt=''):
  #print npHist[1]
  x = (npHist[1][1:] + npHist[1][:-1]) * 0.5
  x_err =(npHist[1][1:] - npHist[1][:-1]) * 0.5
  y = npHist[0]
  y_err = np.sqrt(y)

  #ax.bar(x, y, yerr = y_err, edgecolor=col, align='center', ecolor=col)
  if lab != '':
    ax.step(npHist[1][1:], y, color=col, label = lab)
  else:
    ax.step(npHist[1][1:], y, color=col)

  ax.errorbar(x, y, y_err, x_err, fmt='.', color=col, label = ("%s_err" % lab))

  #if lab != '':
  #  ax.legend()

  #if txt != '':
  #  ax.text(0.7, 0.9, txt, transform=ax.transAxes, fontsize=12)

# Input Evts is,
#Evts = [\
#  yymmdd, 	\ Evt[0]
#  hhmmss, 	\ Evt[1]
#  nstclust, 	\ Evt[2]
#  x_core_geo1, \ Evt[3]
#  y_core_geo1, \ Evt[4]
#  theta, 	\ Evt[5]
#  phi, 	\ Evt[6]
#  chi2_geo1, 	\ Evt[7]
#  ndof_geo1, 	\ Evt[8]
#  energy_ldf_log, \ Evt[9]
#  energy_ldf_log, \ Evt[10]
#  chi2_ldf, 	\ Evt[11]
#  ndof_ldf 	] Evt[12]

def drawDist(Evts, ct):
  # Some parameters for drawing
  chi2max = 20
  ndofmax = 20
  ndofmin = 0#int(round(np.min([Evts[8],Evts[12]])))

  # Define canvases and figure
  '''
  fig = plt.figure()
  ax1 = fig.add_subplot(3,3,1) # canvas for n of hit
  ax2 = fig.add_subplot(3,3,2) # canvas for chi2
  ax3 = fig.add_subplot(3,3,3) # canvas for ndof
  ax4 = fig.add_subplot(3,3,4) # canvas for x_core distribution
  ax5 = fig.add_subplot(3,3,5) # canvas for y_core distribution
  ax6 = fig.add_subplot(3,3,6) # canvas for x_core, y_core plot
  ax7 = fig.add_subplot(3,3,7) # canvas for theta distribution
  ax8 = fig.add_subplot(3,3,8) # canvas for phi distribution
  ax9 = fig.add_subplot(3,3,9) # canvas for energy distribution
  '''
  # Adjust canvas
  fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = plt.subplots(3, 3, figsize=(15,15))
  #fig.subplots_adjust(hspace=0.5)
  # Titles and x, y labels
  # ax1, n of hit
  ax1.set_title("N.O.H Dist.", fontsize=25)
  ax1.set_xlabel("N.O.H. in S-T cluster")
  ax1.set_ylabel("Number of Evts")
  ax1.set_yscale('log')

  # ax2, chi2
  ax2.set_title("Chi2 Dist.", fontsize=25)
  ax2.set_xlabel("Chi2")
  ax2.set_ylabel("Number of Evts")
  ax2.set_xlim(0, chi2max)
  ax2.set_yscale('log')

  # ax3, ndof
  ax3.set_title("N. of DOF Dist.", fontsize=25)
  ax3.set_xlabel("Ndof")
  ax3.set_ylabel("Number of Evts")
  ax3.set_xlim(ndofmin,ndofmax)
  ax3.set_yscale('log')

  # ax4, x_core
  ax4.set_title("X_core Dist.", fontsize=25)
  ax4.set_xlabel("X_core [km]")
  ax4.set_ylabel("Number of Evts")
  # ax5, y_core
  ax5.set_title("Y_core Dist.", fontsize=25)
  ax5.set_xlabel("Y_core [km]")
  ax5.set_ylabel("Number of Evts")

  # ax6, core scatter plot
  ax6.set_title("Core Position Scatter Plot", fontsize=25)
  ax6.set_xlabel("X_core [km]")
  ax6.set_ylabel("Y_core [km]")
  #ax6.set_ylim(35, 52)

  # ax7, theta
  ax7.set_title("Theta Dist.", fontsize=25)
  ax7.set_xlabel("Theta [degree]")
  ax7.set_ylabel("Number of Evts")
  ax7.set_xlim(0,90)

  # ax8, phi
  ax8.set_title("Phi Dist.", fontsize=25)
  ax8.set_xlabel("Phi [degree]")
  ax8.set_ylabel("Number of Evts")
  ax8.set_xlim(0,360)

  # ax9, eLog
  ax9.set_title("Log(E) Dist.", fontsize=25)
  ax9.set_xlabel("log(E/EeV)")
  ax9.set_ylabel("Number of Evts")

  fig.tight_layout()
  # Histogram of n of hits
  nOfHit = np.histogram(Evts[2], bins = range(15))
  plotNpHist(nOfHit, ax1, txt=('Entry=%d' % len(Evts[2])))

  # bin for chi2
  chi2bin = np.array(range(chi2max + 1))

  chi2_geo1 = np.histogram(Evts[7], bins=chi2bin)
  # Count the number of evtnts, greater then chi2 manimum
  add_chi2_geo1 = 0
  for chi2 in Evts[7]:
    if chi2 > chi2max: add_chi2_geo1 += 1
  chi2_geo1[0][-1] += add_chi2_geo1

  chi2_ldf = np.histogram(Evts[11], bins=chi2bin)
  # Count the number of evtnts, greater then chi2 manimum
  add_chi2_ldf = 0
  for chi2 in Evts[11]:
    if chi2 > chi2max: add_chi2_ldf += 1
  chi2_ldf[0][-1] += add_chi2_ldf

  # Draw chi2 dist.
  plotNpHist(chi2_geo1, ax2, lab = 'Geom')
  plotNpHist(chi2_ldf, ax2, 'blue', lab = 'LDF')

  # bin for ndof
  ndofbin = np.arange(ndofmin,ndofmax + 1,1)

  ndof_geo1 = np.histogram(Evts[8], bins=ndofbin)

  # Count the number of evtnts, greater then chi2 manimum
  add_ndof_geo1 = 0
  for ndof in Evts[8]:
    if ndof > ndofmax: add_ndof_geo1 += 1
  ndof_geo1[0][-1] += add_ndof_geo1

  ndof_ldf = np.histogram(Evts[12], bins=ndofbin)

  # Count the number of evtnts, greater then chi2 manimum
  add_ndof_ldf = 0
  for ndof in Evts[12]:
    if ndof > ndofmax: add_ndof_ldf += 1
  ndof_ldf[0][-1] += add_ndof_ldf

  plotNpHist(ndof_geo1, ax3, lab='Geom')
  plotNpHist(ndof_ldf, ax3, 'blue', lab='LDF')

  # conver x, y core to km
  x_core_geo1_km = (np.array(Evts[3]) - 12.2435) * 1.2
  y_core_geo1_km = (np.array(Evts[4]) - 16.4406) * 1.2
  x_core_geo1 = np.histogram(x_core_geo1_km, bins=10)
  #  bins=np.arange(int(np.min(x_core_geo1_km)) -1), int(np.max(x_core_geo1_km)+1),1))
  y_core_geo1 = np.histogram(y_core_geo1_km, bins=10)
  #  bins=np.arange(int(np.min(y_core_geo1_km) -1), int(np.max(y_core_geo1_km)+1),1))

  plotNpHist(x_core_geo1, ax4)
  plotNpHist(y_core_geo1, ax5)
  #ax5.set_xlim(int(np.min(y_core_geo1_km) -1), int(np.max(y_core_geo1_km)+1))

  # Draw SD position
  SD_ID, SD_POS_X_km, SD_POS_Y_km = posSD(ct)
  #ax6.scatter(SD_POS_X_km, SD_POS_Y_km, marker="s", color='blue', s=8, label='SD')
  #ax6.scatter(x_core_geo1_km, y_core_geo1_km, marker = '.', color='red', s=1, label='Core position')
  ax6.plot(SD_POS_X_km, SD_POS_Y_km, marker='s', linestyle='None', color='blue', markersize=8, label='SD')
  ax6.plot(x_core_geo1_km, y_core_geo1_km, marker = '.', linestyle='None', color='red', markersize=1, label='Core position')
  ax6.legend(numpoints=1, fontsize=10)


  thetaHist = np.histogram(Evts[5], bins=np.arange(0,100,10))
  phiHist = np.histogram(Evts[6], bins=np.arange(0,370,30))
  elogHist = np.histogram(Evts[10], bins=np.arange(-2.5,3.5,0.5))

  plotNpHist(thetaHist, ax7)
  plotNpHist(phiHist, ax8)
  plotNpHist(elogHist, ax9)

# Function for Quality Cut - Old vertion
# Remade for Event dictionary form
'''
def QC(Evts, varName, condition, thr):

  varNames = {
    'yymmdd':0,\
    'hhmmss':1,\
    'nstclust':2,\
    'x_core_geo1':3,\
    'y_core_geo1':4,\
    'theta':5,\
    'phi':6,\
    'chi2_geo1':7,\
    'ndof_geo1':8,\
    'energy_ldf':9,\
    'energy_ldf_log':10,\
    'chi2_ldf':11,\
    'ndof_ldf':12,\
    't0_gldf':13, \
    'xcore_gldf':14, \
    'ycore_gldf':15, \
    'theta_gldf':16, \
    'phi_gldf':17, \
    'energy_gldf':18, \
    'chi2_gldf':19, \
    'ndof_gldf':20,\
    'xcore_MC':21, \
    'ycore_MC':22, \
    'energy_MC':23,\
    'theta_MC':24,\
    'phi_MC':25 }

  varIndex = varNames.get(varName)
  print "Quality Cut for", varName, condition, thr, "is applied"

  # Cut out index
  cutOutIndex = []
  for i in range(len(Evts[0])):
    if condition == 'GT':
      if Evts[varIndex][i] > thr:
        cutOutIndex.append(i)
    if condition == 'GE':
      if Evts[varIndex][i] >= thr:
        cutOutIndex.append(i)
    if condition == 'LT':
      if Evts[varIndex][i] < thr:
        cutOutIndex.append(i)
    if condition == 'LE':
      if Evts[varIndex][i] <= thr:
        cutOutIndex.append(i)
    if condition == 'EQ':
      if Evts[varIndex][i] == thr:
        cutOutIndex.append(i)


  if len(cutOutIndex) != 0:
    for delIndex in reversed(cutOutIndex):
      #print delIndex, 'th event will be deleted'
      for j in range(len(Evts)):
        #print j, Evts[j][delIndex],
        Evts[j].pop(delIndex)
      #print '\n'

  return Evts
'''

# Quality cut
def QC(EvtDict, varName, condition, thr):

  EvtDictAlive = {}
  for key in EvtDict: EvtDictAlive[key] = []

  print "Quality cut,", varName, condition, thr, "will remained"
  
  for i in range(len(EvtDict[varName])):
    if condition == 'GT':
      if float(EvtDict[varName][i]) >  thr:
        for key in EvtDict: EvtDictAlive[key].append(EvtDict[key][i])
    if condition == 'GE':
      if float(EvtDict[varName][i]) >= thr:
        for key in EvtDict: EvtDictAlive[key].append(EvtDict[key][i])
    if condition == 'LT':
      if float(EvtDict[varName][i]) <  thr:
        for key in EvtDict: EvtDictAlive[key].append(EvtDict[key][i])
    if condition == 'LE':
      if float(EvtDict[varName][i]) <= thr:
        for key in EvtDict: EvtDictAlive[key].append(EvtDict[key][i])
    if condition == 'EQ':
      if float(EvtDict[varName][i]) == thr:
        for key in EvtDict: EvtDictAlive[key].append(EvtDict[key][i])

  return EvtDictAlive



# Function for print out
def PO(Evts, varName, condition, thr, output=''):

  varNames = {
    'yymmdd':0,\
    'hhmmss':1,\
    'nstclust':2,\
    'x_core_geo1':3,\
    'y_core_geo1':4,\
    'theta':5,\
    'phi':6,\
    'chi2_geo1':7,\
    'ndof_geo1':8,\
    'energy_ldf':9,\
    'energy_ldf_log':10,\
    'chi2_ldf':11,\
    'ndof_ldf':12,\
    'chi2_gldf':13,\
    'ndof_gldf':14 }

  varIndex = varNames.get(varName)
  print "Print out", varName, condition, thr

  # Print out index
  printOutIndex = []
  for i in range(len(Evts[0])):
    if condition == 'GT':
      if Evts[varIndex][i] > thr:
        printOutIndex.append(i)
    if condition == 'GE':
      if Evts[varIndex][i] >= thr:
        printOutIndex.append(i)
    if condition == 'LT':
      if Evts[varIndex][i] < thr:
        printOutIndex.append(i)
    if condition == 'LE':
      if Evts[varIndex][i] <= thr:
        printOutIndex.append(i)
    if condition == 'EQ':
      if Evts[varIndex][i] == thr:
        printOutIndex.append(i)


  if len(printOutIndex) != 0:
    for Index in printOutIndex:
      #print delIndex, 'th event will be deleted'
      for j in range(len(Evts)):
        print Evts[j][Index],
      print '\n'

  if output != '':
    if len(printOutIndex) != 0:
      for Index in printOutIndex:
        #print delIndex, 'th event will be deleted'
        for j in range(len(Evts)):
          print>>output, Evts[j][Index],
        print>>output, '\n'

# Draw core and SD position scatter plot on given canvas
def CoreMap(SD_POS_X_km, SD_POS_Y_km, x_core_km, y_core_km, ax):
  ax.plot(SD_POS_X_km, SD_POS_Y_km, marker='s', linestyle='None', color='blue', markersize=8, label='SD')
  ax.plot(x_core_geo1_km, y_core_geo1_km, marker = '.', linestyle='None', color='red', markersize=1, label='Core position')
  ax.legend(numpoints=1, fontsize=10)
 
# Compare MC thrown and reconstructed core map
#Evts = [\
#  yymmdd, \
#  hhmmss, \
#  nstclust, \
#  x_core_geo1, \
#  y_core_geo1, \
#  theta, \
#  phi, \
#  chi2_geo1, \
#  ndof_geo1, \
#  energy_ldf, \
#  energy_ldf_log, \
#  chi2_ldf, \
#  ndof_ldf, \
#  chi2_gldf, \
#  ndof_gldf, \
#  xcore_MC, \
#  ycore_MC, \
#  energy_MC , \
#  theta_MC, \
#  phi_MC ]
def CompCoreMap(Evts, alpha=0.5):
  # Make convas [MC_thrown, reconstructed]
  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))
  SD_ID, SD_POS_X_km, SD_POS_Y_km = posSD('MC')

  ax1.plot(SD_POS_X_km, SD_POS_Y_km, marker='s', linestyle='None', color='blue', markersize=8, label='SD')
  ax2.plot(SD_POS_X_km, SD_POS_Y_km, marker='s', linestyle='None', color='blue', markersize=8, label='SD')

  x_core_geo1_km = (np.array(Evts[3]) - 12.2435) * 1.2
  y_core_geo1_km = (np.array(Evts[4]) - 16.4406) * 1.2

  x_core_MC_km = (np.array(Evts[15])) * 1.2
  y_core_MC_km = (np.array(Evts[16])) * 1.2

  ax1.plot(x_core_MC_km, y_core_MC_km, marker = '.', linestyle='None', color='red', markersize=1, label='Core position', alpha=alpha)
  ax2.plot(x_core_geo1_km, y_core_geo1_km, marker = '.', linestyle='None', color='red', markersize=1, label='Core position', alpha=alpha)

  ax1.legend(numpoints=1, fontsize=10)
  ax2.legend(numpoints=1, fontsize=10)

  #plt.show()
def plot_mwd(ax, org=180):
    #RA,Dec,org=0,title='Mollweide projection', projection='mollweide'):
    ''' RA, Dec are arrays of the same length.
    RA takes values in [0,360), Dec in [-90,90],
    which represent angles in degrees.
    org is the origin of the plot, 0 or a multiple of 30 degrees in [0,360).
    title is the title of the figure.
    projection is the kind of projection: 'mollweide', 'aitoff', 'hammer', 'lambert'
    '''
    #x = np.remainder(RA+360-org,360) # shift RA values
    #ind = x>180
    #x[ind] -=360    # scale conversion to [-180, 180]
    #x=-x    # reverse the scale: East to the left
    tick_labels = np.array([150, 120, 90, 60, 30, 0, 330, 300, 270, 240, 210])
    tick_labels = np.remainder(tick_labels+360+org,360)
    #fig = plt.figure(figsize=(10, 5))
    #ax = fig.add_subplot(111, projection=projection, axisbg ='LightCyan')
    #ax.scatter(np.radians(x),np.radians(Dec))  # convert degrees to radians
    ax.set_xticklabels(tick_labels)     # we add the scale on the x axis
    #ax.set_title(title)
    #ax.title.set_fontsize(15)
    ax.set_xlabel("RA")
    ax.xaxis.label.set_fontsize(12)
    ax.set_ylabel("Dec")
    ax.yaxis.label.set_fontsize(12)
    ax.grid(True)

def plotRaDecMap(Evts, ax, color='k', ct='', org=180):
  Evts_np = np.array(Evts).T
  
  ra_rad = []
  dec_rad = []
  for Evt in Evts_np:
    ra_deg, dec_deg = HO2EQ.HO2EQ(float(Evt[5]), float(Evt[6]), Evt[0], Evt[1])
    # Shift and rotate to fit origin
    ra_deg = (ra_deg - org) % 360
    if ra_deg>180: ra_deg -= 360
    ra_deg = -ra_deg
    # ra from 0 to 360
    #ra_deg = (ra_deg + 180) % 360 - 180
    ra_rad.append(np.deg2rad(ra_deg))
    dec_rad.append(np.deg2rad(dec_deg))
  #print ra_deg, dec_deg

  ax.scatter(ra_rad, dec_rad, marker='o', s=15, c=color, label=ct)

# Compare MC thrown and reconstructed
# Evts = [\
#    yymmdd, hhmmss, nstclust, \
#    x_core_geo1, y_core_geo1, theta, phi, chi2_geo1, ndof_geo1, \
#    energy_ldf, energy_ldf_log, chi2_ldf, ndof_ldf,\
#    x_core_gldf, y_core_gldf, theta_gldf, phi_gldf, energy_gldf, chi2_gldf, ndof_gldf, \
#    xcore_MC, ycore_MC, energy_MC, theta_MC, phi_MC\
#    ]
def CompMC(Evts):
  Evts = np.array(Evts, dtype=np.float)
  print(Evts[9][Evts[9] > 0])
  print("LDF/GLDF/Thrown events are %3d/%3d/%3d" % (\
    len(Evts[9][Evts[9] > 0]), \
    len(Evts[17][Evts[17] > 0]), \
    len(Evts[22])\
  ))

  # Make canvas for MC thrown, reconstruction
  fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(10,15))

  # ax1, number of events with log10(E)
  energyThrHist = np.histogram(np.log10(Evts[22]), bins=np.arange(0, 4, 0.20))
  energyLDFHist = np.histogram(np.log10(Evts[9][Evts[9] > 0]), bins=np.arange(0, 4, 0.20)) # reconstructed only
  energyGLDFHist = np.histogram(np.log10(Evts[17][Evts[17] > 0]), bins=np.arange(0, 4, 0.20))

  plotNpHist(energyThrHist, ax1, col='black', lab='Thr')
  plotNpHist(energyLDFHist, ax1, col='red', lab="LDF")
  plotNpHist(energyGLDFHist, ax1, col='blue', lab="GLDF")

  ax1.set_yscale('log')
  ax1.set_ylim(bottom = 0.1)
  #ax1.legend()
  #plt.show()

  # Make efficiency
  nofRecLDFHist = np.histogram(np.log10(Evts[22][Evts[9]>0]), bins=np.arange(0, 4, 0.20))
  nofRecGLDFHist = np.histogram(np.log10(Evts[22][Evts[17]>0]), bins=np.arange(0, 4, 0.20))
  #print nofRecLDFHist
  #print energyThrHist
  effLDF = 1. * nofRecLDFHist[0]/ (energyThrHist[0] + 1.e-8)
  effGLDF = 1. * nofRecGLDFHist[0]/ (energyThrHist[0] + 1.e-8)


  ax2.plot(0.5 * (energyThrHist[1][:-1] + energyThrHist[1][1:]), effLDF)
  ax2.plot(0.5 * (energyThrHist[1][:-1] + energyThrHist[1][1:]), effGLDF)

  # Make energy resolution = (E_rec - E_thr)/E_thr

  energyThr = Evts[22][Evts[9] > 0]
  energyLDF = Evts[9][Evts[9] > 0]
  energyGLDF= Evts[17][Evts[9] > 0]

  eResLDF = 1. * (energyLDF - energyThr)/energyThr
  eResGLDF= 1. * (energyGLDF - energyThr)/energyThr

  eResLDFHist = np.histogram(eResLDF, bins=np.arange(-0.5, 0.5, 0.025))
  eResGLDFHist = np.histogram(eResGLDF, bins=np.arange(-0.5, 0.5, 0.025))

  plotNpHist(eResLDFHist, ax3, col='red')
  plotNpHist(eResGLDFHist, ax3, col='blue')

  print("LDF Mean Energy resolution is  %.2f +/- %.2f" % (np.mean(eResLDF), np.std(eResLDF)))
  print("GLDF Mean Energy resolution is  %.2f +/- %.2f" % (np.mean(eResGLDF), np.std(eResGLDF)))

  # Make core map
  x_core_MC_km = (np.array(Evts[20]) - 12.2435) * 1.2
  y_core_MC_km = (np.array(Evts[21]) - 16.4406) * 1.2
  SD_ID, SD_POS_X_km, SD_POS_Y_km = posSD("KM")
  ax4.plot(x_core_MC_km, y_core_MC_km, marker = '.', linestyle='None', color='red', markersize=1)
  ax4.plot(SD_POS_X_km, SD_POS_Y_km, marker='s', linestyle='None', color='blue', markersize=8, label='SD')


  # Make delta theta distrivution

  thetaThr  = Evts[23][Evts[9]>0]
  thetaLDF  = Evts[5][Evts[9]>0]
  thetaGLDF = Evts[15][Evts[9]>0]

  dthetaLDF = thetaLDF - thetaThr
  dthetaGLDF = thetaGLDF - thetaThr

  dthetaLDFHist = np.histogram(dthetaLDF, bins=np.arange(-10, 10, 0.5))
  dthetaGLDFHist = np.histogram(dthetaGLDF, bins=np.arange(-10, 10, 0.5))

  plotNpHist(dthetaLDFHist, ax5, col='red')
  plotNpHist(dthetaGLDFHist, ax5, col='blue')

  print("GEOM Mean dtheta is %.2f +/- %.2f" % (np.mean(dthetaLDF), np.std(dthetaLDF)))
  print("GLDF Mean dtheta is %.2f +/- %.2f" % (np.mean(dthetaGLDF), np.std(dthetaGLDF)))

  # Make delta phi distrivution

  phiThr  = Evts[24][Evts[9]>0]
  phiLDF  = Evts[6][Evts[9]>0]
  phiGLDF = Evts[16][Evts[9]>0]

  dphiLDF = (phiLDF - phiThr - 180) % 360 - 180 # Phi range to [-180, 180]
  dphiGLDF = (phiGLDF - phiThr - 180) % 360 - 180 # Phi range to [-180, 180]

  dphiLDFHist = np.histogram(dphiLDF, bins=np.arange(-10, 10, 0.5))
  dphiGLDFHist = np.histogram(dphiGLDF, bins=np.arange(-10, 10, 0.5))

  plotNpHist(dphiLDFHist, ax6, col='red')
  plotNpHist(dphiGLDFHist, ax6, col='blue')

  print("GEOM Mean dphi is %.2f +/- %.2f" % (np.mean(dphiLDF), np.std(dphiLDF)))
  print("GLDF Mean dphi is %.2f +/- %.2f" % (np.mean(dphiGLDF), np.std(dphiGLDF)))


  '''
  # Make canvas for MC thrown, reconstruction
  # [[ MC_core, Rec_core],\
  #  [ Theta  , phi     ],\
  #  [ dTheta , dPhi    ] ]
  fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(10,15))

  thetaRecHist = np.histogram(Evts[5], bins=np.arange(0,90,10))
  thetaMCHist = np.histogram(Evts[18], bins=np.arange(0,90,10))
  phiRecHist = np.histogram(Evts[6], bins=np.arange(0,360,36))
  phiMCHist = np.histogram(Evts[19], bins=np.arange(0,360,36))

  #plotNpHist(npHist, ax, col = 'black', lab = '', txt=''):

  plotNpHist(thetaRecHist, ax3, lab = 'reconstructed')
  plotNpHist(thetaMCHist, ax3, col = 'red', lab = 'thrown')
  plotNpHist(phiRecHist, ax4, lab = 'reconstructed')
  plotNpHist(phiMCHist, ax4, col = 'red', lab = 'thrown')

  dtheta = np.array(Evts[5]) - np.array(Evts[18])
  dphi = np.array(Evts[6]) - np.array(Evts[19]) # need to improve!

  dthetaHist = np.histogram(dtheta, bins = 20)
  dphiHist = np.histogram(dphi, bins = 20)

  plotNpHist(dthetaHist, ax5)
  plotNpHist(dphiHist, ax6)

  print("Mean dTheta = %5.3f" % np.mean(dtheta))
  '''

def EvtsFromDSTDump(DSTFile, Evts = []):

  if Evts == []:
    yymmdd = []
    hhmmss = []
    nstclust = []
    x_core_geo1 = []
    y_core_geo1 = []
    theta = []
    phi = []
    chi2_geo1 = []
    ndof_geo1 = []
    energy_ldf = []
    energy_ldf_log = []
    chi2_ldf = []
    ndof_ldf = []
    x_core_gldf = []
    y_core_gldf = []
    theta_gldf = []
    phi_gldf = []
    energy_gldf = []
    chi2_gldf = []
    ndof_gldf = []
    xcore_MC = []
    ycore_MC = []
    energy_MC = []
    theta_MC = []
    phi_MC = []

  else:
    yymmdd, hhmmss, nstclust, \
    x_core_geo1, y_core_geo1, theta, phi, chi2_geo1, ndof_geo1, \
    energy_ldf, energy_ldf_log, chi2_ldf, ndof_ldf, \
    x_core_gldf, y_core_gldf, theta_gldf, phi_gldf, energy_gldf, chi2_gldf, ndof_gldf, \
    xcore_MC, ycore_MC, energy_MC, theta_MC, phi_MC\
      = Evts
 

  dumpFile = open(DSTFile, 'r')

  n = 0

  while 1:
    line = dumpFile.readline()

    #print line[:33]

    # Events data start, initialize event data
    if line == "START OF EVENT ***********************************************************\n":
      n+=1
      #print "READING a EVT"

      yymmdd_tmp = '000000' #float(0)
      hhmmss_tmp = '000000' #float(0)
      nstclust_tmp = int(0) #float(0)
      x_core_geo1_tmp = float(0)
      y_core_geo1_tmp = float(0)
      theta_tmp = float(0)
      phi_tmp = float(0)
      chi2_geo1_tmp = float(0)
      ndof_geo1_tmp = float(0)
      chi2_ldf_tmp = float(0)
      ndof_ldf_tmp = float(0)
      energy_ldf_tmp = float(0)
      energy_ldf_log_tmp = float(0)
      x_core_gldf_tmp = float(0)
      y_core_gldf_tmp = float(0)
      theta_gldf_tmp = float(0)
      phi_gldf_tmp = float(0)
      energy_gldf_tmp = float(0)
      chi2_gldf_tmp = float(0)
      ndof_gldf_tmp = float(0)
      xcore_MC_tmp = float(0)
      ycore_MC_tmp = float(0)
      energy_MC_tmp = float(0)
      theta_MC_tmp = float(0)
      phi_MC_tmp = float(0)

    # Events data end, fill up event data
    if line == "END OF EVENT *************************************************************\n":
      yymmdd.append(yymmdd_tmp)
      hhmmss.append(hhmmss_tmp)
      nstclust.append(nstclust_tmp)
      x_core_geo1.append(x_core_geo1_tmp)
      y_core_geo1.append(y_core_geo1_tmp)
      theta.append(theta_tmp)
      phi.append(phi_tmp)
      chi2_geo1.append(chi2_geo1_tmp)
      ndof_geo1.append(ndof_geo1_tmp)
      chi2_ldf.append(chi2_ldf_tmp)
      ndof_ldf.append(ndof_ldf_tmp)
      energy_ldf.append(energy_ldf_tmp)
      energy_ldf_log.append(energy_ldf_log_tmp)
      x_core_gldf.append(x_core_gldf_tmp)
      y_core_gldf.append(y_core_gldf_tmp)
      theta_gldf.append(theta_gldf_tmp)
      phi_gldf.append(phi_gldf_tmp)
      energy_gldf.append(energy_gldf_tmp)
      chi2_gldf.append(chi2_gldf_tmp)
      ndof_gldf.append(ndof_gldf_tmp)
      xcore_MC.append(xcore_MC_tmp)
      ycore_MC.append(ycore_MC_tmp)
      energy_MC.append(energy_MC_tmp)
      theta_MC.append(theta_MC_tmp)
      phi_MC.append(phi_MC_tmp)

    # read MC data
    if line.startswith("Total Energy of Primary Particle:"):
      energy_MC_tmp = float(line.split(" ")[5])
    if line.startswith("Zenith Angle of Primary Particle Direction:"):
      theta_MC_tmp = float(line.split(" ")[6])
    if line.startswith("Azimuth Angle of Primary Particle Direction:"):
      phi_MC_tmp = float(line.split(" ")[6])
    if line.startswith("errcode"):
      yymmdd_tmp = float(line.split(" ")[8])
      hhmmss_tmp = float(line.split(" ")[10].rstrip("\n"))
    if line.startswith("rusdmc1"):
      line = dumpFile.readline()
      xcore_MC_tmp = float(line.split(" ")[1])
      ycore_MC_tmp = float(line.split(" ")[3])

    # read rufptn
    if line.startswith("rufptn"):
      line = dumpFile.readline()
      nstclust_tmp = float(line.split(" ")[5])

    # read rusdgeom
    if line.startswith("rusdgeom"):
      # nsds information
      line = dumpFile.readline()
      # Plain fit infomation
      line = dumpFile.readline()
      # Modified Linsley fit infomation
      line = dumpFile.readline()
      #print line.split(" ")
      x_core_geo1_tmp = float(line.split(" ")[4].split("+/-")[0].split("=")[1])
      y_core_geo1_tmp = float(line.split(" ")[5].split("+/-")[0].split("=")[1])
      theta_tmp = float(line.split(" ")[7].split("+/-")[0].split("=")[1])
      phi_tmp = float(line.split(" ")[8].split("+/-")[0].split("=")[1])
      chi2_geo1_tmp = float(line.split(" ")[9].split("=")[1])
      ndof_geo1_tmp = float(line.split(" ")[10].split("=")[1])

      
      #ycore_geo1_tmp = float(line.split(" ")[2]
      # core position, need to be improved later

    # read rufldf
    if line.startswith("rufldf"):
      # info from ldf
      line = dumpFile.readline()
      energy_ldf_tmp = float(line.split(" ")[11])
      if energy_ldf_tmp > 0:
        energy_ldf_log_tmp = np.log10(energy_ldf_tmp)
      chi2_ldf_tmp = float(line.split(" ")[13])
      ndof_ldf_tmp = float(line.split(" ")[15])
      # info from gldf
      line = dumpFile.readline()
      x_core_gldf_tmp = float(line.split(" ")[1])
      y_core_gldf_tmp = float(line.split(" ")[5])
      energy_gldf_tmp = float(line.split(" ")[11])
      chi2_gldf_tmp = float(line.split(" ")[13])
      ndof_gldf_tmp = float(line.split(" ")[15])
      line = dumpFile.readline()
      theta_gldf_tmp = float(line.split(" ")[1])
      phi_gldf_tmp = float(line.split(" ")[5])

    # End of File
    if line == '':
      break

  # Take out event data
  print n
  Evts = [\
    yymmdd, hhmmss, nstclust,\
    x_core_geo1, y_core_geo1, theta, phi, chi2_geo1, ndof_geo1,\
    energy_ldf, energy_ldf_log,chi2_ldf, ndof_ldf, \
    x_core_gldf, y_core_gldf, theta_gldf, phi_gldf, energy_gldf, chi2_gldf, ndof_gldf,\
    xcore_MC, ycore_MC, energy_MC, theta_MC, phi_MC\
  ]
  return Evts

def ReadDicStructure(DumpScriptFile = "/ta/work/user/hyomin/sdanalysis_2018_TALE_TAx4SingleCT_KM/dst2k-ta/DumpEvtAll.c"):
  DumpScript = open(DumpScriptFile, 'r')

  reading = True
  RecStart = False

  EvtDict = {}
  DataStrt = []
  print("Data structure from %s" % DumpScriptFile)
  while reading:
    line = DumpScript.readline()
    #print line
    if line == "":
      reading = False

    line = line.strip('\n').strip()
    if line == "/* Printout Reconstruction start */":
      RecStart = True
    if line == "/* Printout Reconstruction end */":
      RecStart = False
    if RecStart: 
      #print line.strip()
      if line.strip().startswith('"'):
        bName = line.split("\\t")[0][1:]
        print bName, ":",
        DataStrt.append([])
        #print line
        elLine=DumpScript.readline()[:-3]
        #print elLine
        for element in elLine.strip().split(','):
          eleName = element.split('.')[1].split('[')[0]
          print eleName,
          DictKey = ("%s_%s" % (eleName, bName))
          DataStrt[-1].append(DictKey)
          EvtDict[DictKey] = []
        print

  return EvtDict, DataStrt

def FillDicFromTXT(EvtDict, DataStrt, EvtTXTFile):
  '''
  EvtTXTLines = open(EvtTXTFile, 'r').readlines()
  for i in range(len(DataStrt)):
    line = EvtTXTLines[i]
    for j in range(len(DataStrt[i])):
      #print line.strip('\n').split('\t')[j+1],
      EvtDict[DataStrt[i][j]].append(line.strip('\n').split('\t')[j+1])
    #print
   '''

  # Changed to use grep
  for i in range(len(DataStrt)):
    bName = DataStrt[i][0].split('_')[-1]
    cmd = "grep '^%s' %s" % (bName, EvtTXTFile)
    dataLine = os.popen(cmd).read().split('\t')[1:]
    #print dataLine
    for j in range(len(DataStrt[i])):
      EvtDict[DataStrt[i][j]].append(dataLine[j])
  return EvtDict
    
def SDIDtoCLF(SDID, sdxyzclf_raw="/ta/work/user/hyomin/sdanalysis_2018_TALE_TAx4SingleCT_KM/inc/sdxyzclf_raw.h"):

  cmd = 'grep "^  %s" %s' % (SDID, sdxyzclf_raw)
  SDIDCLFLine = os.popen(cmd).read().split("\n")[0].split(',')[1:4]
  #print SDIDCLFLine
  return SDIDCLFLine 

def LineSDIDtoCLF(LineSDID, sdxyzclf_raw="/ta/work/user/hyomin/sdanalysis_2018_TALE_TAx4SingleCT_KM/inc/sdxyzclf_raw.h"):
  edgeLineCLF=[]
  for lineSeg in LineSDID:
    edgeLineCLF.append([SDIDtoCLF(lineSeg[0]), SDIDtoCLF(lineSeg[1])])
  return np.array(edgeLineCLF, dtype=np.float)

def SDedgeIDs(sdEdgeFile = "/ta/work/user/hyomin/sdanalysis_2018_TALE_TAx4SingleCT_KM/sduti/sdparamborder.c"):
  edEdgeLines = open(sdEdgeFile, 'r')

  eof = False
  edgeStart = False
  edgeLineSDID = []
  while ~eof:
    line=edEdgeLines.readline()
    #print line
    if line=='':
      eof=True
    if not line: break
    if line.startswith("static double sdedgelinesRAW"):
      line=edEdgeLines.readline()
      edgeStart = True
    if edgeStart:
      #print line
      if line.startswith("    {"):
        SDIDYY1, SDIDXX1, SDIDYY2, SDIDXX2 = re.findall("\d+", line)#line.strip().strip('{').strip('}').split(',')
        #edgeLineSDID.append([[SDIDYY1, SDIDXX1],[SDIDYY2, SDIDXX2]])
        edgeLineSDID.append(["%s%s" % (SDIDYY1, SDIDXX1),"%s%s" % (SDIDYY2, SDIDXX2)])

        #print SDIDYY1, SDIDXX1, SDIDYY2, SDIDXX2
        #print line.strip().strip('{').strip('}').strip("\n").split(',')
        #break
      if line.startswith("  };"):
        edgeStart = False
        eof=True
  return edgeLineSDID

def plotLoop(cLoop, ax):
  for line in cLoop:
    ax.plot(line.T[0], line.T[1], marker='o', color='black')

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


def cross(point, lineSeg):
  # calculate a, b of y=ax+b of line segment
  delta = lineSeg[1] - lineSeg[0]
  a = delta[1]/delta[0]
  b = lineSeg[1][1] - a * lineSeg[1][0]
  print lineSeg, a, b
  # node
  x = point[0]
  y = a * x + b
  print x, y, lineSeg.T
  if y <= max(lineSeg.T[1]) and y >= min(lineSeg.T[1]):
    return 1
  else:
    return 0

def inLoop(point, cLoop):
  nofCross = 0
  for lineSeg in cLoop:
    if intersect(point, [1.e6, 0], lineSeg[0], lineSeg[1]):
      nofCross += 1
  return nofCross % 2
