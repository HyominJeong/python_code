import numpy as np
import datetime
import math

# example_datetime = datetime.datetime(1877, 8, 11, 7, 30, 0)
def get_julian_datetime(date):
    """
    Convert a datetime object into julian float.
    Args:
        date: datetime-object of date in question

    Returns: float - Julian calculated datetime.
    Raises: 
        TypeError : Incorrect parameter type
        ValueError: Date out of range of equation
    """

    # Ensure correct format
    if not isinstance(date, datetime.datetime):
        raise TypeError('Invalid type for parameter "date" - expecting datetime')
    elif date.year < 1801 or date.year > 2099:
        raise ValueError('Datetime must be between year 1801 and 2099')

    # Perform the calculation
    julian_datetime = 367 * date.year - int((7 * (date.year + int((date.month + 9) / 12.0))) / 4.0) + int(
        (275 * date.month) / 9.0) + date.day + 1721013.5 + (
                          date.hour + date.minute / 60.0 + date.second / math.pow(60,
                                                                                  2)) / 24.0 - 0.5 * math.copysign(
        1, 100 * date.year + date.month - 190002.5) + 0.5

    return julian_datetime
# JD: Julian date
# output: GMST, in deg
# ref: https://dc.zah.uni-heidelberg.de/apfs/times/q/form

def calc_GMST(JD):
  T0 = (JD - 2451545.0)
  T = T0 / 36525.0
  #return 24110.54841 + 8640184.812866 * T + 0.093104 * T**2 - 0.0000062 * T**3 # in sec, wrong!
  #return 100.46061837 + 36000.770053608 * T + 0.000387933 * T ** 2 - T**3/38710000 # in deg
  gmst = 280.46061837 + 360.98564736629 * T0 + 0.000387933 * T * T - (1/38710000.0) * T * T * T
  return gmst % 360

# theta: angle from zenith in degree
# phi: angle from east to north, in degree
# CLF Latitude : 39.29693degee
# CLF Longitude : 112.90875degee
# yymmdd, hhmmss should be strings
# Conversion: see
# https://en.wikipedia.org/wiki/Celestial_coordinate_system#Equatorial_%E2%86%94_horizontal
def HO2EQ(theta, phi, yymmdd, hhmmss):
  YYYY = 2000 + int(yymmdd[:2])
  MM = int(yymmdd[2:4])
  DD = int(yymmdd[4:])

  hh = int(hhmmss[:2])
  mm = int(hhmmss[2:4])
  ss = int(hhmmss[4:])

  #H = float(hhmmss[:2]) + float(hhmmss[2:4])/60 + float(hhmmss[-2:]/3600 + float(usec)/3.6e-6
  lat_clf_rad = np.deg2rad(39.29693)
  lon_clf_rad = np.deg2rad(-112.90875)
  
  a_rad = np.deg2rad(90-theta) # Altitude, from ground
  #A_rad = np.deg2rad((90 - phi) % 360) # Azimuth algne, from north to east
  A_rad = np.deg2rad((270-phi)%360)
  
  #print YYYY, MM, DD, hh, mm, ss
  #print yymmdd, hhmmss, theta, phi
  DT = datetime.datetime(YYYY,MM,DD,hh,mm,ss)
  JD = get_julian_datetime(DT)
  #print JD
  GMST_rad = np.deg2rad(calc_GMST(JD))
  GMST_ha  = calc_GMST(JD) / 15 # in hour angle
  LMST_rad = GMST_rad + lon_clf_rad
  #print GMST_rad, GMST_ha, LMST_rad

  rot_LMST = np.array([\
    [np.cos(LMST_rad),  np.sin(LMST_rad), 0],\
    [np.sin(LMST_rad), -np.cos(LMST_rad), 0],\
    [               0,                 0, 1] \
  ])
  
  rot_lat = np.array([\
    [ np.sin(lat_clf_rad), 0, np.cos(lat_clf_rad)],\
    [                   0, 1,                   0],\
    [-np.cos(lat_clf_rad), 0, np.sin(lat_clf_rad)] \
  ])
  vec_aA = np.array([\
    np.cos(a_rad) * np.cos(A_rad),\
    np.cos(a_rad) * np.sin(A_rad),\
    np.sin(a_rad)
  ])

  vec_radec = np.dot(np.dot(rot_LMST,rot_lat),vec_aA)

  dec = np.arcsin(vec_radec[2])
  ra = np.arctan2(vec_radec[1], vec_radec[0])
  #print np.dot(vec_radec,vec_radec)
  #print np.rad2deg(ra)%360, np.rad2deg(dec)
  return np.rad2deg(ra) % 360, np.rad2deg(dec)
'''
print HO2EQ(42.21, 80.66, 190514, 84059)
print HO2EQ(33.75, 76.47, 190516, 123156)
print HO2EQ(61.78, 97.94, 190704, 205323)
print HO2EQ(59.41, 209.63, 190721, 211648)
'''

def EQ2HO(ra, dec, yymmdd, hhmmss):
  YYYY = 2000 + int(yymmdd[:2])
  MM = int(yymmdd[2:4])
  DD = int(yymmdd[4:])

  hh = int(hhmmss[:2])
  mm = int(hhmmss[2:4])
  ss = int(hhmmss[4:])

  ra_rad = np.deg2rad(ra)
  dec_rad = np.deg2rad(dec)

  #H = float(hhmmss[:2]) + float(hhmmss[2:4])/60 + float(hhmmss[-2:]/3600 + float(usec)/3.6e-6
  lat_clf_rad = np.deg2rad(39.29693)
  lon_clf_rad = np.deg2rad(-112.90875)


  #print YYYY, MM, DD, hh, mm, ss
  #print yymmdd, hhmmss, theta, phi
  DT = datetime.datetime(YYYY,MM,DD,hh,mm,ss)
  JD = get_julian_datetime(DT)
  #print JD
  GMST_rad = np.deg2rad(calc_GMST(JD))
  GMST_ha  = calc_GMST(JD) / 15 # in hour angle
  LMST_rad = GMST_rad + lon_clf_rad
  #print GMST_rad, GMST_ha, LMST_rad
  #print yymmdd, hhmmss, GMST_ha %24 // 1, GMST_ha % 1 * 100 / 60

  rot_LMST = np.array([\
    [np.cos(LMST_rad),  np.sin(LMST_rad), 0],\
    [np.sin(LMST_rad), -np.cos(LMST_rad), 0],\
    [               0,                 0, 1] \
  ])

  rot_lat = np.array([\
    [ np.sin(lat_clf_rad), 0,-np.cos(lat_clf_rad)],\
    [                   0, 1,                   0],\
    [ np.cos(lat_clf_rad), 0, np.sin(lat_clf_rad)] \
  ])
  vec_radec = np.array([\
    np.cos(dec_rad) * np.cos(ra_rad),\
    np.cos(dec_rad) * np.sin(ra_rad),\
    np.sin(dec_rad)
  ])

  vec_aA = np.dot(np.dot(rot_lat,rot_LMST),vec_radec)

  a_deg = np.rad2deg(np.arctan2(vec_aA[1], vec_aA[0]))
  A_deg = np.rad2deg(np.arcsin(vec_aA[2]))

  return a_deg, A_deg

