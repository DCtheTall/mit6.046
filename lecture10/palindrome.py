"""
Longest Palindromic Subsequence
-------------------------------
Given a string, find the longest subsequence
of that string that is a palindrome

e.g.

The longest palindromic subsequence of "underqualified" is "deified"

The longest palindromic subsequence of "turboventilator" is "rotator"

"""


def longest_palindromic_subseq_length(dp, S, i, j):
  """
  Get the length of the longest palindromic sequence
  in a string

  This is the algorithm covered in the lecture

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
        longest_palindromic_subseq_length(dp, S, i + 1, j - 1)
  else:
    dp[(i, j)] = \
      max(
        longest_palindromic_subseq_length(dp, S, i + 1, j),
        longest_palindromic_subseq_length(dp, S, i, j - 1))
  return dp[(i, j)]


def longest_palindromic_subseq(dp, S, i, j):
  """
  Get the longest palindromic subsequence from a string
  using a modified version of the algorithm above

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
        longest_palindromic_subseq(dp, S, i + 1, j - 1) + \
        S[i]
  else:
    s_i = longest_palindromic_subseq(dp, S, i + 1, j)
    s_j = longest_palindromic_subseq(dp, S, i, j - 1)
    dp[(i, j)] = s_i if len(s_i) > len(s_j) else s_j
  return dp[(i, j)]
