"""
Lecture 10: Dynamic Programming
Longest Palindromic Subsequence
-------------------------------
Problem:

Given a string, find the longest subsequence
of that string that is a palindrome

e.g.

The longest palindromic subsequence of "underqualified" is "deified"

The longest palindromic subsequence of "turboventilator" is "rotator"

This program provides 2 functions which

"""


def dp_palindrome_length(dp, S, i, j):
  """
  Recursive function for finding the length
  of the longest palindromic sequence
  in a string

  This is the algorithm covered in the lecture

  It uses memoization to improve performance,
  dp "dynamic programming" is a Python dict
  containing previously computed values

  """
  if i == j:
    return 1
  if (i, j) in dp:
    return dp[(i, j)]
  if S[i] == S[j]:
    if i + 1 == j:
      dp[(i, j)] = 2
    else:
      dp[(i, j)] = 2 + \
        dp_palindrome_length(dp, S, i + 1, j - 1)
  else:
    dp[(i, j)] = \
      max(
        dp_palindrome_length(dp, S, i + 1, j),
        dp_palindrome_length(dp, S, i, j - 1))
  return dp[(i, j)]


def longest_palindromic_subsequence_length(S):
  """
  Find the length of the longest palindromic
  subsequence of string S

  """
  n = len(S)
  return dp_palindrome_length(dict(), S, 0, n - 1)


def dp_longest_palindrome(dp, S, i, j):
  """
  Recursive function for finding the longest palindromic
  subsequence from a string using a modified version
  of the algorithm above

  """
  if i == j:
    return S[i]
  if (i, j) in dp:
    return dp[(i, j)]
  if S[i] == S[j]:
    if i + 1 == j:
      dp[([i, j])] = 2 * S[i]
    else:
      dp[(i, j)] = \
        S[i] + \
        dp_longest_palindrome(dp, S, i + 1, j - 1) + \
        S[i]
  else:
    s_i = dp_longest_palindrome(dp, S, i + 1, j)
    s_j = dp_longest_palindrome(dp, S, i, j - 1)
    dp[(i, j)] = s_i if len(s_i) > len(s_j) else s_j
  return dp[(i, j)]


def longest_palindromic_subsequence(S):
  """
  Find the longest palindromic subsequence
  of string S

  """
  n = len(S)
  return dp_longest_palindrome(dict(), S, 0, n - 1)
