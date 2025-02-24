from src.bellman_equation import EggDropState, bellman_equation, get_optimal_strategy, transition 
import streamlit as st
import graphviz

def get_complete_strategy(state: EggDropState) -> list[str]:
    """Returns a complete strategy showing all possible outcomes at each step"""
    def recursive_strategy(curr_state: EggDropState, path: str, step: int) -> list[str]:
        if curr_state.num_untested == 0 or curr_state.eggs == 0:
            return []

        solution = bellman_equation(curr_state)
        floor = solution.action
        
        if floor == 0:
            return []

        # Calculate the two possible next states
        breaks_state, survives_state = transition(curr_state, floor)
        
        result = []
        result.append(f"Step {step} {path}:")
        result.append(f"- Drop egg from floor {floor}")
        
        # Recursively get strategies for both outcomes
        breaks_path = f"{path} → [Breaks at {floor}]"
        survives_path = f"{path} → [Survives {floor}]"
        
        result.extend(recursive_strategy(breaks_state, breaks_path, step + 1))
        result.extend(recursive_strategy(survives_state, survives_path, step + 1))
        
        return result

    return recursive_strategy(state, "", 1)

def reset_session_state():
    """Reset all session state variables"""
    st.session_state.current_state = None
    st.session_state.step_number = 1
    st.session_state.path_history = []
    st.session_state.floor_offset = 0
    st.session_state.decisions = []  # Track decisions for visualization

def create_decision_tree():
    """Creates a graphviz visualization of the decision path taken"""
    graph = graphviz.Digraph()
    graph.attr(rankdir='TB')
    
    # Add start node
    graph.node('start', 'Start', shape='oval')
    
    prev_node = 'start'
    for i, decision in enumerate(st.session_state.decisions):
        # Create unique node IDs
        node_id = f'step_{i+1}'
        
        # Create node label
        floor_num = decision['floor']
        outcome = decision['outcome']
        label = f'Floor {floor_num}\n{outcome}'
        
        # Add node and edge
        graph.node(node_id, label, shape='box')
        graph.edge(prev_node, node_id)
        
        prev_node = node_id
    
    return graph

def main():
    st.title("Egg Drop Problem Solver")
    st.write("""
    This app helps solve the classic egg drop problem using dynamic programming.
    Given n eggs and k floors, find the minimum number of drops needed to determine
    the critical floor (where eggs start breaking).
    """)

    # Create three columns: two for inputs, one for start over button
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        num_eggs = st.number_input("Number of Eggs", min_value=1, max_value=10, value=2)
    with col2:
        num_floors = st.number_input("Number of Floors", min_value=1, max_value=100, value=10)
    with col3:
        if st.button("Start Over", key="constant_start_over"):
            reset_session_state()
            st.rerun()

    # Initialize session state variables if they don't exist
    if 'current_state' not in st.session_state:
        st.session_state.current_state = None
    if 'step_number' not in st.session_state:
        st.session_state.step_number = 1
    if 'path_history' not in st.session_state:
        st.session_state.path_history = []
    if 'floor_offset' not in st.session_state:
        st.session_state.floor_offset = 0
    if 'decisions' not in st.session_state:
        st.session_state.decisions = []

    if st.button("Solve"):
        # Create initial state
        initial_state = EggDropState(eggs=num_eggs, num_untested=num_floors)
        
        # Get solution
        solution = bellman_equation(initial_state)
        result = -solution.value  # Negate because our implementation uses costs
        
        # Display results
        st.success(f"Minimum number of drops needed: {result}")
        
        # Initialize session state for interactive strategy
        reset_session_state()
        st.session_state.current_state = initial_state
        st.rerun()

    # Show interactive strategy if we have a valid current state
    if st.session_state.current_state is not None:
        st.write("### Interactive Strategy:")
        st.write("Follow the steps and click the appropriate button based on what happens to the egg.")
        
        current_state = st.session_state.current_state
        
        # Show path history
        if st.session_state.path_history:
            st.write("#### Previous steps:")
            for step in st.session_state.path_history:
                st.write(step)
        
        # If we still have floors to test and eggs to use
        if current_state.num_untested > 0 and current_state.eggs > 0:
            solution = bellman_equation(current_state)
            relative_floor = solution.action
            absolute_floor = relative_floor + st.session_state.floor_offset
            
            if relative_floor > 0:
                st.write(f"#### Step {st.session_state.step_number}:")
                st.write(f"Drop egg from floor {absolute_floor}")
                
                st.write("#### What happened to the egg?")
                col1, col2 = st.columns(2)
                
                # Calculate next states
                breaks_state, survives_state = transition(current_state, relative_floor)
                
                with col1:
                    if st.button("Broken"):
                        st.session_state.decisions.append({
                            'floor': absolute_floor,
                            'outcome': 'Broke'
                        })
                        st.session_state.path_history.append(
                            f"Step {st.session_state.step_number}: Dropped at floor {absolute_floor} - Egg broke"
                        )
                        st.session_state.current_state = breaks_state
                        st.session_state.step_number += 1
                        st.rerun()
                
                with col2:
                    if st.button("Not Broken"):
                        st.session_state.decisions.append({
                            'floor': absolute_floor,
                            'outcome': 'Survived'
                        })
                        st.session_state.path_history.append(
                            f"Step {st.session_state.step_number}: Dropped at floor {absolute_floor} - Egg survived"
                        )
                        st.session_state.current_state = survives_state
                        st.session_state.floor_offset = absolute_floor
                        st.session_state.step_number += 1
                        st.rerun()
            else:
                st.write("Strategy complete!")
        else:
            if current_state.eggs == 0:
                st.write("No more eggs left! The critical floor has been found.")
            else:
                st.write("All floors have been tested! The critical floor has been found.")
            
            # Show decision tree visualization
            if st.session_state.decisions:
                st.write("### Your Decision Path:")
                graph = create_decision_tree()
                st.graphviz_chart(graph)

        # Add explanation
        st.write("""
        ### How to interpret the result:
        - Follow the steps one by one
        - After each drop, click the appropriate button based on whether the egg broke or survived
        - The strategy will adapt based on your choices
        - Continue until you find the critical floor
        - Use the Start Over button at any time to begin a new problem
        """)

if __name__ == "__main__":
    main()