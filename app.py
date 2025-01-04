import streamlit as st
from typing import Dict, TypedDict
from agent import *
from BZRA import bzra_tasks
from AHG import ahg_tasks
from AP import ap_tasks
from CHEI import chei_tasks
from PPI import ppi_tasks

def initialize_session_state():
    if 'state' not in st.session_state:
        st.session_state.state = initial_state
        st.session_state.state['tasks'] = {'BZRA': bzra_tasks, 'AHG': ahg_tasks, 'AP': ap_tasks, 'CHEI': chei_tasks, 'PPI': ppi_tasks}
    if 'conversation_ended' not in st.session_state:
        st.session_state.conversation_ended = False

def reset_conversation():
    st.session_state.state = initial_state
    st.session_state.conversation_ended = False

def main():
    st.title("Infohealth Agent Demo")
    
    # Initialize session state
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
    for msg in st.session_state.state['messages'][1:]:  # Skip system message
        if msg['role'] == 'assistant':
            st.write("🤖 Assistant: " + msg['content'])
        else:
            st.write("👤 User: " + msg['content'])
    

    
    
    # User input section
    if not st.session_state.conversation_ended:
        user_input = st.text_input("Your message:")
        
        if st.button("Send") and user_input:
            # Append user message before processing
            process_user_input(user_input, st.session_state.state)
            
            
            # Rerun to update the display
            st.rerun()
        if st.button("Reset Conversation"):
            st.session_state.state = AgentState(
                messages=[{"role":"system", "content":""},
                        {"role":"assistant", "content": "Hello! To assist you today, could you please tell me what medication you're taking?"}],  # Sequence of BaseMessage objects
                user_data={},
                curr_node=medication_task,
                tasks = {'BZRA': bzra_tasks, 'AHG': ahg_tasks, 'AP': ap_tasks, 'CHEI': chei_tasks, 'PPI': ppi_tasks},
                total_tokens=0
            )
            st.rerun()
    else:
        st.success("Conversation completed!")
        if st.button("Start New Conversation"):
            reset_conversation()
            st.rerun()

if __name__ == "__main__":
    main()