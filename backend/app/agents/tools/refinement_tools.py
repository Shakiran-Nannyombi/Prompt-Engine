import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3)

class RefinePromptArgs(BaseModel):
    prompt: str = Field(description="The user's original, unrefined prompt.")

# Clarity Tools 
@tool("core_refiner", args_schema=RefinePromptArgs, return_direct=False)
def core_refine(prompt: str) -> str:
    """Refines prompts using C.O.R.E. (Context, Objective, Role, Example).
    Best for prompts needing better structure."""
    
    if not prompt or not prompt.strip():
        return "Error: The prompt cannot be empty."
    
    system_prompt = f"""You are an expert prompt engineer. Refine the following user prompt using the C.O.R.E. framework.
Analyze the prompt and infer any missing components (Context, Objective, Role, Example).
User's Prompt: "{prompt}"
Construct a new, refined prompt based on your analysis."""

    refined_prompt = llm.invoke(system_prompt)
    return refined_prompt.content

@tool("race_refiner", args_schema=RefinePromptArgs, return_direct=False)
def race_refine(prompt: str) -> str:
    """Refines prompts using R.A.C.E. (Role, Action, Context, Expectation). 
    Best for prompts needing clear roles and actions."""
    
    if not prompt or not prompt.strip():
        return "Error: The prompt cannot be empty."
    
    system_prompt = f"""You are an expert prompt engineer. Refine the following user prompt using the R.A.C.E. framework.
Analyze the prompt and infer any missing components (Role, Action, Context, Expectation).
User's Prompt: "{prompt}"
Construct a new, refined prompt based on your analysis."""

    refined_prompt = llm.invoke(system_prompt)
    return refined_prompt.content

@tool("car_refiner", args_schema=RefinePromptArgs, return_direct=False)
def car_refine(prompt: str) -> str:
    """Refines prompts using C.A.R. (Context, Action, Result).
    Best for direct prompts needing clear context and outcomes."""
    
    if not prompt or not prompt.strip():
        return "Error: The prompt cannot be empty."
    
    system_prompt = f"""You are an expert prompt engineer. Refine the following user prompt using the C.A.R. framework.
Analyze the prompt and infer any missing components (Context, Action, Result).
User's Prompt: "{prompt}"
Construct a new, refined prompt based on your analysis."""

    refined_prompt = llm.invoke(system_prompt)
    return refined_prompt.content

@tool("spear_refiner", args_schema=RefinePromptArgs, return_direct=False)
def spear_refine(prompt: str) -> str:
    """Refines prompts using S.P.E.A.R. (Situation, Problem, Emotion, Action, Result).
    Best for complex prompts with emotional context."""
    
    if not prompt or not prompt.strip():
        return "Error: The prompt cannot be empty."
    
    system_prompt = f"""You are an expert prompt engineer. Refine the following user prompt using the S.P.E.A.R. framework.
Analyze the prompt and infer any missing components (Situation, Problem, Emotion, Action, Result).
User's Prompt: "{prompt}"
Construct a new, refined prompt based on your analysis."""

    refined_prompt = llm.invoke(system_prompt)
    return refined_prompt.content

clarity_tool_list = [core_refine, race_refine, car_refine, spear_refine]

# Precision Tools
@tool("risen_refiner", args_schema=RefinePromptArgs, return_direct=False)
def risen_refine(prompt: str) -> str:
    """Refines prompts using Risen (Role, Instructions, Steps, Goal, Narrowing).
    Best for technical prompts needing step-by-step instructions."""
    
    if not prompt or not prompt.strip():
        return "Error: The prompt cannot be empty."
    
    system_prompt = f"""You are an expert prompt engineer. Refine the following user prompt using the Risen framework.
Analyze the prompt and infer any missing components (Role, Instructions, Steps, Goal, Narrowing).
User's Prompt: "{prompt}"
Construct a new, refined prompt based on your analysis."""

    refined_prompt = llm.invoke(system_prompt)
    return refined_prompt.content

@tool("scorer_refiner", args_schema=RefinePromptArgs, return_direct=False)
def scorer_refine(prompt: str) -> str:
    """Refines prompts using SCORER (Set scene, Clarify task, Offer options, Refine output, 
    Evaluate, Reflect). Best for complex projects needing planning."""
    
    if not prompt or not prompt.strip():
        return "Error: The prompt cannot be empty."
    
    system_prompt = f"""You are an expert prompt engineer. Refine the following user prompt using the SCORER framework.
Analyze the prompt and infer any missing components (Set scene, Clarify task, Offer options, Refine output, Evaluate, Reflect).
User's Prompt: "{prompt}"
Construct a new, refined prompt based on your analysis."""

    refined_prompt = llm.invoke(system_prompt)
    return refined_prompt.content

precision_tool_list = [risen_refine, scorer_refine]

# Creative Tools 
@tool("idea_refiner", args_schema=RefinePromptArgs, return_direct=False)
def idea_refine(prompt: str) -> str:
    """Refines prompts using IDEA (Inspire, Develop, Express, Assess). 
    Best for creative prompts needing brainstorming."""
    
    if not prompt or not prompt.strip():
        return "Error: The prompt cannot be empty."
    system_prompt = f"""You are an expert prompt engineer. Refine the following user prompt using the IDEA framework.
Analyze the prompt and infer any missing components (Inspire, Develop, Express, Assess).
User's Prompt: "{prompt}"
Construct a new, refined prompt based on your analysis."""

    refined_prompt = llm.invoke(system_prompt)
    return refined_prompt.content

creative_tool_list = [idea_refine]

# RAG Tools
@tool("document_search")
def search_documents(query: str) -> str:
    """Searches uploaded documents for context to help refine a prompt. 
    Use this when you need information from a file."""
    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        persist_directory = "./chroma_db"
        
        if not os.path.exists(persist_directory):
            return "No documents have been uploaded."
        
        vector_store = Chroma(
            collection_name="uploads_collection",
            embedding_function=embeddings,
            persist_directory=persist_directory
        )
        results = vector_store.similarity_search(query, k=3)
        
        if not results:
            return "No relevant documents found."
        context = "Relevant document context:\n\n" + "\n\n".join([f"Document {i+1}:\n{doc.page_content}" for i, doc in enumerate(results)])
        return context
    except Exception as e:
        return f"Error searching documents: {str(e)}"

@tool("file_processor")
def process_uploaded_file(file_content: str) -> str:
    """Extracts text, generates embeddings, and stores it in the vector database."""
    try:
        documents = [Document(page_content=file_content, metadata={"source": "user_upload"})]
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        
        split_docs = text_splitter.split_documents(documents)
        
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        
        persist_directory = "./chroma_db"
        
        vector_store = Chroma(
            collection_name="uploads_collection",
            embedding_function=embeddings,
            persist_directory=persist_directory
        )
        vector_store.add_documents(split_docs)
        
        return f"Successfully processed and embedded file. Created {len(split_docs)} chunks."
    except Exception as e:
        return f"Error processing file: {str(e)}"

rag_tool_list = [search_documents, process_uploaded_file]