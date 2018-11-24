"""
Lecture 13: Max Flow Min Cut
Ford-Fulkerson Algorithm
------------------------
Below is an implementation of the Ford-Fulkerson algorithm
for finding the maximum possible flow through a flow network
G(V, E) using a mathematical structure called a residual network
G_f(V, E_f) which is discussed in flownetwork.py

The Ford-Fulkerson algorithm traverses the residual network using
BFS to find a path from the source to the sink. If a path exists,
then the maximum flow has not been reached, and we should increase the
flow with the minimum residual capacity available on that path.

Once a path is not longer available from the source to the sink along
the residual network, we know that the maximum allowable flow is
being sent through the network.

"""


from flownetwork import FlowNetwork


def ford_fulkerson(network):
  """
  Ford-Fulkerson algorithm

  Below is an implementation of the algorithm
  described above using the FlowNetwork class
  defined in flownetwork.py

  This algorithm does not assume that the flows
  are integral values, and traverses each path
  it finds from the source to the sink in the
  residual network for the minimum available
  residual capacity. An insight found by studying
  the code provided here:

  https://www.geeksforgeeks.org/ford-fulkerson-algorithm-for-maximum-flow-problem/

  """
  if not isinstance(network, FlowNetwork):
    raise TypeError(
      'ford_fulkerson expects an instance of FlowNetwork')
  max_flow = 0
  while True:
    # Use BFS to check if a path exisits
    path_exists, parents = network.residual_network_bfs()
    if not path_exists:
      break
    # If one exists, look for the minimum residual capacity on the path
    u = network.sink
    min_capacity = float('inf')
    while u != network.src:
      u, v = parents[u], u
      if (u, v) in network.residual_capacities:
        min_capacity = min(
          min_capacity, network.residual_capacities[(u, v)])
    max_flow += min_capacity
    u = network.sink
    while u != network.src:
      u, v = parents[u], u
      if (u, v) in network.residual_capacities:
        network.residual_capacities[(u, v)] -= min_capacity
        network.flows[(u, v)] += min_capacity
  return max_flow


if __name__ == '__main__':
  # network in lecture
  network = FlowNetwork('s', 't', {
    ('s', 'a'): 3,
    ('s', 'b'): 2,
    ('a', 'd'): 2,
    ('b', 'a'): 3,
    ('b', 'c'): 3,
    ('c', 'd'): 3,
    ('c', 't'): 2,
    ('d', 'b'): 1,
    ('d', 't'): 3,
  })
  print ford_fulkerson(network) # correctly prints 4
