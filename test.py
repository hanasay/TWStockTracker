import matplotlib.pyplot as plt
import numpy as np

from matplotlib.widgets import MultiCursor

fig = plt.figure()

t = np.arange(0.0, 2.0, 0.01)
s1 = np.sin(2*np.pi*t)
s2 = np.sin(3*np.pi*t)

fig, (ax1, ax2) = plt.subplots(2, sharex=True)
ax1.plot(t, s1)
ax2.plot(t, s2)

cursor = MultiCursor(fig.canvas, (ax[0], ax[1]), color='r',lw=0.5, horizOn=True, vertOn=True)
plt.show()