# Gridworld environment based on mdp.py
# Gridworld provides a basic environment for RL agents to interact with
#
# ---
# @author Yiren Lu
# @email luyiren [at] seas [dot] upenn [dot] edu
#
# MIT License

import mdp
import numpy as np
import unittest


class GridWorld(mdp.MDP):
  """
  Grid world environment
  """

  def __init__(self, grid, terminals, trans_prob=1):
    """
    input:
      grid        2-d list of the grid including the reward
      terminals   a set of all the terminal states
      trans_prob  transition probability when given a certain action
    """
    self.height = len(grid)
    self.width = len(grid[0])
    self.terminals = terminals
    self.grid = grid
    self.neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
    self.actions = [0, 1, 2, 3, 4]
    self.dirs = {0: 'r', 1: 'l', 2: 'd', 3: 'u', 4: 's'}
    #                   right,    left,     down,     up
    # self.action_nei = {0: (0,1), 1:(0,-1), 2:(1,0), 3:(-1,0)}

    # If the mdp is deterministic, the transition probability of taken a certain action should be 1
    # otherwise < 1, the rest of the probability are equally spreaded onto
    # other neighboring states.
    self.trans_prob = trans_prob

  def show_grid(self):
    for i in range(len(self.grid)):
      print self.grid[i]

  def get_grid(self):
    return self.grid

  def get_states(self):
    """
    returns
      a list of all states
    """
    return filter(
        lambda x: self.grid[x[0]][x[1]] != 'x',
        [(i, j) for i in range(self.height) for j in range(self.width)])

  def get_actions(self, state):
    """
    get all the actions that can be takens on the current state
    returns
      a list of (action, state) pairs
    """
    res = []
    for i in range(len(self.actions)):
      inc = self.neighbors[i]
      a = self.actions[i]
      nei_s = (state[0] + inc[0], state[1] + inc[1])
      if nei_s[0] >= 0 and nei_s[0] < self.height and nei_s[1] >= 0 and nei_s[
              1] < self.width and self.grid[nei_s[0]][nei_s[1]] != 'x':
        res.append((a, nei_s))
    return res

  def get_reward(self, state):
    """
    returns
      the reward on current state
    """
    if not self.grid[state[0]][state[1]] == 'x':
      return float(self.grid[state[0]][state[1]])
    else:
      return 0

  def get_transition_states_and_probs(self, state, action):
    """
    get all the possible transition states and their probabilities with [action] on [state]
    args
      state     (y, x)
      action    int
    returns
      a list of (state, probability) pair
    """
    if self.trans_prob == 1:
      inc = self.neighbors[action]
      nei_s = (state[0] + inc[0], state[1] + inc[1])
      if nei_s[0] >= 0 and nei_s[0] < self.height and nei_s[
              1] >= 0 and nei_s[1] < self.width:
        return [(nei_s, 1)]
      else:
        return [(state, 1)]
    else:
      action_states = self.get_actions(state)
      inc = self.neighbors[action]
      nei_s = (state[0] + inc[0], state[1] + inc[1])
      res = []

      if nei_s[0] >= 0 and nei_s[0] < self.height and nei_s[
              1] >= 0 and nei_s[1] < self.width:
        for i in range(len(action_states)):
          if action_states[i][0] == action:
            res.append((action_states[i][1], self.trans_prob))
          else:
            res.append(
                (action_states[i][1], (1 - self.trans_prob) / (len(action_states) - 1)))
      else:
        for i in range(len(action_states)):
          res.append((action_states[i][1], 1 / len(action_states)))
      return res

  def is_terminal(self, state):
    """
    returns
      True if the [state] is terminal
    """
    if state in self.terminals:
      return True
    else:
      return False

  def display_value_grid(self, agent):
    """
    prints a nice layout of the values in grid
    """
    value_grid = np.zeros((len(self.grid), len(self.grid[0])))

    for k in agent.values:
      value_grid[k[0]][k[1]] = float(agent.values[k])

    row_format = '{:>20.4}' * (len(value_grid) + 1)
    for row in value_grid:
      print row_format.format(*row)

  def display_policy_grid(self, agent):
    """
    prints a nice layout of the policy in grid
    """
    policy_grid = np.chararray((len(self.grid), len(self.grid[0])))

    for k in agent.values:
      if self.is_terminal((k[0], k[1])) or self.grid[k[0]][k[1]] == 'x':
        policy_grid[k[0]][k[1]] = '-'
      else:
        policy_grid[k[0]][k[1]] = self.dirs[agent.get_action((k[0], k[1]))]

    row_format = '{:>20}' * (len(policy_grid) + 1)
    for row in policy_grid:
      print row_format.format(*row)
