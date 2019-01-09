"""
Lecture 3: Divide and Conquer:
Convex Hull
-----------
Topics covered:
- Divide and conquer

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
  n = len(S)
  if n < 2:
    return S
  L, R = S[:n // 2], S[n // 2:]
  return merge(less, mergesort(less, L), mergesort(less, R))


def curry_clockwise_compare(center):
  """
  Returns the clockwise comparison function
  for sorting elements in clockwise order
  given a center point

  It returns a function used for comparison in sort,
  in this implementation, the comparison function is
  curried with the center of the circle you are comparing
  the points' relative positions to

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


def calculate_center(S):
  """
  Calculate the center of a list
  of points, S

  """
  cx = 0.
  cy = 0.
  n = len(S)
  for p in S:
    cx += p[0] / n
    cy += p[1] / n
  return (cx, cy)


def brute_force_convex_hull(S):
  """
  Brute force algorithm
  for finding the convex hull of
  a set of points

  The idea is you check for points where every other
  point is only on one side of the line defined
  by the chosen two. This indicates these two points belong
  to an edge of the convex hull

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
  convex_hull_points = list(convex_hull_points)
  center = calculate_center(convex_hull_points)
  return mergesort(
    curry_clockwise_compare(center), convex_hull_points)


def divide_and_conquer_convex_hull(S):
  """
  Recursive convex hull divide and merge
  function that operates on a list of
  points (tuples of x and y coords) assuming
  that they are sorted by their x coordinate

  Complexity: O(n * (log(n) ** 2))

  Since it takes O(n * log(n)) work over O(log(n)) recursions

  """
  n = len(S)
  if n <= 3:
    # We can treat this case as approximately constant time
    # because it's only operating on a maximum of 3 elements
    # Since for 3 points finding a convex hull is trivial
    center = calculate_center(S)
    return mergesort(
      curry_clockwise_compare(center), S)
  # Split the points in half by x-coordinate
  sorted_S = mergesort(lambda p1, p2: p1[0] < p2[0], S)
  L, R = sorted_S[:n // 2], sorted_S[n // 2:]
  middle_x = (sorted_S[n // 2 - 1][0] + sorted_S[n // 2][0]) / 2.
  L, R = \
    divide_and_conquer_convex_hull(L), \
    divide_and_conquer_convex_hull(R)
  l, r = len(L), len(R)
  # Find the middle X coordinate between the extremes of either set
  y_coord = lambda i, k: \
    get_line_from_two_points(L[i], R[k])(middle_x)
  # Use the "two finger" algorithm method to find the indices of the topmost
  # and bottommost in each solution of the subproblem
  rightmost_L = L.index(sorted_S[n // 2 - 1])
  leftmost_R = R.index(sorted_S[n // 2])
  i_top = rightmost_L
  k_top = leftmost_R
  while y_coord(i_top, k_top) < y_coord((i_top - 1) % l, k_top) \
    or y_coord(i_top, k_top) < y_coord(i_top, (k_top + 1) % r):
      if y_coord(i_top, k_top) < y_coord(i_top, (k_top + 1) % r):
        k_top = (k_top + 1) % r
      else:
        i_top = (i_top - 1) % l
  i_bot = rightmost_L
  k_bot = leftmost_R
  while y_coord(i_bot, k_bot) > y_coord((i_bot + 1) % l, k_bot) \
    or y_coord(i_bot, k_bot) > y_coord(i_bot, (k_bot - 1) % r):
      if y_coord(i_bot, k_bot) > y_coord(i_bot, (k_bot - 1) % r):
        k_bot = (k_bot - 1) % r
      else:
        i_bot = (i_bot + 1) % l
  # Merge step
  result = []
  i = i_bot
  while i != i_top:
    result.append(L[i])
    i = (i + 1) % l
  result.append(L[i])
  k = k_top
  while k != k_bot:
    result.append(R[k])
    k = (k + 1) % r
  result.append(R[k])
  return result
