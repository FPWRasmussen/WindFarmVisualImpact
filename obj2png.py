import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import matplotlib as mpl
from PIL import Image, ImageChops

V, F = [], []
with open("objects/turbine2.obj") as f:
    for line in f.readlines():
        if line.startswith('#'):
            continue
        values = line.split()
        if not values:
            continue
        if values[0] == 'v':
            V.append([float(x) for x in values[1:4]])
        elif values[0] == 'f' :
            F.append([int(x.split("/", 1)[0]) for x in values[1:4]])
V, F = np.array(V), np.array(F)-1
V = (V-(V.max(0)+V.min(0))/2) / max(V.max(0)-V.min(0))

fig = plt.figure(figsize=(6,6))
ax = fig.add_axes([0,0,1,1], xlim=[-1,+1], ylim=[-1,+1], aspect=1, frameon=False)
ax = fig.add_subplot(111, projection="3d")
plt.axis('off')
ax.view_init(elev=0, azim=60)
plt.grid(visible=None)
ax.plot_trisurf(V[:, 0], V[:,1], F, V[:, 2], linewidth=0.1, antialiased=True, closed=True, cmap=mpl.colormaps["Greys"])
limits = np.array([getattr(ax, f"get_{axis}lim")() for axis in "xyz"])
ax.set_box_aspect(np.ptp(limits, axis=1))
plt.savefig("turbine.png", dpi=300, transparent=True)
plt.show()


pil_image = Image.open("turbine.png")
pil_image = pil_image.crop((5, 5, pil_image.size[0]-5, pil_image.size[1]-5))
np_array = np.array(pil_image)
blank_px = [255, 255, 255, 0]
mask = np_array != blank_px
coords = np.argwhere(mask)
x0, y0, z0 = coords.min(axis=0)
x1, y1, z1 = coords.max(axis=0) + 1
cropped_box = np_array[x0:x1, y0:y1, z0:z1]
pil_image = Image.fromarray(cropped_box, 'RGBA')
pil_image.save("images/turbine5.png")
