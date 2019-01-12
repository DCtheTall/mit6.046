"""
Lecture 10: Dynamic Programming
Alternating Coin Game
---------------------
Consider a game where you have a list
with an even number of coins with
positive integer values

v_0, v_1, ..., v_i, ..., v_(n - 1)

Each player alternates picking either the
leftmost or rightmost coin until there are
no coins left. Whichever player picks coins
that add to the highest value wins.

It can be easily shown that the player who
moves first can always force a win.

This program contains a function which given a
list of coins, returns the most the first player
can win assuming his opponent is also playing
optimally.

"""


def dp_max_coin_value(dp, coins, i, j):
  """
  Recursive function which computes the maximum
  possible value assuming the opponent also plays
  optimally

  It uses memoization to speed up performance
  with a Python dictionary named dp "dynamic programming"

  """
  if (i, j) in dp:
    return dp[(i, j)]
  if i > j:
    return 0
  elif i == j:
    dp[(i, j)] = coins[i]
  else:
    dp[(i, j)] = max(
      coins[i] + min(
        dp_max_coin_value(dp, coins, i + 1, j - 1),
        dp_max_coin_value(dp, coins, i + 2, j),
      ),
      coins[j] + min(
        dp_max_coin_value(dp, coins, i + 1, j - 1),
        dp_max_coin_value(dp, coins, i, j - 2),
      ),
    )
  return dp[(i, j)]


def max_possible_value(coins):
  """
  Get the maximum possible value the first
  player can accumulate given a list
  of coins

  """
  return dp_max_coin_value(
    dict(), coins, 0, len(coins) - 1)
