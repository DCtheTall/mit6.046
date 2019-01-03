"""
Lecture 22: Encryption
RSA Algorithm
-------------
RSA is a form of asymmetric-key cryptography. Let us say
Alice wants to receive messages from Bob.

Alice chooses two prime integers, p, q, and computes

N = p * q.

Alice chooses an integer, e, s.t.

1 < e < N and gcd(e, (p - 1) * (q - 1)) = 1.

Alice publishes (N, e) so that Bob can encrypt
messages by computing

c = (m ** e) % N

where m is the message, an integer coprime to
p and q. Bob sends the ciphertext, c, to Alice.

Alice is able to decrypt messages by computing an
integer, d, such that

d * e = 1 + k * ((p - 1) * (q - 1))

where k is a non-negative integer. Alice can decrypt
a encrypted message, c, using

m = (c ** d) % N.

The security of this cryptosystem comes from the fact
that for large p and q, it is computationally difficult to
factor N = p * q. Without knowing p and q, the decryption
exponent, d, is also computationally difficult to compute,
even with knowledge of N and e.

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
  Service object represents a server which means
  to send encrypted messages between another instance
  using RSA to encrypt integer messages.

  """
  def __init__(self, p, q):
    self.p = p
    self.q = q
    self.N = p * q
    self.phi = (p - 1) * (q - 1)
    self.e = randint(2, self.N - 1)
    while gcd(self.e, self.phi) == 1:
      self.e = randint(2, self.N - 1)
    self.d = mod_inverse(self.e, self.phi)
    self.dst_N = None
    self.dst_e = None
    self.port = None

  def encrypt_msg(self, m):
    """
    Encrypt a message to the other service.

    """
    return (m ** self.dst_e) % self.dst_N

  def receive_key(self, N, e):
    """
    Receive a published encryption key.

    """
    self.dst_N = N
    self.dst_e = e

  def receive_msg(self, c):
    """
    Receive an encrypted message from the other service
    and print the plaintext.

    """
    msg = (c ** self.d) % self.N
    print msg

  def send_msg(self, msg):
    """
    A mock public method for sending an integer message
    using the encryption scheme to another service.

    """
    self.port.send_msg(self.encrypt_msg(msg))


class Port(object):
  """
  Port object represents one direction in the two-way
  channel between two Service instances.

  """
  def __init__(self, src):
    self.src = src
    self.dst = None

  def send_key(self):
    """
    Publish the RSA encryption key across the
    channel.

    """
    self.dst.receive_key(self.src.N, self.src.e)

  def send_msg(self, ciphertext):
    """
    Encrypt then send a message through the channel.

    """
    self.dst.receive_msg(ciphertext)


class Channel(object):
  """
  Channel object represents a two-way communication
  channel between two services. Messages over the
  channel are assumed to be public, and information
  that is only stored in Service instances is meant
  to mock private data.

  """
  def __init__(self, u, v):
    u.port = Port(u)
    v.port = Port(v)
    u.port.dst = v
    v.port.dst = u
    self.ports = [u.port, v.port]

  def publish_keys(self):
    """
    Publish the service keys to either
    end of the channel.

    """
    for port in self.ports:
      port.send_key()
