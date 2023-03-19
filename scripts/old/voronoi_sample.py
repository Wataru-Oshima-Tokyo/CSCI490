import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
from matplotlib import pyplot as plt
from PIL import Image

# PNGファイルを読み込んで、その幅と高さを取得する
image = Image.open("sh.png")
width, height = image.size

# 4つのポイントを計算する
x1, y1 = 0, 0
x2, y2 = width, 0
x3, y3 = width, height
x4, y4 = 0, height

# 四角形の頂点を配列にまとめる
points = np.array([[x1, y1], [x4, y4]])

# Voronoi図を作成する
vor = Voronoi(points)

# 有限領域のポリゴンを取得する
finite_polygons = []
for i, region in enumerate(vor.regions):
    if -1 not in region:
        polygon = [vor.vertices[j] for j in region]
        finite_polygons.append(polygon)

# Voronoi図をプロットする
fig, ax = plt.subplots()
voronoi_plot_2d(vor, ax=ax)

# 有限領域のポリゴンをプロットする
for polygon in finite_polygons:
    plt.fill(*zip(*polygon), alpha=0.2)

# 軸を調整する
min_x, max_x = np.min(points[:, 0])-1, np.max(points[:, 0])+1
min_y, max_y = np.min(points[:, 1])-1, np.max(points[:, 1])+1
ax.set_xlim(min_x, max_x)
ax.set_ylim(min_y, max_y)


# プロットを表示
plt.show()



