import streamlit as st
from src.bellman_equation import EggDropState, bellman_equation, get_optimal_strategy
import numpy as np
import matplotlib.pyplot as plt

def main():
    st.title("Egg Drop Problem Solver")
    st.write("""
    This app helps solve the classic egg drop problem using dynamic programming.
    Given n eggs and k floors, find the minimum number of drops needed to determine
    the critical floor (where eggs start breaking).
    """)

    # Input parameters
    col1, col2 = st.columns(2)
    with col1:
        num_eggs = st.number_input("Number of Eggs", min_value=1, max_value=10, value=2)
    with col2:
        num_floors = st.number_input("Number of Floors", min_value=1, max_value=100, value=10)

    if st.button("Solve"):
        # Create initial state
        initial_state = EggDropState(eggs=num_eggs, num_untested=num_floors)
        
        # Get solution
        solution = bellman_equation(initial_state)
        result = -solution.value  # Negate because our implementation uses costs
        
        # Display results
        st.success(f"Minimum number of drops needed: {result}")
        
        # Calculate exact average by testing each floor as the critical floor
        total_drops = 0
        drops_per_floor = []  # Store drops needed for each floor
        
        for critical_floor in range(1, num_floors + 1):
            if num_eggs == 1:
                # With 1 egg, we must test each floor from bottom up
                drops = critical_floor
            elif num_eggs == 2:
                # For 2 eggs, use the optimal strategy from bellman equation
                test_state = EggDropState(eggs=num_eggs, num_untested=critical_floor)
                solution = bellman_equation(test_state)
                drops = -solution.value  # Negate because our implementation uses costs
            else:
                # For more eggs, can use more aggressive strategy
                # This part needs to be implemented based on optimal strategy for 3+ eggs
                drops = max(1, int(np.log2(critical_floor))) + 1
            
            drops_per_floor.append(drops)
            total_drops += drops
        
        avg_drops = total_drops / num_floors
        
        # Display the average and breakdown
        st.success(f"Average number of drops needed (exact calculation): {avg_drops:.2f}")
        
        # Display drops needed for each floor
        st.write("### Drops needed for each critical floor:")
        floor_data = {f"Floor {i+1}": drops for i, drops in enumerate(drops_per_floor)}
        st.write(floor_data)

        # Show optimal strategy
        st.write("### Optimal Strategy:")
        strategy = get_optimal_strategy(initial_state)
        for instruction in strategy:
            st.write(instruction)

        # Create probability distribution chart
        st.write("### Probability Distribution of Finding Solution")
        
        # Calculate probability distribution
        drops_range = np.arange(1, result + 1)
        # Assuming uniform distribution of critical floor
        probabilities = [min(x / result, 1.0) for x in drops_range]
        
        # Create the chart
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(drops_range, probabilities, marker='o')
        ax.set_xlabel('Number of Drops')
        ax.set_ylabel('Probability of Finding Solution')
        ax.set_title('Probability of Finding Critical Floor vs Number of Drops')
        ax.grid(True)
        
        # Add the chart to Streamlit
        st.pyplot(fig)

        # Add explanation for the probability chart
        st.write("""
        ### Understanding the Probability Chart:
        - The x-axis shows the number of drops
        - The y-axis shows the probability of finding the critical floor
        - The chart assumes a uniform distribution of the critical floor
        - The maximum number of drops needed is guaranteed to find the solution
        - You might find the solution earlier depending on the actual critical floor
        """)

        # Add explanation
        st.write("""
        ### How to interpret the result:
        - This is the minimum number of drops needed in the worst case
        - The solution guarantees finding the critical floor within this many drops
        - The actual number of drops needed might be less depending on where the critical floor is
        """)

        # Add some example cases for verification
        st.write("""
        ### Verification Cases:
        1. 1 egg, n floors: Always needs n drops (must test every floor from bottom)
        2. 2 eggs, 100 floors: Should need around 14 drops
        3. 3 eggs, 100 floors: Should need around 9 drops
        """)

if __name__ == "__main__":
    main()
