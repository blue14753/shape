import math
from typing import List


class Point():
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def point(self):
        return (self._x, self._y)


class Line():
    def __init__(self, point1: Point, point2: Point):
        self._start = point1
        self._end = point2

    @property
    def start(self):
        return Point(self._start.x, self._start.y)

    @property
    def end(self):
        return Point(self._end.x, self._end.y)

    @property
    def center(self):
        return Point((self._start.x+self._end.x)/2, (self._start.y+self._end.y)/2)

    @property
    def length(self):
        return round(distance(self._start, self._end), 2)


class Box():
    def __init__(self, top_left: Point, bottom_right: Point):
        self._top_left = top_left
        self._bottom_right = bottom_right

    def is_contain(self, point: Point):
        if (self._top_left.x <= point.x and point.x <= self._bottom_right.x) and (self._top_left.y <= point.y and point.y <= self._bottom_right.y):
            return True

        return False

    @property
    def width(self):
        return abs(self._bottom_right.x-self._top_left.x)

    @property
    def height(self):
        return abs(self._bottom_right.y - self._top_left.y)

    @property
    def top_left(self):
        return Point(self._top_left.x, self._top_left.y)

    @property
    def top_right(self):
        return Point(self._bottom_right.x, self._top_left.y)

    @property
    def bottom_left(self):
        return Point(self._top_left.x, self._bottom_right.y)

    @property
    def bottom_right(self):
        return Point(self._bottom_right.x, self._bottom_right.y)

    @property
    def center(self):
        return Point((self._top_left.x+self._bottom_right.x)/2, (self._top_left.y+self._bottom_right.y)/2)

    @property
    def area(self):
        return abs(self._bottom_right.x-self._top_left.x)*abs(self._bottom_right.y-self._top_left.y)


class Polygon():
    def __init__(self, points: List[Point]):
        self._points = points

    @property
    def points(self):
        return self._points

    def is_contain(self, point: Point):
        if len(self._points) < 3:
            return False

        v = self._points[-1]
        counter = 0

        for i in range(0, len(self._points)):
            v0 = v
            v = self._points[i]

            if (v0.y <= point.y and v.y <= point.y) or (v0.y > point.y and v.y > point.y) or (v0.x < point.x and v.x < point.x):
                if point.y == v.y and (point.x == v.x or (point.y == v0.y and ((v0.x <= point.x and point.x <= v.x) or (v.x <= point.x and point.x <= v0.x)))):
                    return True
                continue

            dist = (point.y-v0.y)*(v.x-v0.x) - (point.x-v0.x)*(v.y-v0.y)
            if dist == 0:
                return True

            if v.y < v0.y:
                dist = -dist

            if dist > 0:
                counter += 1

        if counter % 2 == 0:
            return False
        else:
            return True

# Math


def dot(point1: Point, point2: Point):
    return point1.x*point2.x + point1.y*point2.y


def point_cross(point1: Point, point2: Point):
    return point1.x*point2.y - point1.y*point2.x


# Direction of vector(o, a) -> vertor(o, b)
def cross_angle(o: Point, a: Point, b: Point):
    return (a.x-o.x)*(b.x-o.x) - (a.x-o.x)*(b.x-o.x)


def project_intersect(a1: int, a2: int, b1: int, b2: int):
    if a1 > a2:
        a1, a2 = a2, a1

    if b1 > b2:
        b1, b2 = b2, b1

    return max(a1, b1) <= min(a2, b2)


def axis_overlay(a1, len1, a2, len2):
    return min(a1+len1, a2+len2) - min(a1, a2)


def distance(point1: Point, point2: Point):
    dx = point1.x-point2.x
    dy = point1.y-point2.y

    return math.sqrt(dx*dx + dy*dy)


# Util
def similar_box(box1: Box, box2: Box):
    r1 = max(box1.width, box1.height) / 2
    r2 = max(box2.width, box2.height) / 2

    dist = distance(box1.center, box2.center)

    if dist <= min(r1, r2):
        return dist
    else:
        return -1


def box_intersect(box1: Box, box2: Box):
    top_left_x = max(box1.top_left.x, box2.top_left.x)
    top_left_y = max(box1.top_left.y, box2.top_left.y)
    bottom_right_x = min(box1.bottom_right.x, box2.bottom_right.x)
    bottom_right_y = min(box1.bottom_right.y, box2.bottom_right.y)

    if top_left_x < bottom_right_x and top_left_y < bottom_right_y:
        return Box(Point(top_left_x, top_left_y), Point(bottom_right_x, bottom_right_y))


def box_union_area(box1: Box, box2: Box):
    return box1.area + box2.area - box_intersect(box1, box2).area


def box_iou(box1: Box, box2: Box):
    union = box_union_area(box1, box2)
    if union > 0:
        return box_intersect(box1, box2).area / union


def is_line_cross(line1: Line, line2: Line):
    return project_intersect(line1.start.x, line1.end.x, line2.start.x, line2.end.x) and project_intersect(line1.start.y, line1.end.y, line2.start.y, line2.end.y) and cross_angle(line1.start, line1.end, line2.start)*cross_angle(line1.start, line1.end, line2.end) <= 0 and cross_angle(line2.start, line2.end, line1.start)*cross_angle(line2.start, line2.end, line1.end) <= 0


if __name__ == "__main__":
    line = Line(Point(0, 0), Point(2, 5))
    # print(line.start.point, line.end.point, line.center.point, line.length)

    box1 = Box(Point(0, 0), Point(2, 5))
    # print(box.top_left.point, box.top_right.point,
    #       box.bottom_left.point, box.bottom_right.point, box.center.point, box.width, box.height, box.area)
    # print(box.is_contain(Point(1, 1)))
    box2 = Box(Point(0, 0), Point(1, 1))
    print(box_intersect(box1, box2).area, box_iou(box1, box2))

    polygon = Polygon([Point(0, 0), Point(2, 2), Point(-2, -2)])
    # print(polygon.is_contain(Point(1, 1)))
