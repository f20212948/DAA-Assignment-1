from random import randint
from collections import namedtuple
from graham import *


import math


Point = namedtuple('Point', 'x y')

neg = -1


def flipped(points):
    return [Point(neg*point.x, neg*point.y) for point in points]


def swap(ls, i, j):
    ls[i], ls[j] = ls[j], ls[i]
    return ls


def quickselect(ls, index, lo=0, hi=None, depth=0):
    if hi is None:
        hi = len(ls)+neg
    if lo == hi:
        return ls[lo]
    pivot = randint(lo, hi)
    ls = list(ls)
    ls = swap(ls, lo, pivot)
    cur = lo
    for run in range(lo+1, hi+1):
        if ls[run] < ls[lo]:
            cur += 1
            ls = swap(ls, cur, run)
    ls = swap(ls, cur, lo)
    if index > cur:
        return quickselect(ls, index, cur+1, hi, depth+1)
    elif index < cur:
        return quickselect(ls, index, lo, cur-1, depth+1)
    else:
        return ls[cur]
    # a = sorted(list(ls))
    # return a[index]


def clockwiseorder(points):
    points = list(points)
    n = len(points)
    for i in range(n):
        for j in range(i+1, n):
            if points[j].x < points[i].x:
                points[i], points[j] = points[j], points[i]
            elif points[j].x == points[i].x:
                if points[j].y < points[i].y:
                    points[i], points[j] = points[j], points[i]
    return points

def bridge(points, vertical_line):
    candidates = []
    if len(points) == 2:
        return tuple(sorted(points))
    pairs = []
    modify_s = set(points)
    while len(modify_s) >= 2:
        x = [tuple(sorted([modify_s.pop(), modify_s.pop()]))]
        pairs += x
    if len(modify_s) == 1:
        candidates.append(modify_s.pop())
    slopes = []
    for pi, pj in pairs[:]:
        if pi.x == pj.x:
            pairs.remove((pi, pj))
            candidates.append(pi if pi.y > pj.y else pj)
        else:
            slopes += [(pi.y-pj.y)/(pi.x-pj.x)]

    if(slopes == []):
        return [min(points), max(points)]

    median_index = len(slopes)//2 + (neg if len(slopes) % 2 == 0 else 0)
    median_slope = quickselect(slopes, median_index)
    small = {pairs[i]
             for i, slope in enumerate(slopes) if slope < median_slope}
    equal = {pairs[i]
             for i, slope in enumerate(slopes) if slope == median_slope}
    large = {pairs[i]
             for i, slope in enumerate(slopes) if slope > median_slope}
    
    

    max_slope = max(point.y + neg*median_slope*point.x for point in points)
    max_set = [point for point in points if point.y +
               neg*median_slope*point.x == max_slope]
    left = min(max_set)
    right = max(max_set)
    candidates = set(candidates)
    if left.x <= vertical_line and right.x > vertical_line:
        return (left, right)
    if right.x <= vertical_line:
        candidates |= {point for _, point in equal}
        candidates |= {point for _, point in large}
        candidates |= {point for pair in small for point in pair}
    if left.x > vertical_line:
        candidates |= {point for point, _ in equal}
        candidates |= {point for point, _ in small}
        candidates |= {point for pair in large for point in pair}
    return bridge(candidates, vertical_line)


def connect(lower, upper, points):
    if lower == upper:
        return [upper]
    
    if(1 < len(points) <= 5):
        # graham scan
        a = list([point.x, point.y] for point in points)
        hull1 = graham(a)
        # hull1 in clockwise order

        hull2 = [Point(x, y) for [x, y] in hull1]
        hull3 = clockwiseorder(hull2)
        

        return list(hull3)

    max_left = quickselect(points, len(points)//2+neg)
    min_right = quickselect(points, len(points)//2)
    lr = bridge(points, (max_left.x + min_right.x)/2)
    left = lr[0]
    right = lr[1]
    # points_left = {point for point in points if point.x < left.x} | {left}
    # points_right = {point for point in points if point.x > right.x} | {right}

    if(lower.x == left.x):
        points_left = {left} | {point for point in points if point.x <= left.x}
    else:
        slope1 = (left.y-lower.y)/(left.x-lower.x)
        points_left = {left} | {point for point in points if (point.x <= left.x and point.y >= slope1*(point.x-lower.x)+lower.y)}
    
    if(upper.x == right.x):
        points_right = {right} | {point for point in points if point.x >= right.x}
    else:
        slope2 = (right.y-upper.y)/(right.x-upper.x)
        points_right = {right} | {point for point in points if (point.x >= right.x and point.y >= slope2*(point.x-upper.x)+upper.y)}

    # return connect(lower, left, points_left) + connect(right, upper, points_right)
    ret = []
    if(left == lower):
        l=[lower]
        ret += l
    else:
        ret += connect(lower, left, points_left)
    if(right == upper):
        r=[upper]
        ret += r
    else:
        ret += connect(right, upper, points_right)
    return ret


def upper_hull(points):
    lowerx = min([p.x for p in points])
    lower = max({point for point in points if point.x == lowerx})
    upperx = max([p.x for p in points])
    upper = max({point for point in points if point.x == upperx})
    points = {lower, upper} | {p for p in points if upperx > p.x > lowerx}
    return connect(lower, upper, points)


def convex_hull(points):
    upper = upper_hull(points)
    lower = flipped(upper_hull(flipped(points)))
    if upper[-1] == lower[0]:
        del lower[0]
    if upper[0] == lower[-1]:
        del upper[0]
    return upper + lower


def kirkpatricks(a):
    a = [(i[0], i[1]) for i in a]
    points = {Point(x[0], x[1]) for x in a}
    # points = flipped(points
    answer = convex_hull(points)
    return answer
