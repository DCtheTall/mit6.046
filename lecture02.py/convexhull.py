"""
Convex Hull
-----------

Find the convex hull of a set of
points of size n:

S = {(x_i, y_i) for i in 1, 2, ..., n }

given that no 2 points have the same x or y coordinate
and that no 3 points are colinear

Here we will represent the set as a list of tuples
of floats

"""


def get_line_from_two_points(p1, p2):
  """
  Returns a function which takes
  an x-coordinate and returns the
  corresponding y-coordinate on the
  line defined by the points p1, p2

  """
  slope = p2[1] - p1[1]
  slope /= p2[0] - p1[0]
  return lambda x: (slope * (x - p1[0])) + p1[1]


def merge(less, L, R):
  """
  Merge two lists of tuples
  by their first element

  First argument is the comparison function
  returns true if arg1 is "less" than arg2

  """
  i = 0
  k = 0
  result = []
  while i < len(L) or k < len(R):
    if i == len(L):
      result.append(R[k])
      k += 1
    elif k == len(R) or less(L[i], R[k]):
      result.append(L[i])
      i += 1
    else:
      result.append(R[k])
      k += 1
  return result


def mergesort(less, S):
  """
  Merge sort the list of points by x-coordinate

  """
  if len(S) < 2:
    return S
  n = len(S)
  L, R = S[:n // 2], S[n // 2:]
  return merge(less, mergesort(less, L), mergesort(less, R))


def curry_clockwise_compare(center):
  """
  Returns the clockwise comparison function
  for sorting elements in clockwise order
  given a center point

  From: https://stackoverflow.com/questions/6989100/sort-points-in-clockwise-order

  """
  def clockwise_compare(p1, p2):
    if p1[0] - center[0] >= 0 and p2[0] - center[0] < 0:
        return True
    if p1[0] - center[0] < 0 and p2[0] - center[0] >= 0:
        return False
    if p1[0] - center[0] == 0 and p2[0] - center[0] == 0:
      if p1[1] - center[1] >= 0 or p2[1] - center[1] >= 0:
        return p1[1] > p2[1]
      return p2[1] > p1[1]
    det = (p1[0] - center[0]) * (p2[1] - center[1])
    det -= (p1[1] - center[1]) * (p2[0] - center[0])
    if det < 0:
      return True
    if det > 0:
      return False
  return clockwise_compare


def brute_force_convex_hull(S):
  """
  Brute force algorithm
  for finding the convex hull of
  a set of points

  complexity: O(n ** 3)

  """
  convex_hull_points = set()
  for p1 in S:
    for p2 in S:
      if p1 == p2:
        continue
      line = get_line_from_two_points(p1, p2)
      all_points_above_line = None
      is_convex_segment = True
      for p3 in S:
        if p3 == p1 or p3 == p2:
          continue
        y = line(p3[0])
        if all_points_above_line is None:
          all_points_above_line = (y < p3[1])
        elif (y < p3[1]) != all_points_above_line:
          is_convex_segment = False
          break
      if is_convex_segment:
        convex_hull_points.add(p1)
        convex_hull_points.add(p2)
  cx = 0.
  cy = 0.
  convex_hull_points = list(convex_hull_points)
  n = len(convex_hull_points)
  for p in convex_hull_points:
    cx += p[0] / n
    cy += p[1] / n
  return mergesort(
    curry_clockwise_compare((cx, cy)), convex_hull_points)


# TODO divide and conquer method
