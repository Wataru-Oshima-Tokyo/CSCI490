import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

# 入力点の集合
points = np.random.rand(15, 2)

# Voronoi図を計算する
vor = Voronoi(points)

# Voronoi図をプロットする
voronoi_plot_2d(vor)

# プロットを表示する
plt.show()