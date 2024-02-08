"""
writes one test per function of bellman equation
"""
from bellman_equation import knapsackState, actions, transition, immediate_reward, bellman_equation

def test_actions():
    """
    funcitonal test for the actions function
    """
    test_state = knapsackState(0,0)
    assert actions(test_state) == [0,1]

def test_transition():
    assert True