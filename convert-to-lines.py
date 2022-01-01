from triangulared import generate_max_entropy_points, edge_points, adaptive_threshold
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
import argparse
from PIL import Image
import math
from functools import cmp_to_key
import cv2

# finds intersection point of lines passing through points p1 and p2 with boundary x = <x> or y = <y>
def intersection_point(p1, p2, x, y):
    if p2[0] != p1[0]:
        m = (p2[1] - p1[1]) / (p2[0] - p1[0])
        c = p1[1] - (p2[1] - p1[1]) / (p2[0] - p1[0]) * p1[0]

        if y == -1:
            return [x, m * x + c]
        else:
            return [(y - c) / m, y]
    else:
        return [p1[0], y]

# checks if intersection point with boundary lies inside the image
def is_intersecting(ip, x, y, w, h):
    if y == -1:
        return ip[1] >= 0 and ip[1] <= h
    else:
        return ip[0] >= 0 and ip[0] <= w

# string encoding of a point
def point_to_str(p):
    px = str(p[0])
    py = str(p[1])
    return px + ' ' + py

# util for distance between two points
def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))

visited = {}

# finds all neighbors for a point through which line will be drawn
def get_neighbor_points(p, points, dim):
    # max gap between neighbors
    u_space = dim * 0.1
    # min gap between neighbors. lines between extremely close points leads to useless lines being drawn
    l_space = dim * 0.02

    nbs = []

    for nb in points:
        d = dist(p, nb)
        if d <= u_space and d >= l_space:
            key1 = point_to_str(p)
            key2 = point_to_str(nb)
            keyFor = key1 + '->' + key2
            keyBack = key2 + '->' + key1
            if (keyFor not in visited) and (keyBack not in visited):
                visited[keyFor] = True
                visited[keyBack] = True
                nbs.append(nb)
    
    return nbs

ends_visited = {}

def draw_bw_points(ax, p, nbs, w, h):
    for nb in nbs:
        ips = []
        for lp in [[0, -1], [w, -1], [-1, 0], [-1, h]]:
            ip = intersection_point(p, nb, lp[0], lp[1])
            intersects = is_intersecting(ip, lp[0], lp[1], w, h)
            if intersects:
                ips.append(ip)

        if len(ips) != 2:
            continue

        key1 = point_to_str(ips[0])
        key2 = point_to_str(ips[1])
        keyFor = key1 + '->' + key2
        keyBack = key2 + '->' + key1

        if (keyFor not in ends_visited) and (keyBack not in ends_visited):
            ends_visited[keyFor] = True
            ends_visited[keyBack] = True
            line = ConnectionPatch(ips[0], ips[1], coordsA="data", linewidth=0.01)
            ax.add_patch(line)

def process(input_path, output_path, n_points):
    image = plt.imread(input_path)

    image = adaptive_threshold(image, 7)

    points = generate_max_entropy_points(image, n_points=n_points)
    points = np.concatenate([points, edge_points(image)])

    fig, ax = plt.subplots()
    ax.invert_yaxis()

    im = Image.open(input_path)
    width, height = im.size
    dim = max(width, height)

    for point in points:
        nbs = get_neighbor_points(point, points, dim)
        draw_bw_points(ax, point, nbs, width, height)

    # remove boundary
    ax.axis("tight")
    ax.set_axis_off()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)  

    ratio = image.shape[0] / image.shape[1]
    fig.set_size_inches(5, 5*ratio)

    fig.savefig(output_path, bbox_inches='tight', pad_inches=0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Turns and image into triangles")
    parser.add_argument("input_file")
    parser.add_argument("output_file")
    parser.add_argument("-n", "--n_points", nargs='?',
                        help="number of points to use", default=100)

    ns = parser.parse_args()

    input_file = ns.input_file
    output_file = ns.output_file
    n_points = int(ns.n_points)

    process(input_path=input_file, output_path=output_file, n_points=n_points)
