import SD1MIPFunc
import numpy as np
import matplotlib.pyplot as plt

x = np.arange(-5, 10, 0.1)

y = SD1MIPFunc.Landau(x)

plt.plot(x,y)
plt.show()
