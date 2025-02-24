import streamlit as st
from src.bellman_equation import EggDropState, bellman_equation, get_optimal_strategy
import graphviz  # Add this to your imports at the top

def reset_session_state():
    # Clear all session state variables
    if 'history' in st.session_state:
        del st.session_state.history
    if 'current_state' in st.session_state:
        del st.session_state.current_state
    if 'found_solution' in st.session_state:
        del st.session_state.found_solution
    if 'started' in st.session_state:
        del st.session_state.started

def handle_decision(breaks: bool, optimal_floor: int):
    current_state = st.session_state.current_state
    
    # Record the decision in history
    st.session_state.history.append({
        'floor': optimal_floor,
        'breaks': breaks,
        'eggs_left': current_state.eggs,
        'floors_untested': current_state.num_untested
    })
    
    # Update the current state based on the decision
    if breaks:
        # Egg broke, search lower floors with one less egg
        st.session_state.current_state = EggDropState(
            eggs=current_state.eggs - 1,
            num_untested=optimal_floor - current_state.floor_offset - 1,
            floor_offset=current_state.floor_offset
        )
    else:
        # Egg survived, search higher floors with same number of eggs
        st.session_state.current_state = EggDropState(
            eggs=current_state.eggs,
            num_untested=current_state.num_untested - (optimal_floor - current_state.floor_offset),
            floor_offset=optimal_floor  # New offset is the floor that survived
        )

def initialize_session(initial_state):
    # Initialize all session state variables if they don't exist
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'current_state' not in st.session_state:
        st.session_state.current_state = initial_state
    if 'found_solution' not in st.session_state:
        st.session_state.found_solution = False
    if 'started' not in st.session_state:
        st.session_state.started = False

def create_decision_path_visualization(history):
    """Creates a graphviz visualization of the user's decision path"""
    graph = graphviz.Digraph()
    graph.attr(rankdir='LR', splines='ortho', nodesep='0.5', ranksep='0.5')
    
    # Start node (rounded rectangle)
    total_floors = history[0]['floors_untested']
    total_eggs = history[0]['eggs_left']
    graph.node('start', f'Start\nEggs: {total_eggs}\nFloors: {total_floors}', 
               shape='box', style='rounded,filled', fillcolor='lightblue')
    
    # Create nodes for each decision
    prev_node = 'start'
    for i, decision in enumerate(history):
        # Decision node (diamond)
        decision_id = f'decision_{i}'
        label = f'Drop at\nfloor {decision["floor"]}'
        graph.node(decision_id, label, 
                  shape='diamond', 
                  style='filled', 
                  fillcolor='white')
        
        # Edge to decision
        graph.edge(prev_node, decision_id, color='blue', penwidth='2')
        
        # Calculate remaining eggs and floors for outcome
        remaining_eggs = decision["eggs_left"] - (1 if decision["breaks"] else 0)
        remaining_floors = decision["floors_untested"] - decision["floor"] if not decision["breaks"] else decision["floor"] - 1
        
        # Format state label with line breaks
        state_text = [
            "BREAKS" if decision["breaks"] else "SURVIVES",
            f"Eggs: {remaining_eggs}",
            f"Floors: {remaining_floors}"
        ]
        
        # Create outcome node ID
        state_id = f'state_{i}'
        
        # Create state node with custom HTML-like label
        if decision["breaks"]:
            # For break nodes
            html_label = f'''<<table border="0" cellborder="1" cellspacing="0" cellpadding="8" bgcolor="lightpink">
                              <tr><td align="center"><font point-size="12">{state_text[0]}</font></td></tr>
                              <tr><td align="center"><font point-size="10">{state_text[1]}</font></td></tr>
                              <tr><td align="center"><font point-size="10">{state_text[2]}</font></td></tr>
                            </table>>'''
        else:
            # For survive nodes
            html_label = f'''<<table border="0" cellborder="1" cellspacing="0" cellpadding="8" bgcolor="#90EE90">
                              <tr><td align="center"><font point-size="12">{state_text[0]}</font></td></tr>
                              <tr><td align="center"><font point-size="10">{state_text[1]}</font></td></tr>
                              <tr><td align="center"><font point-size="10">{state_text[2]}</font></td></tr>
                            </table>>'''
        
        graph.node(state_id, 
                  shape='none',
                  margin='0',
                  label=html_label)
        
        # Edge to state
        edge_color = 'red' if decision["breaks"] else 'green'
        graph.edge(decision_id, state_id, color=edge_color, penwidth='2')
        
        prev_node = state_id
    
    return graph

def main():
    st.title("Egg Drop Problem Solver")
    st.write("""
    This app helps solve the classic egg drop problem using dynamic programming.
    Given n eggs and k floors, find the minimum number of drops needed to determine
    the critical floor (where eggs start breaking).
    """)

    # Create a container for the input parameters
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            num_eggs = st.number_input("Number of Eggs", min_value=1, max_value=10, value=2)
        with col2:
            num_floors = st.number_input("Number of Floors", min_value=1, max_value=100, value=10)

        # Reset and Start buttons in the same row
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Reset"):
                reset_session_state()
                st.experimental_rerun()
        with col2:
            if st.button("Start Solving"):
                st.session_state.started = True
                initial_state = EggDropState(eggs=num_eggs, num_untested=num_floors)
                initialize_session(initial_state)
                st.experimental_rerun()

    # Continue solving if we've started
    if 'started' in st.session_state and st.session_state.started:
        # Create a container for the game state
        with st.container():
            current_state = st.session_state.current_state
            
            # Display history of decisions in an expander
            if st.session_state.history:
                with st.expander("History of Drops", expanded=True):
                    for i, decision in enumerate(st.session_state.history, 1):
                        outcome = "broke" if decision['breaks'] else "survived"
                        st.write(f"{i}. Dropped from floor {decision['floor']}: Egg {outcome}")
                        st.write(f"   (Eggs left: {decision['eggs_left']}, Floors to test: {decision['floors_untested']})")
            
            # Check if we've found the solution
            if current_state.eggs == 0:
                st.error("No more eggs left! The critical floor must be below the last test.")
                st.session_state.found_solution = True
            elif current_state.num_untested <= 1:
                st.success(f"Found the critical floor! It's floor {current_state.num_untested}")
                st.session_state.found_solution = True
            
            # If we haven't found the solution yet, show the next decision
            if not st.session_state.found_solution:
                st.write("### Next Decision")
                st.write(f"Current state: {current_state.eggs} eggs, {current_state.num_untested} floors to test")
                solution = bellman_equation(current_state)
                optimal_floor = solution.action
                st.write(f"Drop an egg from floor {optimal_floor}")
                
                # Buttons for decisions
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Egg Breaks"):
                        handle_decision(True, optimal_floor)
                        st.experimental_rerun()
                with col2:
                    if st.button("Egg Survives"):
                        handle_decision(False, optimal_floor)
                        st.experimental_rerun()

    # After solution is found and history exists, show visualization
    if ('found_solution' in st.session_state 
            and st.session_state.found_solution 
            and 'history' in st.session_state 
            and st.session_state.history):
        
        # Create a container for the visualization
        with st.container():
            st.write("### Your Decision Path")
            st.write("Here's the path you took to find the solution:")
            
            # Create and display the graph in a fixed-size container
            try:
                graph = create_decision_path_visualization(st.session_state.history)
                # Set a fixed height for the visualization
                st.graphviz_chart(graph, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating visualization: {str(e)}")
            
            # Add explanation of the visualization
            with st.expander("Visualization Guide"):
                st.write("""
                - Blue arrows show your progression through the problem
                - Green arrows indicate when the egg survived
                - Red arrows indicate when the egg broke
                - Each node shows the state of the problem at that point
                """)
            
            # Start new problem button
            if st.button("Start New Problem"):
                reset_session_state()
                st.experimental_rerun()

if __name__ == "__main__":
    main()
