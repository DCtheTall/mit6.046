"""
Lecture 17: Approximation Algorithms
Vertex Cover
------------
This program contains two approximation algorithms
for solving the vertex cover problem for an undirected
graphs G(V, E).

A vertex cover is a subset V' of V such that
forall (u, v) in E, either u or v is in V'.
The goal is to find the smallest set V' which
meets these requirements.

This program contains two approximation algorithms
for finding the minimal vertex cover:

The first is a greedy algorithm which selects
the vertex with the highest degree, u, and add u
to V'. Afterwards remove each vertex which is adjacent to u,
and repeat this process until all vertices are covered.

It is shown in lecture that this algorithm is a
log(log(n))-approximation algorithm.

The second is an algorithm which randomly selects
an edge, (u, v), and adds both to V'. Afterwards
remove all edges with u or v from consideration and
repeat until all edges are covered.

"""


class Graph(object):
  """
  Graph class which will be used for the
  approximation algorithms. It contains
  a set of vertices and an adjacency list
  to represent the edges

  The constructor expects a set or list
  of tuples representing the edges of
  the graph. For this example, we will
  make the assumption that each vertex
  in the graph belongs to an edge.

  """
  def __init__(self, edges):
    self.adjacency_list = dict()
    self.vertices = set()
    for u, v in edges:
      self.vertices.add(u)
      self.vertices.add(v)
      try:
        self.adjacency_list[u].append(v)
      except:
        self.adjacency_list[u] = [v]
      try:
        self.adjacency_list[v].append(u)
      except:
        self.adjacency_list[v] = [u]


def highest_degree_vertex_cover(graph):
  """
  This function finds a vertex cover of an undirected graph
  using a greedy algorithm which picks the vertex
  with the highest degree, u, then removing all vertices
  that are adjacent to u from consideration.

  It is shown in lecture this is at best a
  log(log(n))-approximation algorithm.

  """
  if not isinstance(graph, Graph):
    raise TypeError(
      'highest_degree_vertex_cover must be called with an instance of Graph')
  cover = set()
  get_max_degree = lambda u: len(graph.adjacency_list[u])
  verts = set(graph.vertices)
  while verts:
    u = max(verts, key=get_max_degree)
    cover.add(u)
    verts.remove(u)
    for v in graph.adjacency_list[u]:
      verts.remove(v)
  return cover


def random_edge_vertex_cover(graph):
  """
  This function finds a vertex cover of an undirected graph
  by selecting a random edge from the graph, (u, v) then
  removing all edges with u or v.

  It is shown in lecture this is a 2-approximation
  algorithm.

  """
  if not isinstance(graph, Graph):
    raise TypeError(
      'random_edge_vertex_cover must be called with an instance of Graph')
  cover = set()
  edges = set()
  for u in graph.vertices:
    for v in graph.adjacency_list:
      if (v, u) in edges:
        continue
      edges.add((u, v))
  while edges:
    u, v = edges.pop()
    cover.add(u)
    cover.add(v)
    for e in edges:
      if u in e or v in e:
        edges.remove(e)
  return cover
