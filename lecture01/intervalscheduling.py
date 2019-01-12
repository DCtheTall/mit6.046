"""
Lecture 1: Interval Scheduling
------------------------------
Topics covered:
- Greedy algorithms
- Dynamic programming

"""


class Request:
  """
  Request

  start: int, assume >= 0
  finish: int, assume > 0

  """

  def __init__(self, start, finish):
    self.start = start
    self.finish = finish

  def is_compatible(self, req):
    return self.finish <= req.start \
      or self.start >= req.finish


def greedy_largest_compatible_subset(requests):
  """
  Given requests for a single resource
  and a list of requests

  We want to find the largest subset
  of compatible requests

  A request is compatible if
  r1.finish <= r2.start or r1.start >= r2.finish

  Greedy algorithm:
  - Sort the array by finish time
  - Pick request with earliest finish time, r
  - Add r to the result
  - Iterate over the array until you reach
    the next compatible result

  requests: List[int]
  start: Dict[int]int
  finish: Dict[int]int

  Complexity: O(n * log(n))

  """
  result = []
  i = 0
  requests.sort(key=lambda r: r.finish)
  n = len(requests)
  while i < n:
    best = requests[i]
    result.append(best)
    while i < n and \
      not requests[i].is_compatible(best):
        i += 1
  return result


class WeightedRequest(Request):
  """
  WeightedRequest

  weight: int

  """
  def __init__(self, start, finish, weight):
    Request.__init__(self, start, finish)
    self.weight = weight


def optimal_compatible_subset(requests):
  """
  Get optimal weighted subset

  Uses dynamic programming to get the subset
  of the requests with the largest weight

  """
  dp_weights = dict()
  dp_subsets = dict()
  finishes = {r.finish for r in requests}
  while finishes:
    x = max(finishes)
    finishes.remove(x)
    subsets = dict()
    for req in [r for r in requests if r.start >= x]:
      w = req.weight + dp_weights[req.finish]
      subsets[w] = [req] + dp_subsets[req.finish]
    if not subsets:
      dp_weights[x] = 0
      dp_subsets[x] = []
    else:
      w = max(subsets)
      dp_weights[x] = w
      dp_subsets[x] = subsets[w]
  for req in [r for r in requests if r.start < min(dp_weights)]:
    w = req.weight + dp_weights[req.finish]
    if 0 not in dp_weights or w > dp_weights[0]:
      dp_weights[0] = w
      dp_subsets[0] = [req] + dp_subsets[req.finish]
  return (dp_weights[0], dp_subsets[0])
