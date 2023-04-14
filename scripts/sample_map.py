import matplotlib.pyplot as plt
import numpy as np

map = np.random.rand(100, 100)

plt.imshow(map, cmap='gray', vmin=0.2, vmax=0.8)
plt.colorbar()
plt.show()