"""
Creating general functions to solve dynamic programs
"""

from typing import List, NamedTuple
import numpy as np


class EggDropState(NamedTuple):
    """Type of named tuple that contains number of untested floors and remaining eggs

    Args:
        NamedTuple (_type_): State space for egg drop problem
    """
    eggs: int  # number of eggs remaining
    num_untested: int  # number of untested floors
    floor_offset: int = 0  # lowest floor number in current search range


class Solution(NamedTuple):
    """Stores both the optimal value and optimal action for a state"""
    value: float  # optimal value (negative number of drops needed)
    action: int   # optimal floor to drop from (0 means no action)


def actions(state: EggDropState) -> List[int]:
    """returns a list of possible floors to drop from given our current state

    Args:
        state (EggDropState): Current state containing eggs and number of untested floors

    Returns:
        List[int]: List of floors we can drop from
    """
    if state.num_untested == 0 or state.eggs == 0:
        return []

    # If we only have one egg, we must test from lowest floor
    if state.eggs == 1:
        return [state.floor_offset + 1]  # Test next floor after offset

    # Otherwise we can choose any position in our remaining search space
    return [i + state.floor_offset + 1 for i in range(state.num_untested)]


def transition(state: EggDropState, action: int) -> tuple[EggDropState, EggDropState]:
    """takes in our current state and chosen floor to drop from and returns possible new states

    Args:
        state (EggDropState): Current state
        action (int): Position to drop from (relative to floor_offset)

    Returns:
        tuple[EggDropState, EggDropState]: (state if egg breaks, state if egg survives)
    """
    # Convert action to relative floor number
    relative_action = action - state.floor_offset

    # If egg breaks: we only need to test floors below action
    breaks_state = EggDropState(
        eggs=state.eggs - 1,
        num_untested=relative_action - 1,
        floor_offset=state.floor_offset
    )

    # If egg survives: we only need to test floors above action
    survives_state = EggDropState(
        eggs=state.eggs,
        num_untested=state.num_untested - relative_action,
        floor_offset=action  # New offset is the floor that survived
    )

    return breaks_state, survives_state


def immediate_reward(state: EggDropState, action: int) -> float:
    """gives us our immediate payoff (negative since we want to minimize drops)

    Args:
        state (EggDropState): Current state
        action (int): Position we're dropping from

    Returns:
        float: Cost of this drop
    """
    return -1  # Each drop costs 1


def bellman_equation(state: EggDropState) -> Solution:
    """solves dynamic programming for egg drop problem using bottom-up approach
    
    Args:
        state (EggDropState): Initial state with eggs and number of untested floors
        
    Returns:
        Solution: Contains both optimal value and optimal action
    """
    # Initialize cache for all possible states
    cache = {}
    
    # Fill in base cases
    for e in range(state.eggs + 1):
        for n in range(state.num_untested + 1):
            # Include floor_offset in state creation
            curr_state = EggDropState(eggs=e, num_untested=n, floor_offset=state.floor_offset)
            if n == 0:  # Found solution
                cache[curr_state] = Solution(value=0, action=0)
            elif e == 0:  # Out of eggs
                cache[curr_state] = Solution(value=float("-inf"), action=0)
    
    # Bottom-up DP
    for e in range(1, state.eggs + 1):
        for n in range(1, state.num_untested + 1):
            # Include floor_offset in state creation
            curr_state = EggDropState(eggs=e, num_untested=n, floor_offset=state.floor_offset)
            best_value = float("-inf")
            best_action = 0
            
            # Try each possible action
            for action in actions(curr_state):
                breaks_state, survives_state = transition(curr_state, action)
                
                # Create base states without offset for cache lookup
                breaks_base = EggDropState(eggs=breaks_state.eggs, 
                                        num_untested=breaks_state.num_untested,
                                        floor_offset=state.floor_offset)
                survives_base = EggDropState(eggs=survives_state.eggs,
                                          num_untested=survives_state.num_untested,
                                          floor_offset=state.floor_offset)
                
                # Get values from cache using base states
                breaks_result = cache[breaks_base].value
                survives_result = cache[survives_base].value
                
                # Calculate result for this action
                result = immediate_reward(curr_state, action) + min(breaks_result, survives_result)
                
                # Update best if this is better
                if result > best_value:
                    best_value = result
                    best_action = action
            
            cache[curr_state] = Solution(value=best_value, action=best_action)
    
    return cache[state]


def get_optimal_strategy(state: EggDropState) -> List[str]:
    """Returns the optimal strategy as a list of instructions
    
    Args:
        state (EggDropState): Initial state
        
    Returns:
        List[str]: List of instructions for optimal strategy
    """
    result = []
    curr_state = state
    step = 1
    
    while curr_state.num_untested > 0 and curr_state.eggs > 0:
        solution = bellman_equation(curr_state)
        floor = solution.action
        
        if floor == 0:  # No more actions needed
            break
            
        result.append(f"Step {step}:")
        result.append(f"- Drop egg from floor {floor}")
        
        # Calculate the two possible next states
        breaks_state, survives_state = transition(curr_state, floor)
        
        # Get the optimal value for both outcomes
        breaks_solution = bellman_equation(breaks_state)
        survives_solution = bellman_equation(survives_state)
        
        # Determine which outcome leads to the optimal solution
        if breaks_solution.value >= survives_solution.value:
            result.append(f"- If egg breaks: Continue with {breaks_state.eggs} eggs for floors 1 to {floor-1}")
            curr_state = breaks_state
        else:
            result.append(f"- If egg survives: Continue with {survives_state.eggs} eggs for floors {floor+1} to {curr_state.num_untested}")
            curr_state = survives_state
            
        result.append("---")
        step += 1
        
    return result
