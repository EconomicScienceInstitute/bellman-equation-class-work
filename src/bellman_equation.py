"""
Creating general functions to solve dynamic programs
"""
from typing import List, Tuple
import numpy as np
from collections import namedtuple

WEIGHTS = np.array([1,2,3,4,5,6,7])
VALUES = np.array([7, 5, 2, 8, 7, 9, 4])

def actions(state)->List:
    """returns a list of actions given our current state

    Args:
        state (_type_): _description_

    Returns:
        List: _description_
    """
    return []

def transition(state, action):
    """takes in our current state and our choice of action and returns a new state

    Args:
        state (_type_): _description_
        action (_type_): _description_
    """

def immediate_reward(state, action)->float:
    """gives us our immediate payoff

    Args:
        state (_type_): _description_
        action (_type_): _description_

    Returns:
        float: _description_
    """

def get_max_reward(state: Tuple[int,int])-> float:
    """solves dynamic programming

    Args:
        state (Tuple[int,int]): _description_

    Returns:
        float: _description_
    """
    max_reward = -np.inf
    for a in actions(state):
        new_state = transition(state,a)
        future_reward = get_max_reward(new_state)
        reward = immediate_reward(state, a) + future_reward
        if reward > max_reward:
            max_reward = reward