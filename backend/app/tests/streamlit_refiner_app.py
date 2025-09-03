import uuid
import streamlit as st
import os
import sys
import re

from dotenv import load_dotenv
from agents.refiner_agent import refiner_graph, extract_message_content, RefinerState
from langchain_core.messages import HumanMessage

# Add the parent directory to the path so we can import from agents
sys.path.append(os.path.abspath(".."))

# Load environment variables from .env file
load_dotenv(dotenv_path="../.env")

# Page configuration
st.set_page_config(
    page_title="Prompt Refiner Agent",
    layout="wide"
)

def initialize_session_state():
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "conversation_started" not in st.session_state:
        st.session_state.conversation_started = False
    
    if "graph_state" not in st.session_state:
        st.session_state.graph_state = {}
    
    # User authentication placeholder - will be integrated with frontend auth
    if "current_user" not in st.session_state:
        st.session_state.current_user = {
            "id": "user_123",
            "name": "Demo User",
            "email": "demo@example.com"
        }
        
def main():
    st.title("Prompt Refiner Agent")
    st.markdown("**Master the art of prompt refinement with AI-powered analysis and enhancement!**")
    
    # Initializing session state
    initialize_session_state()
    
    # Sidebar for configuration
    with st.sidebar:
        
        # User info section
        st.header("User Info")
        user = st.session_state.current_user
        st.info(f"**Logged in as:** {user['name']}")
        st.caption(f"Email: {user['email']}")
        
        # Document upload section
        st.subheader("Document Upload")
        uploaded_file = st.file_uploader(
            "Upload documents for context-aware refinement",
            type=['txt', 'pdf', 'docx', 'md', 'pptx', 'xlsx'],
            help="Upload documents to enable RAG capabilities"
        )
        
        if uploaded_file is not None:
            st.success(f"{uploaded_file.name} uploaded successfully!")
        
        # Clearing conversation button
        if st.button("Clear Conversation", type="secondary"):
            if 'refiner_messages' in st.session_state:
                del st.session_state.refiner_messages
            st.rerun()
    
    # Main chat interface
    # Initializing session state
    if 'refiner_messages' not in st.session_state:
        st.session_state.refiner_messages = []
    
    # Display conversation history
    for message in st.session_state.refiner_messages:
        role, content = extract_message_content(message)
        
        if role == "user":
            with st.chat_message("user"):
                st.markdown(content)
        elif role == "assistant":
            with st.chat_message("assistant"):
                st.markdown(content)
        elif role == "system":
            with st.chat_message("assistant"):
                st.markdown(f"**System:** {content}")
    
    # Suggestions button
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("Ask for Suggestions", type="secondary", use_container_width=True):
            with st.chat_message("assistant"):
                with st.spinner("Generating suggestions..."):
                    get_refinement_suggestions("", st.session_state.thread_id)
                    st.rerun()
    
    with col3:
        if st.button("New Session", type="secondary", use_container_width=True):
            clear_conversation()
    
    # Chat input
    if prompt := st.chat_input("Enter your prompt for refinement...", key="user_input"):
        # Checking if this thread already has a refinement
        has_refinement = any(
            hasattr(msg, 'content') and ("Refined Prompt:" in msg.content or "Final Report:" in msg.content) 
            for msg in st.session_state.refiner_messages
        )
        
        # Checking if this is a follow-up question about the existing refinement
        is_follow_up = any(
            keyword in prompt.lower() for keyword in 
            ["refined", "prompt", "framework", "category", "analysis", "explain", "why", "how", "what", "help", "suggestions", "recommendations"]
        )
        
        # Checking if this is a greeting (should always be allowed)
        is_greeting = any(
            keyword in prompt.lower() for keyword in 
            ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening", "how are you", "what's up"]
        )
        
        if has_refinement and not is_follow_up and not is_greeting:
            # User is trying to refine a new prompt in the same thread
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                st.warning("""
⚠️ **New Prompt Detected**

I see you want to refine a new prompt, but this chat thread already contains a previous refinement.

**To refine a new prompt:**
1. Click "New Session" to start a fresh chat
2. Or ask me questions about your current refinement

**To continue with this refinement:**
Ask me about the framework used, analysis, or recommendations

This helps maintain clear conversation context and prevents confusion between different refinements.
                """)
        else:
            # Add user message to display
            st.session_state.refiner_messages.append(HumanMessage(content=prompt))
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Process and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Refiner Agent is analyzing..."):
                    process_refinement(prompt, st.session_state.thread_id)
                    st.rerun()

def clear_conversation():
    if 'refiner_messages' in st.session_state:
        del st.session_state.refiner_messages
    if 'thread_id' in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())
    st.success("New session started! You can now refine a new prompt.")
    st.rerun()

# Processing the user's prompt through the refiner agent
def process_refinement(user_input: str, thread_id: str):
    try:
        # Preparing input for the refiner graph
        user_message = HumanMessage(content=user_input)
        graph_input = {
            "messages": [user_message],
            "text": user_input,
            "refined_text": "",
            "prompt_category": "",
            "framework_used": "",
            "analysis": "",
            "original_prompt": user_input,
            "has_uploaded_documents": False,
            "document_context": ""
        }
        
        # Check if documents are available for RAG
        if os.path.exists("./chroma_db"):
            graph_input["has_uploaded_documents"] = True
            graph_input["document_context"] = "Document context available for enhanced refinement"
        
        # Invoke the refiner graph
        result = refiner_graph.invoke(
            graph_input,
            config={"configurable": {"thread_id": thread_id}}
        )
        
        # Extract the final message
        if result.get("messages"):
            final_message = result["messages"][-1]
            st.session_state.refiner_messages.append(final_message)
            
            # Extract and display response content
            role, content = extract_message_content(final_message)
            st.markdown(content)
            
            # Display refinement details if available
            if result.get("refined_prompt"):
                st.markdown("---")
                st.subheader("**Your Refined Prompt**")
                st.markdown(f"""
                <div style="background-color: #e8f5e8; border: 2px solid #4CAF50; border-radius: 10px; padding: 20px; margin: 15px 0;">
                    <h4>Refined Version:</h4>
                    <p style="font-size: 16px; line-height: 1.6;">{result['refined_prompt']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                message_content = final_message.content
                if "Refined Prompt:" in message_content:
                    # Extract the refined prompt from the message content
                    refined_match = re.search(r'Refined Prompt:\s*(.*?)(?=\n\n|\n$|$)', message_content, re.DOTALL)
                    if refined_match:
                        refined_prompt = refined_match.group(1).strip()
                        st.markdown("---")
                        st.subheader("**Your Refined Prompt**")
                        st.markdown(f"""
                        <div style="background-color: #e8f5e8; border: 2px solid #4CAF50; border-radius: 10px; padding: 20px; margin: 15px 0;">
                            <h4>Refined Version:</h4>
                            <p style="font-size: 16px; line-height: 1.6;">{refined_prompt}</p>
                        </div>
                        """, unsafe_allow_html=True)
            
                            # Display framework and category info
                col1, col2 = st.columns(2)
                with col1:
                    if result.get("framework_used"):
                        framework_name = result['framework_used']
                        st.info(f"**Framework Used:** {framework_name}")
                with col2:
                    if result.get("prompt_category"):
                        category_name = result['prompt_category'].title()
                        st.info(f"**Category:** {category_name}")
                    
        else:
            st.error("No response received from the refiner agent.")
            
    except Exception as e:
        st.error(f"Error processing refinement: {e}")
        
    return result if 'result' in locals() else None

# Getting suggestions for prompt refinement without full processing
def get_refinement_suggestions(user_input: str, thread_id: str):
    try:
        # Create a suggestion response
        user_name = st.session_state.current_user['name']
        
        if user_input.strip():
            # Specific suggestions for the provided input
            suggestion_content = f"""
Hi {user_name}! Here are some suggestions to improve your prompt:

**Current Prompt:** {user_input}

**Suggestions:**
1. **Be Specific**: Add concrete details about what you want to achieve
2. **Define Context**: Specify the background, audience, and constraints
3. **Set Expectations**: Clearly state the desired output format and quality
4. **Include Examples**: Provide sample inputs/outputs if possible
5. **Specify Constraints**: Mention any limitations or requirements
            """
        else:
            # General suggestions for prompt engineering
            suggestion_content = f"""
Hi {user_name}! Here are some general prompt engineering suggestions:

**Key Prompt Engineering Techniques:**

1. **Zero-Shot Prompting**: Direct instructions without examples
2. **Few-Shot Prompting**: Include 1-3 examples in your prompt
3. **Chain-of-Thought**: Ask the AI to show its reasoning step-by-step
4. **Role-Based Prompting**: Assign a specific role or persona to the AI
5. **Template-Based**: Use structured formats with placeholders

**Best Practices:**
- Be clear and specific about what you want
- Define the context and background
- Specify the desired output format
- Include examples when helpful
- Set constraints and limitations
- Use action words and clear instructions

Ready to refine a prompt? Just type it in the chat below! 
            """

        # Adding the suggestion message to chat
        suggestion_message = HumanMessage(content=suggestion_content)
        st.session_state.refiner_messages.append(suggestion_message)
        st.markdown(suggestion_content)
        
    except Exception as e:
        st.error(f"Error generating suggestions: {str(e)}")

if __name__ == "__main__":
    main()
