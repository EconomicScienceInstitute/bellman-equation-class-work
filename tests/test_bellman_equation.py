"""
writes one test per function of bellman equation
"""
import pytest
from bellman_equation import (KnapsackState, actions, transition, 
                              immediate_reward, bellman_equation,
                              WEIGHTS, VALUES)

def test_actions():
    """
    funcitonal test for the actions function
    """
    test_state = KnapsackState(0,0)
    assert actions(test_state) == [0,1]

def test_transition():
    assert True

def test_immediate_reward():
    assert True

def test_bellman_equation():
    start_state = KnapsackState(1,0)
    assert bellman_equation(start_state) == 7
    start_state = KnapsackState(2,0)
    assert bellman_equation(start_state) == 7
    start_state = KnapsackState(3,0)
    assert bellman_equation(start_state) == 13

@pytest.mark.parametrize("state, expected", [
    (KnapsackState(1,0), 7),
    (KnapsackState(2,0), 7),
    (KnapsackState(3,0), 13)
])
def test_bellman_equation_parameterized(state, expected):
    """
    better version
    """
    assert bellman_equation(state) == expected