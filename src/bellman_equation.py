"""
Creating general functions to solve dynamic programs
"""
from typing import List, Tuple
import numpy as np
from collections import namedtuple

WEIGHTS = np.array([1,2,3,4,5,6,7])
VALUES = np.array([7, 5, 2, 8, 7, 9, 4])

knapsackState = namedtuple('knapsackState', ['remaining_weight', 'item_idx'])

def actions(state: knapsackState)->List:
    """returns a list of actions given our current state

    Args:
        state (_type_): _description_

    Returns:
        List: returns a list 0 and 1. 0 for leave. 1 for take
    """
    return [0, 1]

def transition(state: knapsackState, action: int):
    """takes in our current state and our choice of action and returns a new state

    Args:
        state (_type_): _description_
        action (_type_): _description_
    """
    if action ==1: # we take the object
        return knapsackState(state.remaining_weight - WEIGHTS[state.item_idx],
                             state.item_idx + 1)
    else: # do not take object
        return knapsackState(state.remaining_weight, state.item_idx + 1)

def immediate_reward(state:knapsackState, action)->float:
    """gives us our immediate payoff

    Args:
        state (_type_): _description_
        action (_type_): _description_

    Returns:
        float: _description_
    """
    ...

def bellman_equation(state: knapsackState)-> float:
    """solves dynamic programming

    Args:
        state (Tuple[int,int]): _description_

    Returns:
        float: _description_
    """
    max_reward = -np.inf
    for a in actions(state):
        new_state = transition(state, a)
        future_reward = bellman_equation(new_state)
        reward = immediate_reward(state, a) + future_reward
        if reward > max_reward:
            max_reward = reward