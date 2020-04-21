import numpy as np


# Rotate vector about x-axis
# Positive angle rotations move z toward +y

def xrot (a, angle) :

  m = np.array([\
    [ 1., 	     0., 	    0.],\
    [ 0., np.cos(angle), np.sin(angle)],\
    [ 0.,-np.sin(angle), np.cos(angle)]])

  b = np.dot(m, a)
  return b

# Rotate vector about y-axis
# Positive angle rotations move z toward -x

def yrot (a, angle) :

  m = np.array([\
    [ np.cos(angle), 	0., -np.sin(angle)],\
    [ 		 0., 	1.,	        0.],\
    [ np.sin(angle),	0.,  np.cos(angle)]])

  b = np.dot(m, a)
  return b

# Rotate vector about z-axis
# Positive angle rotations move x toward -y

def zrot (a, angle) :

  b = np.zeros(3)

  m = np.array([\
    [ np.cos(angle), np.sin(angle), 0.],\
    [-np.sin(angle), np.cos(angle), 0.],\
    [ 		 0.,		0., 1.]])

  b = np.dot(m, a)
  return b



# Convert geodectic Latitude, Longitude, Altitude to ECEF X, Y, Z
# Altitude is geodectic altitude
# Latitude and Longitude in degrees

def latlonalt_to_xyz (Latitude, Longitude,Altitude):
  Latitude *= tacoortrans_D2R
  Longitude *= tacoortrans_D2R
  r0 = tacoortrans_R_EQ/np.sqrt(\
    np.cos(Latitude)*np.cos(Latitude) + \
    (1-tacoortrans_FLAT)*(1-tacoortrans_FLAT)*np.sin(Latitude)*np.sin(Latitude))
  as_ = (1-tacoortrans_FLAT)*(1-tacoortrans_FLAT)*r0
  X = ( r0 + Altitude ) * np.cos(Latitude)*np.cos(Longitude)
  Y = ( r0 + Altitude ) * np.cos(Latitude)*np.sin(Longitude)
  Z = ( as_ + Altitude ) * np.sin(Latitude)
  return np.array([X,Y,Z])

# Convert GPS coordinates to xyz with respect to CLF coordinate system
# X - EAST, Y-NORTH
# lat,lon in degrees, alt in meters.
# Output: xyz components in meters.

def latlonalt_to_xyz_clf_frame(Latitude, Longitude, Altitude):
  
  XYZ = latlonalt_to_xyz (tacoortrans_CLF_Latitude,tacoortrans_CLF_Longitude,tacoortrans_CLF_Altitude)
  xyz = latlonalt_to_xyz (Latitude, Longitude, Altitude)
  xyz -= XYZ
  xyz = zrot (xyz, tacoortrans_CLF_Longitude*tacoortrans_D2R)
  xyz = yrot (xyz, (90.0-tacoortrans_CLF_Latitude)*tacoortrans_D2R)
  xyz = zrot (xyz, 90.0*tacoortrans_D2R)
  return xyz

# Convert GPS infomation to sdxyzclf
# input: XXYY, Latitude, Longitude, Altitude
# Latitude, Longitude in miliarcsec, altitude in cm
# output: YYXX, SDCLF_X, SDCLF_Y, SDCLF_Z
# SDCLF in [1200m]
def GPS2CLF(XXYY, Latitude, Longitude, Altitude):
  Latitude *= 1. /1.e3 / 3600
  Longitude *= 1. / 1.e3 / 3600
  Altitude *= 1. / 1.e2
  xyz = latlonalt_to_xyz_clf_frame(Latitude, Longitude, Altitude) / 1200
  YYXX = "%2d%2d" % (XXYY % 100, XXYY // 100)
  return YYXX, xyz

# Define constants
tacoortrans_D2R 	= 0.0174532925199432954743716805978692718782
tacoortrans_R_EQ	= 6378137.0  # Radius of the Earth at the equator
tacoortrans_INV_FLAT	= 298.257223 # Shape parameter
tacoortrans_FLAT	= (1./tacoortrans_INV_FLAT)
tacoortrans_CLF_Latitude= 39.29693
tacoortrans_CLF_Longitude=-112.90875
tacoortrans_CLF_Altitude= 1382.0

SD_ORIGIN_X_CLF = -12.2435
SD_ORIGIN_Y_CLF = -16.4406

