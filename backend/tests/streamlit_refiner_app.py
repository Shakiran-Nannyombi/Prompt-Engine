import uuid
import streamlit as st
import os
import sys
from pathlib import Path
import pdfplumber

sys.path.append(os.path.abspath(".."))

from dotenv import load_dotenv
from agents.refiner_agent import refiner_graph, extract_message_content
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv(dotenv_path="../.env")

# Page Config
st.set_page_config(page_title="Prompt Refiner Agent", layout="wide")

# Session State
def initialize_session_state():
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())
    if "messages" not in st.session_state:
        st.session_state.messages = []
    # This flag will track the name of the file we've processed
    if "processed_filename" not in st.session_state:
        st.session_state.processed_filename = None

# Backend Functions

def process_refinement(user_input: str, thread_id: str):
    """Processing user input through the refiner agent."""
    try:
        graph_input = {"messages": [HumanMessage(content=user_input)]}
        config = {"configurable": {"thread_id": thread_id}}
        result = refiner_graph.invoke(graph_input, config)
        return result["messages"][-1]
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return AIMessage(content=f"Sorry, an error occurred during processing: {e}")

def process_uploaded_document(uploaded_file):
    """Extracting text and storing it for the agent to reference."""
    try:
        text_content = extract_text_from_uploaded_file(uploaded_file)
        if text_content and len(text_content.strip()) > 10:
            # Process the document through the refiner agent's file processor
            from agents.tools.refinement_tools import process_uploaded_file
            
            # Call the file processor tool to store in vector database
            result = process_uploaded_file(text_content, uploaded_file.name)
            
            # Also store in session state for reference
            if "uploaded_documents" not in st.session_state:
                st.session_state.uploaded_documents = {}
            
            st.session_state.uploaded_documents[uploaded_file.name] = text_content
            st.success(f"Document '{uploaded_file.name}' uploaded and processed successfully!")
            st.info(f"**{uploaded_file.name}** is now available for the agent to reference.")
            st.info(f"Processing result: {result}")
            # Set the flag in session state
            st.session_state.processed_filename = uploaded_file.name
        else:
            st.warning("Could not extract sufficient text from the file.")
    except Exception as e:
        st.error(f"Failed to process document: {e}")

def extract_text_from_uploaded_file(uploaded_file):
    """Simple text extractor for PDF, TXT, and MD files."""
    file_extension = Path(uploaded_file.name).suffix.lower()
    if file_extension == ".pdf":
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
            return None
    elif file_extension in ['.txt', '.md']:
        return uploaded_file.getvalue().decode("utf-8")
    else:
        st.warning(f"Unsupported file type: {file_extension}. Only .txt, .md, and .pdf are supported.")
        return None

def clear_rag_database():
    try:
        # Clearing uploaded documents from session state
        if "uploaded_documents" in st.session_state:
            del st.session_state.uploaded_documents
        st.session_state.processed_filename = None
        st.toast("Document references cleared.")
    except Exception as e:
        st.error(f"Error clearing document references: {e}")

# Main App
def main():
    initialize_session_state()
    st.title("Prompt Refiner Agent")
    st.markdown("Enter a prompt to refine, or ask a question about an uploaded document.")

    # Sidebar
    with st.sidebar:
        st.header("Actions")
        if st.button("New Session", use_container_width=True):
            st.session_state.messages = []
            st.session_state.thread_id = str(uuid.uuid4())
            clear_rag_database() # Clear document references on new session
            st.rerun()

        st.header("Document Upload")
        st.caption("Upload a document to enable Q&A.")
        uploaded_file = st.file_uploader("Upload a document", type=['txt', 'md', 'pdf'])

        # process if the file is new.
        if uploaded_file is not None and uploaded_file.name != st.session_state.processed_filename:
            with st.spinner(f"Processing {uploaded_file.name}..."):
                process_uploaded_document(uploaded_file)
    
    # Chat Interface
    for message in st.session_state.messages:
        role, content = extract_message_content(message)
        with st.chat_message(role):
            st.markdown(content)

    if prompt := st.chat_input("Enter your prompt or question..."):
        st.session_state.messages.append(HumanMessage(content=prompt))
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response_message = process_refinement(prompt, st.session_state.thread_id)
                st.session_state.messages.append(response_message)
                st.markdown(response_message.content)

if __name__ == "__main__":
    main()