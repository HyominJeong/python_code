import numpy as np
import matplotlib.pyplot as plt
import sys

def gaussian(x, mean=0, sigma=1):
  return 1./ (sigma * np.sqrt(2 * np.pi)) * np.exp(-0.5 * np.power((x - mean) / sigma,2))

def pVal(z):
  result = 0.
  x = z
  x_end = 10
  x_step = 0.01
  while x < x_end:
    result += gaussian(x)
    x += x_step
  return -np.log(result)

# Define Neutrino Detector Class
class NeuDet:

  def __init__(self):
    self.nOfEvt = 0
    self.x_lim = 0
    self.y_lim = 0
    self.x_err = 0
    self.y_err = 0
    self.evts_x = np.array([])
    self.evts_dx = np.array([])
    self.evts_y = np.array([])
    self.evts_dy = np.array([])

    self.x_pixels = []
    self.y_pixels = []  
    print "Neutrin o Detector class is generaged"
  
  def setEnv(self, x_lim_, y_lim_, x_err_, y_err_):
    self.x_lim = x_lim_
    self.y_lim = y_lim_
    self.x_err = x_err_
    self.y_err = y_err_
    self.x_pixels = np.arange(- self.x_lim, self.x_lim, x_err)
    self.y_pixels = np.arange(- self.y_lim, self.y_lim, y_err)
    print "X, Y lim is", "+/-", self.x_lim, "+/-", self.y_lim
    print "X, Y pixels are"
    print self.x_pixels
    print self.y_pixels
  
  def detect(self, x, y, verbose=0):
    if (self.x_lim * self.y_lim * self.x_err * self.y_err == 0):
      print "Set X, Y limits and erros first."
    else:
      # Directly detect (No resolution is considered)
      #self.x_det = x
      #self.y_det = y
      
      # Detect with resolution
      self.x_det = x + np.random.normal() * self.x_err
      self.y_det = y + np.random.normal() * self.y_err
      
      # Neglect events out of FOV
      if ((abs(self.x_det) < self.x_lim) and (abs(self.y_det) < self.y_lim)):
        self.evts_x = np.append(self.evts_x, self.x_det)
        self.evts_dx = np.append(self.evts_dx, self.x_err)
        self.evts_y = np.append(self.evts_y, self.y_det)
        self.evts_dy = np.append(self.evts_dy, self.y_err)
        
        self.nOfEvt += 1

        if (verbose==1):
          print "Detected X and Y is", self.x_det, "+/-", self.x_err, ",", self.y_det, "+/-", self.y_err
          print "Input Event is", x, y
  
  def prtEvt(self):
    print self.nOfEvt, "Events are detected"

  def plotHist(self):
    #print self.evts_x, "\n", self.evts_y
    plt.hist2d(self.evts_x, self.evts_y, bins=60)
    plt.colorbar()
    plt.show()

  def plotScatter(self):
    plt.scatter(self.evts_x, self.evts_y, marker=".", alpha = 0.1)
    plt.savefig("ScatterPlot.pdf")
    np.save("scatterPlot.npy", np.array([self.evts_x, self.evts_y]))
    plt.close()


  def pValueMap(self, bin = 1):
    # Bined likelihood method
    if (bin == 1):
      # Set each bins
      nOfBin_x = 60
      nOfBin_y = 60
      self.x_pixels = np.linspace( -self.x_lim, self.x_lim, nOfBin_x)
      self.y_pixels = np.linspace( -self.y_lim, self.y_lim, nOfBin_y)
      self.pValuePos = np.zeros((nOfBin_x, nOfBin_y, 2),dtype = np.float)
      # [x,y] position of each pixel
      self.nOfHits = np.zeros((nOfBin_x, nOfBin_y),	dtype = np.float)
      # value of pValue of each pixel
      self.pValue = np.zeros((nOfBin_x, nOfBin_y),     dtype = np.float)      
      # Fill pValuePos
      for x_ind in range(nOfBin_x):
        for y_ind in range(nOfBin_y):
          self.pValuePos[x_ind,y_ind] = [self.x_pixels[x_ind], self.y_pixels[y_ind]]
      np.save("Binned_Pos.npy", self.pValuePos)
      
      # Fill pValue map
      for i in range(self.nOfEvt):
        x_ind_ = np.where(self.x_pixels < self.evts_x[i])[0][-1]
        y_ind_ = np.where(self.y_pixels < self.evts_y[i])[0][-1]
        #print self.evts_x[i], self.evts_y[i], x_ind_, y_ind_, self.x_pixels[x_ind_], self.y_pixels[y_ind_]
        self.nOfHits[x_ind_,y_ind_] += 1
      np.save("Binned_nOfHits.npy", self.nOfHits)

      # Convert number of hits to p-value
      self.ZMap = (self.nOfHits - np.mean(self.nOfHits)) / np.std(self.nOfHits)
      np.save("Binned_ZMap.npy", self.ZMap)

      # Calculate p-Value
      for i in range(nOfBin_x):
        for j in range(nOfBin_y):
          self.pValue[i,j] = pVal(self.ZMap[i,j])

      # Show result
      #plt.imshow(self.ZMap, interpolation='nearest')
      plt.imshow(self.pValue, interpolation='nearest')

      plt.colorbar()
      plt.savefig("Binned_pValue.pdf")
      plt.close()
      np.save("Binned_pValue.npy", self.pValue)

    # Unbinned likelihood method
    else:
      nOfBin_x = 600
      nOfBin_y = 600
      self.x_pixels = np.linspace( -self.x_lim, self.x_lim, nOfBin_x)
      self.y_pixels = np.linspace( -self.y_lim, self.y_lim, nOfBin_y)
      self.pValuePos = np.zeros((nOfBin_x, nOfBin_y, 2),dtype = np.float)
      # [x,y] position of each pixel
      self.nOfHits = np.zeros((nOfBin_x, nOfBin_y),     dtype = np.float)
      # value of pValue of each pixel
      self.pValue = np.zeros((nOfBin_x, nOfBin_y),     dtype = np.float)

      # Fill pValues
      print("Filling p-Values")
      for x_ind in range(nOfBin_x):
        for y_ind in range(nOfBin_y):
          self.pValuePos[x_ind,y_ind] = [self.x_pixels[x_ind], self.y_pixels[y_ind]]

          for i in range(self.nOfEvt):
            self.nOfHits[x_ind,y_ind] += gaussian(np.sqrt(\
              np.power(self.pValuePos[x_ind,y_ind][0] - self.evts_x[i],2) + \
              np.power(self.pValuePos[x_ind,y_ind][1] - self.evts_y[i],2)),\
              mean = 0,
              sigma = np.sqrt(np.power(self.x_err,2) + np.power(self.y_err,2)))

        if ((x_ind % 10) == 0):
          print("Calculating flux is done %.2f" % (1.* x_ind / nOfBin_x * 100))
      np.save("Unbinned_Pos.npy", self.pValuePos)
      np.save("Unbinned_nOfHits.npy", self.nOfHits)
      
      self.ZMap = (self.nOfHits - np.mean(self.nOfHits)) / np.std(self.nOfHits)
      np.save("Unbinned_ZMap.npy", self.ZMap)
      
      # Calculate p-Value
      for i in range(nOfBin_x):
        for j in range(nOfBin_y):
          self.pValue[i,j] = pVal(self.ZMap[i,j])

        if ((i % 10) == 0):
          print("Calculating p-value is done %.2f" % (1.*i / nOfBin_x * 100))
      # Show result
      #plt.imshow(self.ZMap, interpolation='nearest')
      plt.imshow(self.pValue, interpolation='nearest')
      plt.colorbar()
      plt.savefig("Unbinned.pdf")
      plt.close()
      np.save("Unbinned_pValue.npy", self.pValue)


#############################
#       Main procedure      #
#############################

# Set constants
x_lim = 30
y_lim = x_lim
x_err = 1
y_err = x_err

nOfMC = int(sys.argv[1])
#nOfMC = 100

detector = NeuDet()
detector.setEnv(x_lim,y_lim,x_err,y_err)

# Generate MC set
for i in range(nOfMC):
  x = (np.random.rand() - 0.5) * 2 * x_lim
  y = (np.random.rand() - 0.5) * 2 * y_lim
  detector.detect(x, y)

# Set source position and number of neutrino detected
srcPos_X = 0
srcPos_Y = 0

nOfNeu = int(sys.argv[2])
# Generate real events
for i in range(nOfNeu):
  x = srcPos_X
  y = srcPos_Y
  detector.detect(x,y)


detector.plotScatter()

detector.pValueMap()

detector.pValueMap(bin = 0)
