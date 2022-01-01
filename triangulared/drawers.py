"""
Utilities to draw different steps to a matplotlib ax
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, ConnectionPatch, Arc
import math

def set_axis_defaults(ax):
    """
    Set's some defaults for a matplotlib ax

    :param ax: ax to change
    :return: None
    """
    ax.axis("off")
    ax.axis("tight")
    ax.set_aspect("equal")
    ax.autoscale(False)


def draw_image(ax, image):
    """
    Plots image to an ax
    :param ax: matplotlib axis
    :param image: image in array form
    :return: None
    """
    ax.imshow(image)


def draw_points(ax, points):
    """
    Plots a set of points on an ax
    :param ax: ax
    :param points: array of (x,y) coordinates
    :return: None
    """
    ax.scatter(x=points[:, 0], y=points[:, 1], color="k")

def get_poly_new_coords(p1, p2, n):
    new_coords = []

    for i in range(n):
        new_coords.append([p1[0] + (p2[0] - p1[0]) * (i + 1) / (n + 1), p1[1] + (p2[1] - p1[1]) * (i + 1) / (n + 1)])
    
    return new_coords

def add_poly_lines(ax, p1, p2, p3, n, color):
    new_coords = get_poly_new_coords(p2, p3, n)
    for new_coord in new_coords:
        nl = ConnectionPatch(p1, new_coord, coordsA="data", color=color)
        ax.add_patch(nl)

def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))

def get_extra_space_triangles(points, angles, c, d, r):
    extra_triangles = []

    for i in range(3):
        px = points[i][0]
        py = points[i][1]
        ang = angles[i]

        la = ((90 - ang / 2) / 2)
        l = math.tan(la * math.pi / 180) * r

        lr = 180 - 4 * la

        otherp = []

        for j in range(3):
            if j != i:
                otherp.append(points[j])

        k1 = math.sin(lr * math.pi / 180) * dist([c, d], otherp[0])
        lk1 = l + k1

        k2 = math.sin(lr * math.pi / 180) * dist([c, d], otherp[1])
        lk2 = l + k2

        l1 = dist(points[i], otherp[0])
        nx1 = (lk1 * otherp[0][0] + (l1 - lk1) * px) / l1
        ny1 = (lk1 * otherp[0][1] + (l1 - lk1) * py) / l1

        l2 = dist(points[i], otherp[1])
        nx2 = (lk2 * otherp[1][0] + (l2 - lk2) * px) / l2
        ny2 = (lk2 * otherp[1][1] + (l2 - lk2) * py) / l2

        extra_triangles.append([points[i], [nx1, ny1], [nx2, ny2]])

    return extra_triangles

def get_extra_space_triangles2(points, angles, c, d, r):
    extra_triangles = []

    for i in range(3):
        px = points[i][0]
        py = points[i][1]
        
        otherp = []

        for j in range(3):
            if j != i:
                otherp.append(points[j])

        d = dist(points[i], [c, d])
        k = d - r
        t = 2 * r

        l1 = dist(points[i], otherp[0])
        nx1 = (t * otherp[0][0] + k * px) / (k + t)
        ny1 = (t * otherp[0][1] + k * py) / (k + t)

        l2 = dist(points[i], otherp[1])
        nx2 = (t * otherp[1][0] + k * px) / (k + t)
        ny2 = (t * otherp[1][1] + k * py) / (k + t)

        extra_triangles.append([points[i], [nx1, ny1], [nx2, ny2]])

    return extra_triangles

def draw_spiral(ax, cx, cy, r, n, color):
    ncx = cx

    for i in range(2 * n - 1):
        if i % 2 == 0:
            fpx = ncx + ((i + 1) / n) * r
            acx = (ncx + fpx) / 2
            aw = (fpx - ncx)

            arc = Arc((acx, cy), aw, aw, theta1=0, theta2=180, color=color)
            ax.add_patch(arc)

            ncx = fpx
        else:
            fpx = ncx - ((i + 1) / n) * r
            acx = (ncx + fpx) / 2
            aw = ncx - fpx

            arc = Arc((acx, cy), aw, aw, theta1=180, theta2=0, color=color)
            ax.add_patch(arc)

            ncx = fpx
    
    arc = Arc((cx, cy), 2 * r, 2 * r, color=color)
    ax.add_patch(arc)

def draw_tear_drop(ax, points, fi, n, color):
    a = points[fi][0]
    b = points[fi][1]

    # draw_spiral(ax, c, d, r, 4, color)

    # x = (-sqrt(r^2 (a - c)^2 (a^2 - 2 a c + b^2 - 2 b d + c^2 + d^2)) + a^2 c - 2 a c^2 + b^2 c - 2 b c d + c^3 + c d^2)/(a^2 - 2 a c + b^2 - 2 b d + c^2 + d^2), a - c!=0

    # x1 = (-1 * math.sqrt(r * r * (a - c) * (a - c) * (a * a - 2 * a * c + b * b - 2 * b * d + c * c + d * d)) + a * a * c - 2 * a * c * c + b * b * c - 2 * b * c * d + c * c * c + c * d * d) / (a * a - 2 * a * c + b * b - 2 * b * d + c * c + d * d)
    # x2 = (math.sqrt(r * r * (a - c) * (a - c) * (a * a - 2 * a * c + b * b - 2 * b * d + c * c + d * d)) + a * a * c - 2 * a * c * c + b * b * c - 2 * b * c * d + c * c * c + c * d * d) / (a * a - 2 * a * c + b * b - 2 * b * d + c * c + d * d)

    # y = (a^3 d - b sqrt(r^2 (a - c)^2 (a^2 - 2 a c + b^2 - 2 b d + c^2 + d^2)) + d sqrt(r^2 (a - c)^2 (a^2 - 2 a c + b^2 - 2 b d + c^2 + d^2)) - 3 a^2 c d + a b^2 d - 2 a b d^2 + 3 a c^2 d + a d^3 - b^2 c d + 2 b c d^2 - c^3 d - c d^3)/((a - c) (a^2 - 2 a c + b^2 - 2 b d + c^2 + d^2))
    # y1 = (a * a * a * d - b * math.sqrt(r * r * (a - c) * (a - c) * (a * a - 2 * a * c + b * b - 2 * b * d + c * c + d * d)) + d * math.sqrt(r * r * (a - c) * (a - c) * (a * a - 2 * a * c + b * b - 2 * b * d + c * c + d * d)) - 3 * a * a * c * d + a * b * b * d - 2 * a * b * d * d + 3 * a * c * c * d + a * d * d * d - b * b * c * d + 2 * b * c * d * d - c * c * c * d - c * d * d * d) / ((a - c) * (a * a - 2 * a * c + b * b - 2 * b * d + c * c + d * d))
    # y2 = (a * a * a * d + b * math.sqrt(r * r * (a - c) * (a - c) * (a * a - 2 * a * c + b * b - 2 * b * d + c * c + d * d)) - d * math.sqrt(r * r * (a - c) * (a - c) * (a * a - 2 * a * c + b * b - 2 * b * d + c * c + d * d)) - 3 * a * a * c * d + a * b * b * d - 2 * a * b * d * d + 3 * a * c * c * d + a * d * d * d - b * b * c * d + 2 * b * c * d * d - c * c * c * d - c * d * d * d) / ((a - c) * (a * a - 2 * a * c + b * b - 2 * b * d + c * c + d * d))

    # dx = 0
    # dy = 0

    # if dist([a, b], [x1, y1]) < dist([a, b], [x2, y2]):
    #     dx = x1
    #     dy = y1
    # else:
    #     dx = x2
    #     dy = y2

    # fdist = dist([a, b], [c, d])

    # dx = c + (r / fdist) * (a - c)
    # dy = d + (r / fdist) * (b - d)

    otherp = []

    for i in range(3):
        if i != fi:
            otherp.append(points[i])

    dx = (otherp[0][0] + otherp[1][0]) / 2
    dy = (otherp[0][1] + otherp[1][1]) / 2

    for i in range(n):
        nx = dx + ((i + 1) / n) * (a - dx)
        ny = dy + ((i + 1) / n) * (b - dy)

        nl1 = ConnectionPatch(otherp[0], [nx, ny], coordsA="data", color=color)
        ax.add_patch(nl1)

        nl2 = ConnectionPatch(otherp[1], [nx, ny], coordsA="data", color=color)
        ax.add_patch(nl2)

def draw_circle_remaining_space(ax, extra_triangle, color):
    draw_tear_drop(ax, extra_triangle, 0, 3, color)

def draw_triangles(ax, points, vertices, colours=None, **kwargs):
    """
    Draws a set of triangles on axis
    :param ax: ax
    :param points: array of (x,y) coordinates
    :param vertices: an array of the vertices of the triangles, indexing the array points
    :param colours: colour of the faces, set as none just to plot the outline
    :param kwargs: kwargs passed to Polygon
    :return: None
    """

    if colours is None:
        face_colours = len(vertices) * ["none"]
        line_colours = len(vertices) * ["black"]
    else:
        face_colours = colours
        line_colours = colours
    
    max_px = max(map(lambda p: p[0], points))
    max_py = max(map(lambda p: p[1], points))
    max_side = max(max_px, max_py)

    for triangle, fc, ec in zip(vertices, face_colours, line_colours):
        back_color = [fc[0], fc[1], fc[2], 0.33]
        triangle_points = [points[i] for i in triangle]

        p1 = triangle_points[0]
        p2 = triangle_points[1]
        p3 = triangle_points[2]

        l1 = math.sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))
        l2 = math.sqrt((p2[0] - p3[0]) * (p2[0] - p3[0]) + (p2[1] - p3[1]) * (p2[1] - p3[1]))
        l3 = math.sqrt((p3[0] - p1[0]) * (p3[0] - p1[0]) + (p3[1] - p1[1]) * (p3[1] - p1[1]))

        ang1 = math.acos(0.5 * (l1 * l1 + l3 * l3 - l2 * l2) / (l1 * l3))
        ang2 = math.acos(0.5 * (l1 * l1 + l2 * l2 - l3 * l3) / (l1 * l2))
        ang3 = math.acos(0.5 * (l2 * l2 + l3 * l3 - l1 * l1) / (l2 * l3))

        min_ang = min(ang1, ang2, ang3) * 180 / math.pi
        can_draw_circle = min_ang > 45

        peri = l1 + l2 + l3

        ix = (l1 * p3[0] + l2 * p1[0] + l3 * p2[0]) / peri
        iy = (l1 * p3[1] + l2 * p1[1] + l3 * p2[1]) / peri

        area = 0.5 * (p1[0] * p2[1] + p2[0] * p3[1] + p3[0] * p1[1] - p2[0] * p1[1] - p3[0] * p2[1] - p1[0] * p3[1])
        semi = 0.5 * peri

        inradius = area / semi
        
        if can_draw_circle:
            p = Polygon(triangle_points,
                    closed=True, facecolor=back_color,
                    edgecolor=back_color, **kwargs)
            ax.add_patch(p)
            draw_spiral(ax, ix, iy, inradius, max(math.floor(inradius / max_side * 160), 3), ec)

            extra_triangles = get_extra_space_triangles(triangle_points, [ang1, ang2, ang3], ix, iy, inradius)

            for i in range(3):
                draw_circle_remaining_space(ax, extra_triangles[i], ec)
        elif min_ang > 30:
            p = Polygon(triangle_points,
                    closed=True, facecolor=back_color,
                    edgecolor=back_color, **kwargs)
            ax.add_patch(p)

            d1 = dist(p1, [ix, iy])
            d2 = dist(p2, [ix, iy])
            d3 = dist(p3, [ix, iy])

            maxd = max(d1, d2, d3)
            n = max(math.floor(maxd / max_side * 80), 4)

            if d1 == maxd:
                draw_tear_drop(ax, triangle_points, 0, n, ec)
            elif d2 == maxd:
                draw_tear_drop(ax, triangle_points, 1, n, ec)
            else:
                draw_tear_drop(ax, triangle_points, 2, n, ec)
        else:
            p = Polygon(triangle_points,
                    closed=True, facecolor=back_color,
                    edgecolor=ec, **kwargs)
            ax.add_patch(p)

            if ang1 >= ang2 and ang1 >= ang3:
                n = max(3, math.floor(l2 / max_side * 30))
                add_poly_lines(ax, p1, p2, p3, n, ec)
            elif ang2 >= ang1 and ang2 >= ang3:
                n = max(3, math.floor(l3 / max_side * 30))
                add_poly_lines(ax, p2, p3, p1, n, ec)
            else:
                n = max(3, math.floor(l1 / max_side * 30))
                add_poly_lines(ax, p3, p1, p2, n, ec)
