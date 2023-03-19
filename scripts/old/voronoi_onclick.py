import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
from matplotlib import pyplot as plt
from PIL import Image
import random
# PNGファイルを読み込んで、その幅と高さを取得する
image = Image.open("sh.png")
width, height = image.size
# Voronoi図の領域をPNGファイルの幅と高さにする
voronoi_xmin, voronoi_ymin = 0, 0
voronoi_xmax, voronoi_ymax = width, height

# ランダムに4つの点を選ぶ
points = []
for _ in range(4):
    x = random.randint(0, width-1)
    y = random.randint(0, height-1)
    points.append([x, y])
points = np.array(points)
print(points)

# Voronoiダイアグラムを作成
vor = Voronoi(points)

# クリックした座標に新しいポイントを追加する
fig, ax = plt.subplots()


ax.imshow(image)
# 軸をPNGファイルの幅と高さに調整する
ax.set_xlim([voronoi_xmin, voronoi_xmax])
ax.set_ylim([voronoi_ymin, voronoi_ymax])
new_points = []

def onclick(event):
    
    global points, new_points
    x, y = event.xdata, event.ydata
    print("x,y", x,y)
    if x is not None and y is not None:
        new_points.append([x, y])
        points = np.vstack([points, [x, y]])
        ax.scatter(x, y, color='red')
        vor = Voronoi(points)
        voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='orange')
        for r in vor.regions:
            polygon = [vor.vertices[i] for i in r if i >= 0]
            if len(polygon) > 0:
                ax.fill(*zip(*polygon), alpha=0.2)

# # # Voronoi図をプロットする

# voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='orange')
cid = fig.canvas.mpl_connect('button_press_event', onclick)

# プロットを表示
plt.show()