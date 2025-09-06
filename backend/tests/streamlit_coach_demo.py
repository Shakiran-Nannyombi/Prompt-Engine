import sys
import os
from dotenv import load_dotenv
import streamlit as st
import uuid
from langchain_core.messages import HumanMessage

# Adding path of files imported
sys.path.append(os.path.abspath(".."))

# Load environment variables from .env file
load_dotenv(dotenv_path="../.env")

from agents.coach_agent import coach_graph, extract_message_content, CoachingState

def initialize_session_state():
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "conversation_started" not in st.session_state:
        st.session_state.conversation_started = False
    
    if "graph_state" not in st.session_state:
        st.session_state.graph_state = {}

def start_conversation():
    if not st.session_state.conversation_started:
        config = {"configurable": {"thread_id": st.session_state.thread_id}}
        try:
            # Start the conversation by invoking the graph without user input
            initial_state = coach_graph.invoke({}, config)
            st.session_state.graph_state = initial_state
            
            # Add the welcome message to display
            if 'messages' in initial_state and initial_state['messages']:
                ai_message = initial_state['messages'][-1]
                role, content = extract_message_content(ai_message)
                st.session_state.messages.append({"role": role, "content": content})
            
            st.session_state.conversation_started = True
            
        except Exception as e:
            st.error(f"Could not connect to the coaching agent. Please check your configuration. Error: {e}")
            st.stop()

def process_user_input(user_input: str):
    config = {"configurable": {"thread_id": st.session_state.thread_id}}
    
    try:
        # Add user message to the graph
        graph_input = {"messages": [HumanMessage(content=user_input)]}
        
        # Invoke the graph with user input
        updated_state = coach_graph.invoke(graph_input, config)
        
        # Update session state
        st.session_state.graph_state = updated_state
        
        # Extract and return the latest AI message
        if 'messages' in updated_state and updated_state['messages']:
            # Find the last AI message
            ai_messages = [msg for msg in updated_state['messages'] 
                          if extract_message_content(msg)[0] == "assistant"]
            if ai_messages:
                _, content = extract_message_content(ai_messages[-1])
                return content
        
        return "I apologize, but I couldn't process your input. Please try again."
        
    except Exception as e:
        st.error(f"Error processing your input: {e}")
        return "There was an error processing your request. Please try again."

# Extracting progress information from current state
def get_progress_info():
    current_state = st.session_state.get("graph_state", {})
    
    task = current_state.get("task", "")
    context = current_state.get("context", "")
    references = current_state.get("references", [])
    final_prompt = current_state.get("final_prompt", "")
    current_step = current_state.get("current_step", "initializing")
    
    # Calculate progress
    steps_completed = 0
    if task: steps_completed += 1
    if context: steps_completed += 1 
    if references: steps_completed += 1
    if final_prompt: steps_completed += 1
    
    total_steps = 4
    progress_percentage = (steps_completed / total_steps) * 100
    
    return {
        "task": task,
        "context": context, 
        "references": references,
        "final_prompt": final_prompt,
        "current_step": current_step,
        "steps_completed": steps_completed,
        "total_steps": total_steps,
        "progress_percentage": progress_percentage
    }

def main():
    st.set_page_config(
        page_title="Prompt Engineering Coach",
        layout="wide"
    )

    st.title("Prompt Engineering Coach")
    st.markdown("*Master the art of prompt engineering with guided assistance!*")
    
    # Initialize session state
    initialize_session_state()
    
    # Start conversation if not started
    start_conversation()
    
    # Sidebar for Progress Tracking
    with st.sidebar:
        st.markdown("## Progress Tracker")
        
        progress_info = get_progress_info()
        
        # Display current step
        step_display = progress_info["current_step"].replace("_", " ").title()
        st.markdown(f"**Current Step:** `{step_display}`")
        
        # Progress bar
        st.progress(progress_info["progress_percentage"] / 100)
        st.markdown(f"Progress: {progress_info['steps_completed']}/{progress_info['total_steps']} steps completed")
        
        # Details of each step
        with st.expander("View Captured Details", expanded=False):
            task_preview = progress_info['task'][:50] + '...' if progress_info['task'] and len(progress_info['task']) > 50 else progress_info['task'] or 'Not provided yet'
            context_preview = progress_info['context'][:50] + '...' if progress_info['context'] and len(progress_info['context']) > 50 else progress_info['context'] or 'Not provided yet'
            
            st.markdown(f"**Task:** {task_preview}")
            st.markdown(f"**Context:** {context_preview}")
            st.markdown(f"**References:** {'Provided' if progress_info['references'] else 'Not provided yet'}")
            st.markdown(f"**Final Prompt:** {'Created' if progress_info['final_prompt'] else 'Not created yet'}")
        
        st.markdown("---")
        
        # Reset button
        if st.button("Reset Conversation", use_container_width=True):
            # Clear all session state
            keys_to_clear = list(st.session_state.keys())
            for key in keys_to_clear:
                del st.session_state[key]
            st.rerun()
        
        # Completion celebration and download
        if progress_info["current_step"] == "completed":
            st.balloons()
            st.success("🎉 Congratulations! Your prompt is ready.")
            
            if progress_info["final_prompt"]:
                st.download_button(
                    label="Download Final Prompt",
                    data=progress_info["final_prompt"],
                    file_name="engineered_prompt.txt",
                    mime="text/plain",
                    use_container_width=True
                )

    # Main Chat Interface
    st.markdown("## Coaching Session")
    
    # Display conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your response here...", key="user_input"):
        # Add user message to display
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Process and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Coach is thinking..."):
                response_content = process_user_input(prompt)
                st.markdown(response_content)
                # Add AI response to history
                st.session_state.messages.append({"role": "assistant", "content": response_content})
        
        # Rerun to update the sidebar with new state
        st.rerun()

    # Help section at the bottom
    with st.expander(" Need Help?", expanded=False):
        st.markdown("""
        **How to use the Prompt Engineering Coach:**
        
        1. **Task**: Describe what you want to accomplish
        2. **Context**: Provide background information and requirements  
        3. **References**: Share any resources or examples
        4. **Final Prompt**: Create your complete engineered prompt
        
        **Tips:**
        - Be specific about your needs
        - Provide concrete examples when possible
        - Don't worry if you're not sure - the coach will guide you!
        - You can say "suggest some tasks" if you need ideas
        
        **Examples of good tasks:**
        - "Create a customer service chatbot"
        - "Write a lesson plan for teaching fractions"
        - "Generate code for a todo app"
        - "Draft a professional email template"
        """)

if __name__ == "__main__":
    main()