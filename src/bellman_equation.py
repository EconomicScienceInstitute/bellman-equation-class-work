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
        return [1]  # Always test the next floor

    # Otherwise we can choose any position in our remaining search space
    return list(range(1, state.num_untested + 1))


def transition(state: EggDropState, action: int) -> tuple[EggDropState, EggDropState]:
    """takes in our current state and chosen floor to drop from and returns possible new states

    Args:
        state (EggDropState): Current state
        action (int): Position to drop from (1 to num_untested)

    Returns:
        tuple[EggDropState, EggDropState]: (state if egg breaks, state if egg survives)
    """
    # If egg breaks: we only need to test floors below action
    breaks_state = EggDropState(eggs=state.eggs - 1, num_untested=action - 1)

    # If egg survives: we only need to test floors above action
    survives_state = EggDropState(
        eggs=state.eggs, num_untested=state.num_untested - action
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
            curr_state = EggDropState(eggs=e, num_untested=n)
            if n == 0:  # Found solution
                cache[curr_state] = Solution(value=0, action=0)
            elif e == 0:  # Out of eggs
                cache[curr_state] = Solution(value=float("-inf"), action=0)
    
    # Bottom-up DP
    for e in range(1, state.eggs + 1):
        for n in range(1, state.num_untested + 1):
            curr_state = EggDropState(eggs=e, num_untested=n)
            best_value = float("-inf")
            best_action = 0
            
            # Try each possible action
            for action in actions(curr_state):
                breaks_state, survives_state = transition(curr_state, action)
                
                # Get values from cache
                breaks_result = cache[breaks_state].value
                survives_result = cache[survives_state].value
                
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


def visualize_solution(state: EggDropState) -> None:
    """Creates a visualization of the egg drop solution process

    Args:
        state (EggDropState): Initial state
    """
    import matplotlib.pyplot as plt

    # Get the optimal strategy
    strategy = get_optimal_strategy(state)

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Draw building outline
    building_height = state.num_untested
    ax.plot([0, 0], [0, building_height], 'k-', linewidth=2)  # Left wall
    ax.plot([1, 1], [0, building_height], 'k-', linewidth=2)  # Right wall

    # Draw floors as horizontal lines
    for i in range(building_height + 1):
        ax.plot([0, 1], [i, i], 'k-', alpha=0.2)

    # Parse strategy and plot drops
    curr_floor = 0
    colors = ['red', 'blue', 'green', 'orange', 'purple']  # Colors for different eggs
    egg_num = 0

    for line in strategy:
        if line.startswith("- Drop egg from floor"):
            floor = int(line.split()[-1])
            # Plot drop point
            ax.scatter(0.5, floor, color=colors[egg_num % len(colors)],
                       s=100, label=f'Drop {curr_floor + 1}')
            curr_floor += 1

    # Customize plot
    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(0, building_height + 1)
    ax.set_title(f'Egg Drop Solution\n{state.eggs} eggs, {state.num_untested} floors')
    ax.set_xticks([])
    ax.set_ylabel('Floor Number')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.show()

    # Print strategy
    print("\nOptimal Strategy:")
    for line in strategy:
        print(line)

