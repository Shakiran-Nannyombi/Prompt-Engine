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
    
    system_prompt = f"""You are an expert prompt engineer. Refine the following user prompt using the C.O.R.E. framework (Context, Objective, Role, Example).

User's Prompt: "{prompt}"

IMPORTANT: Only work with the information the user actually provided. Do NOT invent, assume, or hallucinate specific details like dates, names, locations, or scenarios that weren't mentioned.

If the prompt is missing key information, create placeholders like [specify context], [your role], [desired outcome] and suggest what information would be helpful.

Enhance the prompt by:
- Making the objective clearer and more specific
- Adding structure and format requirements
- Suggesting what context or role would be helpful (without inventing it)
- Providing guidance on desired outcomes

Create a refined version that builds on what they provided while identifying what additional information would make it even better."""

    refined_prompt = llm.invoke(system_prompt)
    return refined_prompt.content

@tool("race_refiner", args_schema=RefinePromptArgs, return_direct=False)
def race_refine(prompt: str) -> str:
    """Refines prompts using R.A.C.E. (Role, Action, Context, Expectation). 
    Best for prompts needing clear roles and actions."""
    
    if not prompt or not prompt.strip():
        return "Error: The prompt cannot be empty."
    
    system_prompt = f"""You are an expert prompt engineer. Refine the following user prompt using the R.A.C.E. framework (Role, Action, Context, Expectation).

User's Prompt: "{prompt}"

IMPORTANT: Only work with the information the user actually provided. Do NOT invent, assume, or hallucinate specific details like dates, names, locations, or scenarios that weren't mentioned.

If the prompt lacks specific information, use placeholders like [your role], [specific context], [desired format] and suggest what details would be helpful.

Enhance the prompt by:
- Clarifying the role/perspective needed
- Making the action more specific and actionable
- Adding structure for context that should be provided
- Setting clear expectations for the output

Create a refined version that builds on their actual input while indicating where more specifics would improve results."""

    refined_prompt = llm.invoke(system_prompt)
    return refined_prompt.content

@tool("car_refiner", args_schema=RefinePromptArgs, return_direct=False)
def car_refine(prompt: str) -> str:
    """Refines prompts using C.A.R. (Context, Action, Result).
    Best for direct prompts needing clear context and outcomes."""
    
    if not prompt or not prompt.strip():
        return "Error: The prompt cannot be empty."
    
    system_prompt = f"""You are an expert prompt engineer. Refine the following user prompt using the C.A.R. framework (Context, Action, Result).

User's Prompt: "{prompt}"

IMPORTANT: Only work with the information the user actually provided. Do NOT invent, assume, or hallucinate specific details like dates, names, locations, or scenarios that weren't mentioned.

If the prompt lacks specific information, use placeholders like [provide context], [specific action needed], [desired result format] and suggest what details would be helpful.

Enhance the prompt by:
- Adding structure for context that should be provided
- Making the action more specific and clear
- Defining what the result should look like
- Suggesting what additional information would improve the outcome

Create a refined version that works with their actual input while indicating where more details would enhance results."""

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
    
    system_prompt = f"""You are an expert prompt engineer. Refine the following user prompt using the RISEN framework (Role, Instructions, Steps, End goal, Narrowing).

User's Prompt: "{prompt}"

IMPORTANT: Only work with the information the user actually provided. Do NOT invent, assume, or hallucinate specific details like dates, names, locations, or scenarios that weren't mentioned.

If the prompt lacks specific information, use placeholders like [your role], [specific context], [step-by-step process], [desired outcome] and suggest what details would be helpful.

Enhance the prompt by:
- Clarifying what role/perspective is needed
- Breaking down the task into clear instructions
- Suggesting a step-by-step approach structure
- Defining the end goal more specifically
- Adding appropriate constraints or scope

Create a refined version that builds on their actual input while indicating where more specifics would improve the results."""

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
    system_prompt = f"""You are an expert prompt engineer. Refine the following user prompt using the IDEA framework (Inspire, Develop, Express, Assess).

User's Prompt: "{prompt}"

IMPORTANT: Only work with the information the user actually provided. Do NOT invent, assume, or hallucinate specific details like dates, names, locations, companies, or scenarios that weren't mentioned.

If the prompt lacks specific information, use placeholders like [specify your context], [your requirements], [desired format] and suggest what details would be helpful.

Enhance the prompt by:
- Making the objective clearer and more actionable
- Adding structure for the type of output desired
- Suggesting what context or constraints would be helpful
- Defining success criteria or evaluation methods

Create a refined version that builds on what they provided while indicating where additional specifics would improve the results."""

    refined_prompt = llm.invoke(system_prompt)
    return refined_prompt.content

creative_tool_list = [idea_refine]

# RAG Tools
@tool("document_search")
def search_documents(query: str) -> str:
    """Searches uploaded documents for context to help refine a prompt. 
    Use this when you need information from a file or want to reference uploaded content."""
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'batch_size': 32}
        )
        persist_directory = "./chroma_db"
        
        if not os.path.exists(persist_directory):
            return "No documents have been uploaded yet. Please upload a document first."
        
        vector_store = Chroma(
            collection_name="uploads_collection",
            embedding_function=embeddings,
            persist_directory=persist_directory
        )
        
        # Search with better parameters for more relevant results
        results = vector_store.similarity_search_with_score(query, k=5)
        
        if not results:
            return "No relevant content found in uploaded documents for your query."
        
        # Filtering results by relevance score (lower scores are more similar)
        relevant_results = [(doc, score) for doc, score in results if score < 0.8]
        
        if not relevant_results:
            return "No highly relevant content found in uploaded documents for your query."
        
        # Formatting results with metadata and relevance scores
        context_parts = []
        for i, (doc, score) in enumerate(relevant_results):
            filename = doc.metadata.get('filename', 'unknown')
            relevance = "High" if score < 0.4 else "Medium" if score < 0.6 else "Low"
            context_parts.append(
                f"**Source {i+1}** (from {filename}, relevance: {relevance}):\n{doc.page_content}\n"
            )
        
        context = "Found relevant content from uploaded documents:\n\n" + "\n".join(context_parts)
        return context
        
    except Exception as e:
        return f"Error searching documents: {str(e)}"

@tool("file_processor")
def process_uploaded_file(file_content: str, filename: str = "uploaded_document") -> str:
    """Extracts text, generates embeddings, and stores it in the vector database with optimized batch processing."""
    try:
        # Creating document with better metadata
        documents = [Document(
            page_content=file_content, 
            metadata={
                "source": "user_upload",
                "filename": filename
            }
        )]
        
        # Optimized chunking strategy for better performance
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,  # Larger chunks for better context
            chunk_overlap=200,  # More overlap for continuity
            separators=["\n\n", "\n", ". ", " ", ""]  # Better separation
        )
        
        split_docs = text_splitter.split_documents(documents)
        
        # Initialize embeddings once
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'batch_size': 32}  # Batch processing
        )
        
        persist_directory = "./chroma_db"
        
        # Initializing vector store
        vector_store = Chroma(
            collection_name="uploads_collection",
            embedding_function=embeddings,
            persist_directory=persist_directory
        )
        
        # Batch processing for better performance
        batch_size = 10
        total_chunks = len(split_docs)
        
        for i in range(0, total_chunks, batch_size):
            batch = split_docs[i:i + batch_size]
            vector_store.add_documents(batch)
        
        return f"Successfully processed '{filename}'. Created {len(split_docs)} chunks with optimized batching."
    except Exception as e:
        return f"Error processing file: {str(e)}"

rag_tool_list = [search_documents, process_uploaded_file]