from triangulared import generate_max_entropy_points_with_entropy, set_axis_defaults, adaptive_threshold
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import argparse
from matplotlib.patches import Circle, Polygon, Path, PathPatch
import random
from PIL import Image
import matplotlib as mpl

colors = ["#FFFFFF", "#f9caad", "#8fc7dd"]
angles = [0, 45, 90, 135, 180, 225, 270, 315]

def draw_star(ax, x, y, height, color):
    width = height
    c = (x, y)
    p1 = (x, y - height / 2)
    p1c = (x, y - height / 32)
    p2 = (x + width / 2, y)
    p2c = (x + width / 32, y)
    p3 = (x, y + height / 2)
    p3c = (x, y + height / 32)
    p4 = (x - width / 2, y)
    p4c = (x - width / 32, y)

    pathdata = [
        (Path.MOVETO, p1),
        (Path.CURVE4, p1c),
        (Path.CURVE4, p2c),
        (Path.CURVE4, p2),
        (Path.CURVE4, p2c),
        (Path.CURVE4, p3c),
        (Path.CURVE4, p3),
        (Path.CURVE4, p3c),
        (Path.CURVE4, p4c),
        (Path.CURVE4, p4),
        (Path.CURVE4, p4c),
        (Path.CURVE4, p1c),
        (Path.CURVE4, p1),
    ]

    codes, verts = zip(*pathdata)
    path = Path(verts, codes)
    patch = PathPatch(path, facecolor=color, edgecolor=color, linewidth=0.01, alpha=0.9)

    # rotate
    # t = mpl.transforms.Affine2D().rotate_deg_around(x, y, angles[random.randint(0, len(angles) - 1)]) + ax.transData
    # patch.set_transform(t)

    ax.add_patch(patch)

def process(input_path, output_path, n_points, background):
    image = plt.imread(input_path)
    original = image

    image = adaptive_threshold(image, 5)

    points, entropies = generate_max_entropy_points_with_entropy(image, n_points=n_points)

    fig, ax = plt.subplots()
    ax.invert_yaxis()
    
    for i in range(len(points)):
        color_rgba = original[points[i][1]][points[i][0]]
        color = '#{:02x}{:02x}{:02x}'.format(*color_rgba)
        draw_star(ax, points[i][0], points[i][1], entropies[i] * 4, color)
        # draw_star(ax, points[i][0], points[i][1], entropies[i] * 4, colors[random.randint(0, len(colors) - 1)])

    # remove boundary
    ax.axis("tight")
    ax.set_axis_off()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    ratio = image.shape[0] / image.shape[1]
    fig.set_size_inches(5, 5*ratio)

    fc = background

    if background == "light":
        fc = "#0a0b3a"
    elif background == "medium":
        fc = "#040020"
    elif background == "dark":
        fc = "#01040f"

    fig.savefig(output_path, bbox_inches='tight', pad_inches=0, facecolor=fc)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Turns an image into stars")
    parser.add_argument("input_file")
    parser.add_argument("output_file")
    parser.add_argument("-n", "--n_points", nargs='?',
                        help="number of points to use", default=100)
    parser.add_argument("-b", "--background", nargs='?',
                        help="background type (light, medium, dark)", default="dark")

    ns = parser.parse_args()

    input_file = ns.input_file
    output_file = ns.output_file
    n_points = int(ns.n_points)
    background = ns.background

    process(input_path=input_file, output_path=output_file, n_points=n_points, background=background)
