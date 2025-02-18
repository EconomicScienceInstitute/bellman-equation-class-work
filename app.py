import streamlit as st
from src.bellman_equation import EggDropState, bellman_equation, get_optimal_strategy

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
        
        # Show optimal strategy
        st.write("### Optimal Strategy:")
        strategy = get_optimal_strategy(initial_state)
        for instruction in strategy:
            st.write(instruction)

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
