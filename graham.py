from random import randint
from collections import namedtuple


import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def graham(points):
    # Find the lowest, leftmost point
    pivot = min(points, key=lambda point: (point[1], point[0]))

    # Sort the points by polar angle with the pivot
    points.sort(key=lambda point: (slope(pivot, point), -point[1], point[0]))

    # Initialize the hull with the first two points
    hull = []
    hull.append(points[0])
    hull.append(points[1])

    # Process the remaining points
    for point in points[2:]:
        # Turn counter-clockwise
        while not (len(hull) <= 1 or cross_product(hull[-2], hull[-1], point) > 0):
            hull.pop()
        hull.append(point)

    return hull


def slope(p0, p1):
    y_span = p1[1] - p0[1]
    x_span = p1[0] - p0[0]
    return math.atan2(y_span, x_span)


def cross_product(p0, p1, p2):
    return (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p1[1] - p0[1]) * (p2[0] - p0[0])




def kps(points):
    
    pivot = min(points, key=lambda point: (point[1], point[0]))

    points.sort(key=lambda point: (slope(pivot, point), -point[1], point[0]))

    hull = []
    hull.append(points[0])
    hull.append(points[1])

    for point in points[2:]:

        while not (len(hull) <= 1 or cross_product(hull[-2], hull[-1], point) > 0):
            hull.pop()
        hull.append(point)

    return hull