import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0,10,0.01)
y = np.sin(x)

plt.plot(x,y)
plt.xlabel("x")
plt.ylabel("y")
plt.title("y=sin(x)")
plt.show()