# -*- coding: utf-8 -*-
from __future__ import division  # imports division from Python 3.6


def slope(dx, dy):
    return dy / dx if dx else float("inf")


class ReturnValue(object):
    def __init__(self, points, depth):
        self.points = points
        self.depth = depth

    def __add__(self, other):
        new_points = self.points + other.points
        min_depth = min(self.depth, other.depth)
        return ReturnValue(new_points, min_depth)

    def __radd__(self, other):
        return self

    def my_sum(returnValues):
        result = ReturnValue(0, 100000000)
        for rv in returnValues:
            result = result + rv
        return result


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return self.__str__()

    def __cmp__(self, other):
        # compare them with x values first
        if self.x > other.x:
            return 1
        if self.x < other.x:
            return -1
        # if x values are the same check y values
        if self.y > other.y:
            return 1
        if self.y < other.y:
            return -1
        # y values are the same too.
        return 0

    def y_int(self, target):
        return self.y - self.slope(target) * self.x

    def slope_from_origin(self):
        return slope(self.x, self.y)

    def slope(self, target):
        return slope(target.x - self.x, target.y - self.y)

    def line_equation(self, target):
        slope_local = self.slope(target)
        y_int = self.y_int(target)

        if y_int < 0:
            y_int = -y_int
            sign = '-'
        else:
            sign = '+'
        return 'y = {}x {} {}'.format(slope_local, sign, y_int)


# Function returns all possible lines
def solution_brute(points):
    general_set = set()
    for p1 in points:
        for p2 in points:
            line = p1.slope(p2)
            s = {p1}  # set of collinear points ; {} for Python set literal
            for p in points:
                if line == p1.slope(p):
                    s.add(p)
            if len(s) > 1:
                general_set.add(frozenset(s))  # set of sets
    return general_set


# Function returns all possible lines
def solution_faster_brute(points):
    general_set = set()
    for p1 in points:
        slopes_buckets = {}
        for p2 in points:
            if p1 == p2:
                continue
            s = p1.slope(p2)
            if s not in slopes_buckets.keys():  # create different sets for different slopes
                slopes_buckets[s] = {p1}
            slopes_buckets[s].add(p2)
        for bucket in slopes_buckets.values():
            general_set.add(tuple(sorted(bucket)))
    return general_set


# function returns the amount of possible solutions
def final_result_brute(points):
    list_of_sets = []
    if len(points) < 2:
        return ReturnValue(1, len(points))
    list_of_lines = solution_brute(points)
    for line in list_of_lines:
        difference = points.difference(line)
        # keeps all possible ways to remove all collinear points
        list_of_sets.append(final_result_brute(difference))

    presum = sum(list_of_sets)
    presum.depth = presum.depth + 1
    return presum


def final_result_faster_brute(points):
    list_of_sets = []
    if len(points) < 2:
        return ReturnValue(1, len(points))
    list_of_lines = solution_faster_brute(points)
    for line in list_of_lines:
        difference = points.difference(line)
        # keeps all possible ways to remove all collinear points
        list_of_sets.append(final_result_faster_brute(difference))

    pre_sum = sum(list_of_sets)
    pre_sum.depth = pre_sum.depth + 1
    return pre_sum
