"""
Tests for the egg drop dynamic programming solution
"""
import pytest
from bellman_equation import EggDropState, actions, transition, immediate_reward, bellman_equation
from tests.utils import measure_performance

def test_actions():
    """Test actions function for various states"""
    # Edge cases - 0 floors or 0 eggs should return empty list
    assert actions(EggDropState(eggs=1, num_untested=0)) == []
    assert actions(EggDropState(eggs=0, num_untested=5)) == []
    
    # With 1 egg, can only test from first floor
    assert actions(EggDropState(eggs=1, num_untested=5)) == [1]
    
    # With multiple eggs, can test from any floor up to num_untested
    assert actions(EggDropState(eggs=2, num_untested=3)) == [1, 2, 3]

def test_transition():
    """Test transition function returns correct next states"""
    state = EggDropState(eggs=2, num_untested=5)
    breaks, survives = transition(state, 2)
    
    # If egg breaks at floor 2, we have 1 egg and need to check 1 floor below
    assert breaks == EggDropState(eggs=1, num_untested=1)
    # If egg survives at floor 2, we have 2 eggs and need to check 3 floors above
    assert survives == EggDropState(eggs=2, num_untested=3)

def test_immediate_reward():
    """Test immediate reward is always -1 per drop"""
    state = EggDropState(eggs=2, num_untested=5)
    assert immediate_reward(state, 1) == -1
    assert immediate_reward(state, 5) == -1

def test_bellman_equation_edge_cases():
    """Test bellman equation for edge cases we can compute by hand"""
    # 0 floors - should return 0 drops needed
    assert bellman_equation(EggDropState(eggs=1, num_untested=0)) == 0
    assert bellman_equation(EggDropState(eggs=2, num_untested=0)) == 0
    assert bellman_equation(EggDropState(eggs=100, num_untested=0)) == 0
    
    # 1 floor - should always take 1 drop
    assert bellman_equation(EggDropState(eggs=1, num_untested=1)) == -1
    assert bellman_equation(EggDropState(eggs=2, num_untested=1)) == -1
    assert bellman_equation(EggDropState(eggs=100, num_untested=1)) == -1

@measure_performance
def test_bellman_equation_10_floors():
    """Test bellman equation for 10 floors with different numbers of eggs"""
    # With 1 egg: must test each floor from bottom up = 10 drops worst case
    assert bellman_equation(EggDropState(eggs=1, num_untested=10)) == -10
    
    # With 2 eggs: optimal solution is 4 drops worst case
    assert bellman_equation(EggDropState(eggs=2, num_untested=10)) == -4
    
    # With 3 eggs: optimal solution is 4 drops worst case
    assert bellman_equation(EggDropState(eggs=3, num_untested=10)) == -4

@measure_performance
def test_bellman_equation_classic_case():
    """Test the classic case of 2 eggs and 36 floors"""
    # The optimal solution for 2 eggs and 36 floors is 8 drops
    assert bellman_equation(EggDropState(eggs=2, num_untested=36)) == -8

@measure_performance
@pytest.mark.parametrize("eggs,floors,expected_drops", [
    (1, 0, 0),    # Edge case: no floors
    (1, 1, -1),   # One floor
    (2, 10, -4),  # Classic small case
    (2, 36, -8),  # Classic puzzle case
])
def test_bellman_equation_parameterized(eggs, floors, expected_drops):
    """Parameterized tests for various cases"""
    state = EggDropState(eggs=eggs, num_untested=floors)
    assert bellman_equation(state) == expected_drops

# Add a specific performance test for larger inputs
@measure_performance
def test_bellman_equation_performance():
    """Test performance with larger inputs"""
    # Test with 3 eggs and 100 floors
    state = EggDropState(eggs=3, num_untested=100)
    result = bellman_equation(state)
    assert isinstance(result, float)  # Just verify we get a result