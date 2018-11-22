"""
Lecture 14: Incremental Improvement
-----------------------------------
This lecture extends the material covered
in lecture 13 on flow networks and the
Ford-Fulkerson algorithm. This program is an
implementation of an example at the end of
lecture: seeing if a particular baseball team
can possibly win their division given the
current standings.

"""


from flownetwork import FlowNetwork
from fordfulkerson import ford_fulkerson


class BaseballTeam(object):
  """
  BaseballTeam class records a team's name
  as well as the number of games the team
  won and how many they have remaining

  """
  def __init__(self, name, n_games):
    self.name = name
    self.games_remaining = n_games
    self.wins = 0

  def record_win(self):
    """
    Record a win for the team

    """
    self.games_remaining -= 1
    self.wins += 1

  def record_loss(self):
    """
    Record a loss for the team

    """
    self.games_remaining -= 1


class BaseballStandings(object):
  """
  BaseballStandings class keeps track of the
  standings for a particular division of teams

  It keeps track of how many games each team won,
  how many games they have remaining,
  (losses can be deduced if you know the total number of games)

  It also has a method which uses Ford-Fulkerson to determine
  if a particular team can possibly win their division
  covered in lecture

  """
  def __init__(self, team_names, games_per_pair):
    n = len(team_names)
    games_per_team = games_per_pair * (n - 1)
    self.team_names = team_names
    self.teams = [
      BaseballTeam(name, games_per_team)
      for name in team_names
    ]
    self.remaining_matchups = []
    for i in range(n):
      self.remaining_matchups.append([0] * n)
      for j in range(n):
        if i == j:
          self.remaining_matchups[i][j] = 0
        else:
          self.remaining_matchups[i][j] = games_per_pair

  def play_game(self, i, j, i_wins):
    """
    Play a game between between team i and team j

    i and j are integers representing the index of each
    team in the array used in the constructor

    i_wins is a boolean which determines which team won
    the game (True meaning team i won)

    """
    team_i, team_j = self.teams[i], self.teams[j]
    if not (isinstance(team_i, BaseballTeam) and
            isinstance(team_j, BaseballTeam)):
        raise Exception('Teams provided are not in the standings.')
    self.remaining_matchups[i][j] -= 1
    if i_wins:
      team_i.record_win()
      team_j.record_loss()
    else:
      team_i.record_loss()
      team_j.record_win()

  def use_standings_data(self, team_records, remaining_matchups):
    """
    Overwrite standings using the data provided when calling
    this method

    team_records is a list of tuples of lists of length 2
    which represent how many games each team won and how
    many games they have remaining

    remaining_matchups is a multidimensional list which represents
    the number of remaining matchups between each pair of teams

    """
    self.remaining_matchups = remaining_matchups
    for i, team in enumerate(self.teams):
      team.wins, team.games_remaining = team_records[i]

  def get_if_team_can_win(self, team_name):
    """
    Given the current standings, use Ford-Fulkerson
    to determine if a given team (string) can win

    The algorithm creates the flow network covered in
    lecture and then runs Ford-Fulkerson to determine
    if each edge from the source vertex is saturated.
    If it is, then we know that team has a chance of
    winning their division.

    """
    remaining_matchups = dict()
    n = len(self.teams)
    for i in range(n):
      if self.teams[i].name == team_name:
        team_to_verify = self.teams[i]
        continue
      for j in range(n):
        if self.teams[j].name == team_name or \
          (j, i) in remaining_matchups or \
            i == j:
              continue
        remaining_matchups[(i, j)] = self.remaining_matchups[i][j]
    capacities = {
        ('s', (i, j)): remaining_matchups[(i, j)]
        for i, j in remaining_matchups
    }
    for i, team in enumerate(self.teams):
      if team.name == team_name:
        continue
      capacities[(i, 't')] = \
        (team_to_verify.wins + team_to_verify.games_remaining) - team.wins
      for j, k in remaining_matchups:
        if j == i or k == i:
          capacities[((j, k), i)] = float('inf')
    network = FlowNetwork('s', 't', capacities)
    max_flow = ford_fulkerson(network)
    return max_flow == sum(remaining_matchups.values())


if __name__ == '__main__':
  """
  Example from:
  https://www.cs.princeton.edu/~wayne/papers/baseball_talk.pdf

  """
  teams = [
    'NY',
    'Baltimore',
    'Boston',
    'Toronto',
    'Detroit'
  ]
  standings = BaseballStandings(teams, 54)
  standings.use_standings_data(
    [
      (75, 59 + 28),
      (71, 63 + 28),
      (69, 66 + 27),
      (63, 72 + 27),
      (49, 86 + 27),
    ],
    [
      [0, 3, 8, 7, 3],
      [3, 0, 2, 7, 4],
      [8, 2, 0, 0, 0],
      [7, 7, 0, 0, 0],
      [3, 4, 0, 0, 0],
    ],
  )
  print standings.get_if_team_can_win('Detroit')
  # Correctly shows that Detroit could still win
