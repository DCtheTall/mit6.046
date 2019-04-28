# Python Implementations of Algorithms Covered in MIT 6.046

by Dylan Cutler (DCtheTall)

## Topics Covered

- Interval scheduling ([lecture 1](#lecture-1))
- Convex hull divide-and-conquer algorithm ([lecture 2](#lecture-2))
- Order stastics and median finding ([lecture 2](#lecture-2))
- Discrete Fourier Transform ([lecture 3](#lecture-3))
- Van Embde Boas tree ([lecture 4](#lecture-4))
- B-Tree ([lecture 5](#lecture-5))
- Freivald's randomized matrix multiplication algorithm ([lecture 6](#lecture-6))
- Quicksort ([lecture 6](#lecture-6))
- Skip list ([lecture 7](#lecture-7))
- Universal hash functions ([lecture 8](#lecture-8))
- Perfect hash table ([lecture 8](#lecture-8))
- Order statistic tree ([lecture 9](#lecture-9))
- Range tree ([lecture 9](#lecture-9))
- Finger search tree ([lecture 9](#lecture-9))
- Optimal binary search tree ([lecture 10](#lecture-10))
- Longest palindromic substring ([lecture 10](#lecture-10))
- Floyd-Warshall all-pairs shortest path algorithm ([lecture 11](#lecture-11))
- Johnson's all-pairs shortest path algorithm ([lecture 11](#lecture-11))
- Matrix multiplication all-pairs shortest path algorithm ([lecture 11](#lecture-11))
- Minimal spanning tree ([lecture 12](#lecture-12))
- Kruskal's greedy algorithm ([lecture 12](#lecture-12))
- Prim's greedy algorithm ([lecture 12](#lecture-12))
- Flow networks ([lecture 13-14](#lecture-13-14))
- Ford-Fulkerson's algorithm ([lecture 13-14](#lecture-13-14))
- Linear programming ([lecture 15](#lecture-15))
- Simplex algorithm ([lecture 15](#lecture-15))
- Approximation algorithms ([lecture 17](#lecture-17))
- Fixed parameter tractable problems ([lecture 18](#lecture-18))
- Synchronous leader election ([lecture 19](#lecture-19))
- Synchronous breadth-first spanning tree ([lecture 19](#lecture-19))
- Synchronous Bellman-Ford shortest path distributed algorithm ([lecture 19](#lecture-19), [lecture 20](#lecture-20))
- Distributed maximal independent subset algorithm ([lecture 19](#lecture-19))
- Asynchronous leader election ([lecture 20](#lecture-20))
- Asynchronous breadth-first spanning tree ([lecture 20](#lecture-20))
- Asynchronous Bellman-Ford shortest path distributed algorithm ([lecture 20](#lecture-20))
- Diffie-Hellman key exchange ([lecture 22](#lecture-22))
- RSA public key encryption ([lecture 22](#lecture-22))
- Knapsack cryptosystem ([lecture 22](#lecture-22))
- Cache-oblivious scan ([lecture 23](#lecture-23))
- Strassen's matrix multiplication algorithm ([lecture 23](#lecture-23))
- LRU cache ([lecture 24](#lecture-24))

## Lecture 1

### `intervalscheduling.py`

This progrsm covers interval scheduling, an optimization problem where a
service attempts to complete as many tasks as possible in a given window
given that it can only perform one task at once. It also has a dynamic
programming algorithm for finding the optimal schedule if each job has a
given weight.

## Lecture 2

### `convexhull.py`

This program contains both a brute force and a divide and conquer
algorithm for finding the convex hull of a set of points in 2D space.
It compares the runtime of both algorithms as well.

### `median.py`

This program contains a linear-time divide-and-conquer rank algorithm
which, given a list of comparable objects, finds the object of rank
`i` (where `i` ranges from 0 to the length of the list minus 1).

## Lecture 3

### `fourier.py`

This program contains an implementation of Discrete Fourier Transform
which is used for an efficient polynomial multiplication algorithm.

## Lecture 4

### `vanembdeboas.py`

This program contains an implementation of a vEB tree for storing
integers. It supports insert, delete, predecessor, and successor
in `O(log(log(N)))` time.

## Lecture 5

### `btree.py`

The lecture on amortization mentions 2-3 trees, which is a particular
type of a data structure called a B-tree. This program is an implementation
of a B-tree in Python, using an inheritance chain to modularize the node
definition.

## Lecture 6

### `freivalds.py`

This program contains a randomized algorithm for efficient matrix multiplication
verification in `O(N ** 2)` time where `N` is the sidelength of the square matrices
being multiplied.

### `quicksort.py`

This program covers 3 different implementations of quicksort, each differ by how
they choose the pivot element.

## Lecture 7

### `skiplist.py`

This program contains an implementation of a skip list data structure meant for storing
integers.

## Lecture 8

### `universalhash.py`

This program contains an implementation of a hash table which uses a universal hash
function to compute hashes for the keys. Collisions are handled using chaining.

### `perfecthash.py`

This program contains an implementation of a perfect hash table, which can acces any
key in the table in `O(1)` time.

## Lecture 9

### `avl/orderstatistic.py`

This program contains an implementation of a order-statistic tree, an augmented
binary search tree which can compute the rank of a node or select a node of a given
rank all in `O(log(N))` time where `N` is the number of nodes in the tree.

### `avl/rangetree.py`

This program contains an implementation of a 1D range tree which stores integers.
It can query all nodes in a given range in `O(log(N))` time where `N` is the number
of nodes in the tree.

### `btree/fingersearchtree.py`

This program contains an implementation of an augmented B-tree which only stores
data in the leaf nodes. This tree obeys the finger search property, meaning it can
find any node `x` from another node `y` in `O(log(|rank(x) - rank(y)|))` time.

## Lecture 10

### `coins.py`

This program contains a dynamic-programming (DP) algorithm for playing the
alternating coin game (see program for rules) optimally.

### `optimalbst.py`

This program contains a DP algorithm for constructing an optimal binary search
tree given the search frequencies of each value in the tree.

### `palindrome.py`

This program contains a DP algorithm for finding the longest palindromic substring
of a given string.

## Lecture 11

### `dp.py`

This program contains a DP algorithm for finding the shortest paths between all
pairs of vertices in a graph.

### `floydwarshall.py`

This program contains an implementation of the Floyd-Warshall all pairs shortest path
algorithm, another DP algorithm more efficient than the algorithm in `dp.py`.

### `johnsons.py`

This program contains an implementation of Johnson's all pairs shortest path algorith.
This algorithm uses Bellman-Ford's single source shortest path algorithm to create
a heuristic function which allows us to run Dijkstra's shortest path algorithm from
every node.

### `matrixmult.py`

This program contains a matrix multiplication all pairs shortest path algorithm using
a different definition of addition and multiplication.

## Lecture 12

### `kruskals.py`

This program contains an implementation of Kruskal's greedy algorithm for finding the
minimal spanning tree of a weighted digraph. It uses a disjoint set data structure
defined in `disjointset.py` to implement the algorithm.

### `prims.py`

This program contains an implementation of Prim's greedy algorithm for finding the
minimal spanning tree of a weighted digraph. It uses a priority queue (not a very good
one) defined in `priorityqueue.py` to implement the algorithm.

## Lecture 13-14

### `flownetwork.py`

This program contains an implementation of a flow network, a network where each
edge has a maximum capacity. It also is able to calculate the residual network,
which is discussed in the program.

### `fordfulkerson.py`

This program contains an implementation of Ford-Fulkerson's algorithm for finding
the maximum allowed traffic through a flow network.

### `baseball.py`

This program shows how the Ford-Fulkerson algorithm can be used to determine if
a baseball team has a chance to win its division given the current season stats.

## Lecture 15

### `linprog.py`

This program uses scipy's linear programing library to demonstrate how linear
programming can be used to solve the flow network problem and the shortest path
problem.

### `simplex.py`

This program contains a crude implementation of the simplex algorithm, a linear
programming solver.

## Lecture 17

### `partition.py`

This program contains an implementation of an approximation algorithm for finding
the most optimal partition of a given set of real numbers.

### `setcover.py`

This program contains an approximation algorithm for solving
the set cover problem, see the program for more information.

### `vertexcover.py`

This program contains an approximation algorithm for solving the vertex cover
graph problem. See the program for more information.

## Lecture 18

### `kvertexcover.py`

This program contains an algorithm to solve the k-vertex cover graph problem,
a fixed-parameter tractable problem.

### `kernelization.py`

This program contains an implementation of kernelization, a process used to make
algorithms for (FPT) problems more efficient.

## Lecture 19

### `leaderelection.py`

This program contains an implementation of an algorithm for electing a leader
node in a synchronized distributed network.

### `bfst.py`

This program contains an implementation of an algorithm for finding a
breadth-first spanning tree across a synchronized distributed network.

### `maximalindepset.py`

This program contains an implementation of an algorithm for finding a
maximal independent subset in a synchronized distributed network.

### `bellmanford.py`

This program contains an implementation of Bellman-Ford's shortest path
algorithm for a synchronized distributed network.

## Lecture 20

### `bellmanford.py`

This program is an extended version of the Bellman-Ford algorithm covered
in lecture 19.

### `asyncleaderelection.py`

This program contains an implementation of an algorithm for electing a leader
node in a asynchronous distributed network.

### `asyncbfst.py`

This program contains an implementation of an algorithm for finding a
breadth-first spanning tree across a asynchronous distributed network.

### `asyncbellmanford.py`

This program contains an implementation of Bellman-Ford's shortest path
algorithm for a asynchronous distributed network.

## Lecture 22

All crypto algorithms covered in this lecture are for educational purposes,
they are not to be used as an encryption algorithm for an application as
they are not guaranteed to be secure.

### `diffiehellman.py`

This program contains an implementation of mock services that can do
Diffie-Hellman key exchanges for symmetric key cryptography.

### `rsa.py`

This program contains an implementation of mock services that can
use RSA asymmetic key cryptography.

## `knapsack.py`

This program contains an implementation of the knapsack cryptosystem,
a system which we now know is no longer secure.

## Lecture 23

### `scan.py`

This program contains classes which implement the external memory model
covered in lecture. It also implements a contiguous array which can
sum its elements (perform a linear scan) in `O(N/B + 1)` time where `N`
is the size of the array and `B` is the block size.

### `strassen.py`

This program contains an implementation of Strassen's divide-and-conquer
matrix multiplication algorithm.

## Lecture 24

### `lru.py`

This program contains an implementation of an LRU cache which uses a doubley
linked list to do write and reads in constant time. This program is a solution
to [LeetCode problem 146](https://leetcode.com/problems/lru-cache/).
