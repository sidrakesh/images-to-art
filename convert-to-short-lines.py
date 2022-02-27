import cv2
from triangulared import generate_max_entropy_points
import matplotlib.pyplot as plt
import argparse
from matplotlib.patches import ConnectionPatch
import random
from PIL import Image
import math

# colors = ["#4285F4", "#DB4437", "#F4B400", '#0F9D58']
colors = ["#3481ff", "#f5ab06", "#fcee00", "#f03206", "#56da81"]
angles = [0, 45, 90, 135, 180, 225, 270, 315]

# util for distance between two points
def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))

def find_nearest_point(point, points_set):
    if len(points_set) == 0:
        return point

    min_dist = math.inf
    min_point = point

    for nb in points_set:
        d = dist(point, nb)
        if d < min_dist:
            min_dist = d
            min_point = nb

    return min_point

def get_random_color():
    return colors[random.randint(0, len(colors) - 1)]

color_map = {}

def dfs(point, adj_list, color):
    color_map[point] = color

    for nb in adj_list[point]:
        if nb not in color_map:
            dfs(nb, adj_list, color)

def adaptive_threshold(image, sigma):
    # convert the image to grayscale and blur it slightly
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(image, (sigma, sigma), 0)

    # apply simple thresholding with a hardcoded threshold value
    (T, threshInv) = cv2.threshold(blurred, 230, 255,
    cv2.THRESH_BINARY_INV)

    # apply Otsu's automatic thresholding
    (T, threshInv) = cv2.threshold(blurred, 0, 255,
    cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # instead of manually specifying the threshold value, we can use
    # adaptive thresholding to examine neighborhoods of pixels and
    # adaptively threshold each neighborhood
    thresh = cv2.adaptiveThreshold(blurred, 255,
    cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 10)

    # perform adaptive thresholding again, this time using a Gaussian
    # weighting versus a simple mean to compute our local threshold
    # value
    thresh = cv2.adaptiveThreshold(blurred, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 4)

    imagem = cv2.bitwise_not(thresh)

    return imagem

def process(input_path, output_path, n_points, background):
    # image = plt.imread(input_path)
    image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    # image = image.astype("uint8")

    im = Image.open(input_path)
    width, height = im.size
    dim = max(width, height)

    fig, ax = plt.subplots()
    ax.invert_yaxis()

    # image = adaptive_threshold(image, 5)
    # points = generate_max_entropy_points(image, n_points=n_points)

    image = adaptive_threshold(image, 1)

    points = generate_max_entropy_points(image, n_points=n_points)
    # points = np.concatenate([points, edge_points(image)])

    points_set = set()
    for point in points:
        p = (point[0], point[1])
        points_set.add(p)

    pairs = []

    while len(points_set) > 0:
        point = points_set.pop()
        nearest_point = find_nearest_point(point, points_set)
        # points_set.remove(nearest_point)

        pairs.append((point, nearest_point))

    sum_lens = 0

    for pair in pairs:
        sum_lens += dist(pair[0], pair[1])
    
    avg_len = sum_lens / len(pairs)

    lines = []

    for pair in pairs:
        if dist(pair[0], pair[1]) <= avg_len:
            lines.append(pair)

    # dfs
    adj_list = {}

    for pair in lines:
        if pair[0] not in adj_list:
            adj_list[pair[0]] = []
        if pair[1] not in adj_list:
            adj_list[pair[1]] = []
        adj_list[pair[0]].append(pair[1])
        adj_list[pair[1]].append(pair[0])

    for point in adj_list:
        if point not in color_map:
            dfs(point, adj_list, get_random_color())

    for pair in lines:
        color = color_map[pair[0]]
            
        line = ConnectionPatch(pair[0], pair[1], coordsA="data", linewidth=1, edgecolor=color)
        ax.add_patch(line)

    # remove boundary
    ax.axis("tight")
    ax.set_axis_off()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    ratio = image.shape[0] / image.shape[1]
    fig.set_size_inches(5, 5*ratio)

    fig.savefig(output_path, bbox_inches='tight', pad_inches=0, facecolor='black')

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
