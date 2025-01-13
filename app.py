import streamlit as st
from agent import *
from BZRA import bzra_tasks
from AHG import ahg_tasks
from AP import ap_tasks
from CHEI import chei_tasks
from PPI import ppi_tasks
from agent_logger import *
from datetime import datetime


def initialize_session_state():
    st.session_state.state = AgentState(
            messages=[{"role":"system", "content":""},
                    {"role":"assistant", "content": "Hello! To assist you today, could you please tell me what medication you're taking?"}],  # Sequence of BaseMessage objects
            user_data={},
            curr_node=medication_task,
            tasks = {'BZRA': bzra_tasks, 'AHG': ahg_tasks, 'AP': ap_tasks, 'CHEI': chei_tasks, 'PPI': ppi_tasks},
            total_tokens=0
        )
    st.session_state.logger = AgentLogger(datetime.now().isoformat()[:-7])


def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    
    return st.session_state["password_correct"]


def main():
    if not check_password():
        st.stop()  # Do not continue if check_password is not True
        
    st.title("Infohealth Agent Demo")
    
    # Initialize session state
    if 'state' not in st.session_state:
        initialize_session_state()
    
    st.subheader("Agent State")

    st.write("Current token usage:")
    st.metric("Current token usage", st.session_state.state['total_tokens'])

    st.write("Current Task:")
    st.info(st.session_state.state['curr_node']['desc'])
    
    st.write("Collected User Data:")
    st.json(st.session_state.state['user_data'])

    if st.session_state.state['curr_node'].get('acceptable'):
        st.write("Acceptable Answers:")
        st.json(st.session_state.state['curr_node']['acceptable'])

    st.subheader("Conversation")
    # Display conversation history
    for idx, msg in enumerate(st.session_state.state['messages'][1:], 1):
        if msg['role'] == 'assistant':
            if idx > 1:  # Skip the first assistant message
                col1, col2 = st.columns([0.9, 0.1])
                with col1:
                    st.write("🤖 Assistant: " + msg['content'])
                with col2:
                    if st.button("🚩", key=f"flag_{idx}"):
                        st.session_state.logger.log_flag(st.session_state.state['messages'], idx)
            else:
                # Just display the first assistant message without a flag button
                st.write("🤖 Assistant: " + msg['content'])
        else:
            st.write("👤 User: " + msg['content'])
        

    
    
    # User input section
    user_input = st.text_input("Your message:")
    
    if st.button("Send") and user_input:
        # Process user input
        process_user_input(user_input, st.session_state.state, st.session_state.logger)
        # Rerun to update the display
        st.rerun()
    if st.button("Reset Conversation"):
        initialize_session_state()
        st.rerun()


if __name__ == "__main__":
    main()