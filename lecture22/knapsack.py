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

"""
