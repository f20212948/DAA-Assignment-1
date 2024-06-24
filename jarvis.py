class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def orientation(p, q, r):
    '''
    To find orientation of ordered triplet (p, q, r). 
    The function returns following values 
    0 --> p, q and r are collinear 
    1 --> Clockwise 
    2 --> Counterclockwise 
    '''
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)

    if val < 0:
        return 2
    elif val > 0:
        return 1
    else:
        return 0


def Left_index(points):
    min = [0]
    for i in range(1, len(points)):
        if points[i].x < points[min[0]].x:
            min[0] = i
        elif points[i].x == points[min[0]].x:
            if points[i].y > points[min[0]].y:
                min[0] = i
    return min[0]


def convexHull(points):
    if len(points) < 3:
        return
    l = Left_index(points)

    hull = []
    p = l
    q = [0]
    while (True):
        hull.append(p)
        q[0] = (p + 1)
        q[0] %= len(points)
        for i in range(len(points)):
            if (orientation(points[p], points[i], points[q[0]]) == 2):
                q[0] = i
        p = q[0]
        if (p == l):
            break

    hull = list(set([(points[i].x, points[i].y) for i in hull]))
    return [list(i) for i in hull]


def Jarvis(a):
    a = [(i[0], i[1]) for i in a]
    points = [Point(x[0], x[1]) for x in a]
    answer = convexHull(points)
    return answer
