import random
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
from matplotlib import pyplot as plt
from PIL import Image




def onclick(event):
    if event.button == 1:
        # クリックした座標を取得
        x, y = event.xdata, event.ydata
        print("Clicked at:", x, y)

        # 新しいポイントを追加
        global points
        if len(points) == 0:
            points.append([x, y])
            points = np.array(points)
        else:
            points = np.vstack([points, [x, y]])
            print(points)
        if len(points)>2:
           

            # Voronoi図を再作成
            global vor, finite_polygons, image_name
            vor = Voronoi(points)
            finite_polygons = []
            for i, region in enumerate(vor.regions):
                if -1 not in region:
                    polygon = [vor.vertices[j] for j in region]
                    finite_polygons.append(polygon)

            # 図を再描画
            ax.clear()
            ax.imshow(image)
            voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='orange')
            for polygon in finite_polygons:
                plt.fill(*zip(*polygon), alpha=0.2)

            # ax.set_xlim(np.min(points[:, 0])-1, np.max(points[:, 0])+1)
            # ax.set_ylim(np.min(points[:, 1])-1, np.max(points[:, 1])+1)
            # 軸をPNGファイルの幅と高さに調整する
            ax.set_xlim([voronoi_xmin, voronoi_xmax])
            ax.set_ylim([voronoi_ymin, voronoi_ymax])
            plt.gca().invert_yaxis()
            plt.draw()
            image_name = 'voronoi.png'
            plt.savefig(image_name)

# PNGファイルを読み込んでピクセルデータを取得する
image_name = "sh.png"
image = Image.open(image_name)
pixels = image.load()
width, height = image.size

# Voronoi図の領域をPNGファイルの幅と高さにする
voronoi_xmin, voronoi_ymin = 0, 0
voronoi_xmax, voronoi_ymax = width, height

# ランダムに4つの点を選ぶ
points = []
# 図を作成する
fig, ax = plt.subplots()
ax.imshow(image)
cid = fig.canvas.mpl_connect('button_press_event', onclick)


# 図を表示する
plt.show()
plt.savefig(image_name)