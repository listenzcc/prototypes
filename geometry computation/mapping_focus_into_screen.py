"""
File: mapping_focus_into_screen.py
Author: Chuncheng Zhang
Date: 2025-02-18
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Mapping the focus point into the screen space.
    When the screen's 3 corners are marked by the q-code sticky.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""

# %% ---- 2025-02-18 ------------------------
# Requirements and constants
import cv2
import numpy as np

from rich import print
from IPython.display import display
from PIL import Image, ImageDraw, ImageFont


# %% ---- 2025-02-18 ------------------------
# Function and class


def map_to_image_coords(point, img_size):
    '''Map ratio coordinates to image size

    :param point: The point to map.
    :param img_size: The size of the image.

    :return (x, y) (int, int): The mapped coordinates in image size.
    '''
    return (int(point[0] * img_size[0]), int(point[1] * img_size[1]))


def draw_node(point, img, color, mark: str = None):
    '''Draw the point into the img with color.

    :param point: The point to draw.
    :param img: The image to draw.
    :param color: The point color.
    :param mark: The mark to draw next to the point.
    '''
    drawer = ImageDraw.Draw(img)
    coords = map_to_image_coords(point, img.size)
    drawer.ellipse([coords[0] - 5, coords[1] - 5,
                   coords[0] + 5, coords[1] + 5], fill=color)
    if mark is not None:
        font = ImageFont.truetype("arial.ttf", 24)  # Increase font size
        drawer.text((coords[0] + 10, coords[1] - 10),
                    mark, fill=color, font=font)


def assign_points(p1, p2, p3):
    '''
    Assign the points.

    The right most point as NE.
    The other two points on the top, as the NW.
    The latest point as the SW.
    '''
    points = [p1, p2, p3]
    p_ne = sorted(points, key=lambda p: p[0], reverse=True)[0]
    points = [e for e in points if np.sum(np.abs(e-p_ne)) != 0]

    if points[0][1] > points[1][1]:
        p_sw = points[0]
        p_nw = points[1]
    else:
        p_sw = points[1]
        p_nw = points[0]

    corner_points = {
        'NE': p_ne,
        'NW': p_nw,
        'SW': p_sw,
    }
    return corner_points


def convert_coordinates(corner_points, point):
    '''
    Convert the point to the coordinate system defined by the corner points.
    The NE point's coordinates are (1, 0).
    The NW point's coordinates are (0, 0).
    The SW point's coordinates are (0, 1).
    '''
    nw = corner_points['NW']
    ne = corner_points['NE']
    sw = corner_points['SW']
    u = point - nw
    g1 = ne - nw
    g2 = sw - nw
    f1 = np.array([g2[1], -g2[0]])
    h1 = f1 / np.dot(g1, f1)
    f2 = np.array([g1[1], -g1[0]])
    h2 = f2 / np.dot(g2, f2)
    x, y = np.dot(u, h1), np.dot(u, h2)
    return x, y


# %% ---- 2025-02-18 ------------------------
# Play ground
img = Image.new('RGB', (400, 300), color='black')
drawer = ImageDraw.Draw(img)

# Generate random points.
p1 = np.random.random((2,))*0.1 + np.array((0.1, 0.8))
p2 = np.random.random((2,))*0.1 + np.array((0.8, 0.1))
p3 = np.random.random((2,))*0.1 + np.array((0.1, 0.1))
po = np.random.random((2,))*0.1 + 0.5

# Draw red nodes using draw_node function
draw_node(p1, img, 'blue')
draw_node(p2, img, 'blue')
draw_node(p3, img, 'blue')
draw_node(po, img, 'white')

display(img)


# %% ---- 2025-02-18 ------------------------
# Pending
corner_points = assign_points(p1, p2, p3)

# Draw corner points with marks
for k, v in corner_points.items():
    draw_node(v, img, 'green', k)

display(img)
print(corner_points)

# %%
x, y = convert_coordinates(corner_points, po)
print(x, y)

# %%
for i, p in enumerate([p1, p2, p3]):
    x, y = convert_coordinates(corner_points, p)
    print(i+1, x, y)
# %% ---- 2025-02-18 ------------------------
# Pending


class MousePosition:
    x = 0
    y = 0
    ratio_x = 0
    ratio_y = 0
    coord_x = 0
    coord_y = 0

    def set_xy(self, x, y):
        self.x = x
        self.y = y
        self.ratio_x = x / img.size[0]
        self.ratio_y = y / img.size[1]
        _x, _y = convert_coordinates(
            corner_points, (self.ratio_x, self.ratio_y))
        self.coord_x = _x
        self.coord_y = _y
        print(f"Mouse Position: X={x}, Y={y}, Coord=({_x:0.2f}, {_y:0.2f})")


mp = MousePosition()


def mouse_callback(event, x, y, flags, param):
    mp.set_xy(x, y)


winname = 'Image Window'
cv2.namedWindow(winname)
cv2.setMouseCallback(winname, mouse_callback)
while True:
    mat = np.array(img)
    mat[mp.y:mp.y+10, mp.x:mp.x+10] = [255, 0, 0]
    cv2.imshow(winname, mat)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()


# %%
# %%
# %%

# %%
