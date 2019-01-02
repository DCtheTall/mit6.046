"""
Lecture 22: Encryption:
Diffie-Hellman Key Exchange
---------------------------
This program is a mock implementation of a Diffie-Hellman
key exchange between two services, A and B.

The key exchange starts by A and B publicly agreeing
on a prime number p and an integer g such that
gcd(p, g) = 1.

Service A computes c_a = (g ** a) % p where a is a
random integer, which it keeps private. Service A
then sends c_a to service B. Service B then computes
c_b = (g ** b) % p where b is a random integer and
sends c_b to service A.

Service A and B can now both compute the shared
private key

k = (c_a ** b) % p = (c_b ** a) % p = ((g ** a) ** b) % p

The security of this encryption scheme comes from the
fact that for a large p, then even if c_a, g, p are public,
it can still take p - 1 tries to find the random integer
exponent, a.

"""


from random import randint


class Service(object):
  """
  Service class represents a possible
  server or process which requires a key
  exchange with another instance of
  this process.

  """
  def __init__(self):
    self.base = None
    self.exponent = None
    self.key = None
    self.port = None
    self.prime = None

  def compute_key(self):
    return (self.base ** self.exponent) % self.prime

  def receive_base(self, base):
    """
    Receive the public base.

    """
    self.base = base

  def receive_public_key(self, payload):
    """
    Receive the public message from the
    other service. Computes the shared
    key.

    """
    self.key = (payload ** self.exponent) % self.prime

  def receive_prime(self, prime):
    """
    Receive the public prime.

    """
    self.prime = prime
    self.exponent = randint(2, prime ** 2)


class Port(object):
  """
  Port class represents a connection
  from one service to another. A Channel
  is a 2-way connection with 2 ports.

  """
  def __init__(self, src):
    self.src = src
    self.dst = None

  def send_base(self, base):
    """
    Send the base for exponentiation
    to either service.

    """
    self.dst.receive_base(base)

  def send_key(self):
    """
    Send the payload from the source service
    to the destination service.

    """
    self.dst.receive_public_key(self.src.compute_key())

  def send_prime(self, prime):
    """
    Send the modular base, a prime integer,
    for the key exchange.

    """
    self.dst.receive_prime(prime)


class Channel(object):
  """
  Channel class is a two way connection
  between Services for the key exchange.

  """
  def __init__(self, u, v):
    u.port = Port(u)
    v.port = Port(v)
    u.port.dst = v
    v.port.dst = u
    self.ports = [u.port, v.port]

  def publish_keys(self):
    """
    Exchange messages with the encrypted
    payloads to compute the shared key.

    """
    for port in self.ports:
      port.send_key()

  def publish_base(self, base):
    """
    Publish the base for exponentiation.

    """
    for port in self.ports:
      port.send_base(base)

  def publish_prime(self, prime):
    """
    Publish the prime modular base.

    """
    for port in self.ports:
      port.send_prime(prime)
