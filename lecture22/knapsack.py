"""
Lecture 22: Encryption
Merkle-Hellman Knapsack Cryptosystem
------------------------------------
This program is an example of a mock Merkle-Hellman knapsack
cryptosystem between two services. This system is another example
of an asymmetric-key cryptosystem.

In this example, let us say Alice wants to receive messages from
Bob, so she will publish an encryption key which only she can
decrypt. In this example, the messages between services will be unsigned
32 bit integers.

Alice generates a secret key, W, in this case is a superincreasing
sequence, i.e. a sequence where each element w_i obeys the inequality
below:

W[i] > sum(W[j] for j in range(1, i)).

She then chooses a random integer q s.t.

q > sum(W)

and then chooses a random integer r s.t. gcd(r, q) = 1, i.e.
r and q are coprime. Alice then publishes the sequence B where
each element b_i is given by

B = (r * w) % q for w in W.

The public key is B and the private key is (W, q, r). Bob can
encrypt a 32 bit unsigned integer message, m, by computing the
ciphertext, c, given by

c = sum((m & (1 << i)) * b for i, b in enumerate(B)).

In order for Alice to decrypt the message from Bob, she first
needs to compute the inverse of r in the multiplicate group of
integers modulo q. Since gcd(r, q) = 1 this can be computed
using the extended Euclidean algorithm. When Alice receives
a ciphertext, c, she first computes

c' = (c * s) % q = sum(((m & (1 << i)) * b * s) % q for b in B).

Since s * r = 1 mod q, it follows that

c' = sum(((m & (1 << i)) * W[i]) % q for i in range(len(W)))

Since W is a superincreasing sequence, one can traverse W
from greatest to least value and see if each W[i] > c', if
it is, subtract W[i] from c' and set the i^th bit of the
message to 1. Traverse W until c' is reduced to 0, and the
resulting 32 bits is the message Bob sent.

The apparent hardness of this cryptosystem comes from the computational
difficulty of computing which elements in B make up the ciphertext,
c, without knowledge of (W, q, r). Knowing W, q, r makes the problem
solvable in polynomial time. However, this cryptosystem has been shown
to be broken.

"""


from random import randint


def gcd(a, b):
  """
  Compute GCD of two integers.

  """
  a, b = max(a, b), min(a, b)
  while b != 0:
    a, b = b, a % b
  return a


def mod_inverse(x, n):
  """
  Compute the inverse of x in the multiplicative
  group of Z/nZ, i.e. the integer y such that

  x * y = 1 mod N.

  The algorithm uses the extended Euclidean
  algorithm to find the inverse efficiently.

  """
  a, b = n, x
  ta, tb = 0, 1
  while b != 0:
    q = a / b
    a, b = b, a % b
    ta, tb = tb, ta - (q * tb)
  if ta < 0:
    ta += n
  return ta


class Service(object):
  """
  Service object represents a server or process that is
  using the knapsack cyptosystem to exchange encrypted
  32-bit unsigned integers with another Service instance.

  """
  def __init__(self):
    cur_sum = 0
    self.W = [] # private key
    for _ in range(32):
      cur_sum += randint(1, 100)
      self.W.append(cur_sum)
    self.q = randint(cur_sum + 1, 2 * cur_sum)
    self.r = randint(1, 2 * q)
    while gcd(self.r, self.q) != 1:
      self.r = randint(1, 2 * q)
    self.B = [(self.r * w) % self.q for w in self.W] # public key
    self.s = mod_inverse(self.r, self.q)
    self.dst_B = None # partner's public key
    self.port = None

  def encrypt_msg(self, msg):
    """
    Use the partner's public key to encrypt a message
    (a 32 bit unsigned integer), into an encrypted
    integer c.

    """
    c = 0
    for i in range(32):
      c += (msg & (1 << i)) * self.dst_B[i]
    return c

  def receive_key(self, B):
    """
    Receive the public key from the message
    partner.

    """
    self.dst_B = B

  def receive_msg(self, c):
    """
    Decrypt a message from another service
    instance which was sent this service's public
    key and used it to encrypt the ciphertext,
    c.

    """
    c = (c * self.s) % self.q
    msg = 0
    for i, w in reversed(self.W):
      if c >= w:
        msg += (1 << (31 - i))
        c -= w
    print msg

  def send_msg(self, msg):
    """
    Mock public method for sending an encrypted
    message using this service to its partner,
    triggering the receive_msg callback.

    """
    self.port.send_msg(self.encrypt_msg(msg))


def Port(object):
  """
  Port object represents a one way connection between two
  services. The source service pushes messages to the
  destination vertex.

  """
  def __init__(self, src):
    self.src = src
    self.dst = None

  def send_key(self):
    """
    Send a public key from one service to the other.

    """
    self.dst.receive_key(self.src.B)

  def send_msg(self, ciphertext):
    """
    Send an encrypted message through the port.

    """
    self.dst.receive_msg(ciphertext)


class Channel(object):
  """
  Channel object represents a connection between
  two services which consists of two-one way
  ports.

  """
  def __init__(self, u, v):
    u.port = Port(u)
    v.port = Port(v)
    u.port.dst = v
    v.port.dst = u
    self.ports = [u.port, v.port]

  def publish_keys():
    """
    Have the services exchange their public
    keys.

    """
    for port in self.ports:
      port.send_key()