import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Load environment variables
load_dotenv()

# Initializing the LLM
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3)

class RefinePromptArgs(BaseModel):
    prompt: str = Field(description="The user's original, unrefined prompt.")

# Prompt Frameworks for Clarity and Efficiency (Simple Tasks)
# Tool 1: C.O.R.E. 
@tool("core_refiner", args_schema=RefinePromptArgs, return_direct=False)
def core_refine(prompt: str) -> str:
    """
    Refines prompts using the C.O.R.E. framework (Context, Objective, Role, Example).
    Best for: Prompts needing better structure and clear communication.
    """
    if not prompt or not prompt.strip():
        return "Error: The prompt cannot be empty."

    # Instructing the LLM on how to perform the C.O.R.E. refinement.
    system_prompt = f"""
You are an expert in prompt engineering. Your task is to refine the following user's prompt using the C.O.R.E. framework.
Analyze the user's prompt and extract or infer the four key components:

1.  **Context:** What is the necessary background information?
2.  **Objective:** What is the primary goal the user wants to achieve?
3.  **Role:** What perspective or persona should the AI adopt?
4.  **Example:** What is a good example of the desired output format or tone?

If a component is missing from the user's prompt, you MUST infer a reasonable value for it. Do not ask for clarification.

**User's Prompt:** "{prompt}"

Now, construct a new, refined prompt based on your analysis, formatted clearly using the C.O.R.E. structure.
    """

    # Calling the LLM with the system prompt to get the refined prompt.
    refined_prompt = llm.invoke(system_prompt)

    # The tool returns only the final, refined prompt string.
    return refined_prompt.content
   

# Tool 2: R.A.C.E. 
@tool("race_refiner", args_schema=RefinePromptArgs, return_direct=False)
def race_refine(prompt: str) -> str:
    """
    Refines prompts using the R.A.C.E. framework (Role, Action, Context, Expectation).
    Best for: Prompts needing clear role definition and action steps.
    """
    if not prompt or not prompt.strip():
        return "Error: The prompt cannot be empty."

    # Instructing the LLM on how to perform the R.A.C.E. refinement.
    system_prompt = f"""
You are an expert in prompt engineering. Your task is to refine the following user's prompt using the R.A.C.E. framework.
Analyze the user's prompt and extract or infer the four key components:

1.  **Role:** What specific character or persona should the AI adopt?
2.  **Action:** What specific task should the AI perform?
3.  **Context:** What background information is necessary?
4.  **Expectation:** What is the desired outcome or output format?

If a component is missing from the user's prompt, you MUST infer a reasonable value for it. Do not ask for clarification.

**User's Prompt:** "{prompt}"

Now, construct a new, refined prompt based on your analysis, formatted clearly using the R.A.C.E. structure.
    """

    # Calling the LLM with the system prompt to get the refined prompt.
    refined_prompt = llm.invoke(system_prompt)

    # The tool returns only the final, refined prompt string.
    return refined_prompt.content


# Tool 3: C.A.R.
@tool("car_refiner", args_schema=RefinePromptArgs, return_direct=False)
def car_refine(prompt: str) -> str:
    """
    Refines prompts using the C.A.R. framework (Context, Action, Result).
    Best for: Prompts needing clear context and expected outcomes.
    """
    if not prompt or not prompt.strip():
        return "Error: The prompt cannot be empty."

    # Instructing the LLM on how to perform the C.A.R. refinement.
    system_prompt = f"""
You are an expert in prompt engineering. 
Your task is to refine the following user's prompt using the C.A.R. framework.
Analyze the user's prompt and extract or infer the three key components:

1.  **Context:** What is the necessary background information?
2.  **Action:** What is the specific task the AI should perform?
3.  **Result:** What is the desired outcome or output format?

If a component is missing from the user's prompt, you MUST infer a reasonable value for it.
Do not ask for clarification.

**User's Prompt:** "{prompt}"

Now, construct a new, refined prompt based on your analysis,
formatted clearly using the C.A.R. structure.
    """

    # Calling the LLM with the system prompt to get the refined prompt.
    refined_prompt = llm.invoke(system_prompt)

    # The tool returns only the final, refined prompt string.
    return refined_prompt.content   


# Tool 4: S.P.E.A.R. 
@tool("spear_refiner", args_schema=RefinePromptArgs, return_direct=False)
def spear_refine(prompt: str) -> str:
    """
    Refines prompts using the S.P.E.A.R. framework (Situation, Problem, Emotion, Action, Result).
    Best for: Complex prompts needing comprehensive analysis and emotional context.
    """
    if not prompt or not prompt.strip():
        return "Error: The prompt cannot be empty."

    # Instructing the LLM on how to perform the S.P.E.A.R. refinement.
    system_prompt = f"""
You are an expert in prompt engineering. 
Your task is to refine the following user's prompt using the S.P.E.A.R. framework.
Analyze the user's prompt and extract or infer the five key components:

1.  **Situation:** What is the current situation or context?
2.  **Problem:** What is the specific problem or challenge?
3.  **Emotion:** What is the emotional tone or sentiment?
4.  **Action:** What action should the AI take?
5.  **Result:** What is the desired outcome or output format?

If a component is missing from the user's prompt, you MUST infer a reasonable value for it.
Do not ask for clarification.

**User's Prompt:** "{prompt}"

Now, construct a new, refined prompt based on your analysis,
formatted clearly using the S.P.E.A.R. structure.
    """

    # Calling the LLM with the system prompt to get the refined prompt.
    refined_prompt = llm.invoke(system_prompt)

    # The tool returns only the final, refined prompt string.
    return refined_prompt.content   

# A list of all tools in this category
clarity_tool_list = [core_refine, race_refine, car_refine, spear_refine]

# Prompt Frameworks for Precision and Complex Tasks
# Tool 5: Risen
@tool("risen_refiner", args_schema=RefinePromptArgs, return_direct=False)
def risen_refine(prompt: str) -> str:
    """
    Refines prompts using the Risen framework (Role, Instructions, Steps, Goal, Narrowing).
    Best for: Technical prompts needing detailed step-by-step instructions and constraints.
    """
    if not prompt or not prompt.strip():
        return "Error: The prompt cannot be empty."

    # Instructing the LLM on how to perform the Risen refinement.
    system_prompt = f"""
You are an expert in prompt engineering.
Your task is to refine the following user's prompt using the Risen framework.
Analyze the user's prompt and extract or infer the key components:

1.  **Role:** What role should the AI assume?
2.  **Instructions:** What specific instructions should the AI follow?
3.  **Steps:** What are the detailed steps the AI should take?
4.  **Goal:** What is the clear end goal?
5.  **Narrowing:** What constraints should the AI consider?

If a component is missing from the user's prompt, you MUST infer a reasonable value for it.
Do not ask for clarification.

**User's Prompt:** "{prompt}"

Now, construct a new, refined prompt based on your analysis,
formatted clearly using the Risen structure.
    """

    # Calling the LLM with the system prompt to get the refined prompt.
    refined_prompt = llm.invoke(system_prompt)

    # The tool returns only the final, refined prompt string.
    return refined_prompt.content   


# 6. Tool: SCORER 
@tool("scorer_refiner", args_schema=RefinePromptArgs, return_direct=False)
def scorer_refine(prompt: str) -> str:
    """
    Refines prompts using the SCORER framework (Set scene, Clarify task, Offer options, Refine output, Evaluate results, Reflect).
    Best for: Complex projects needing comprehensive planning and evaluation processes.
    """
    if not prompt or not prompt.strip():
        return "Error: The prompt cannot be empty."

    # Instructing the LLM on how to perform the SCORER refinement.
    system_prompt = f"""
You are an expert in prompt engineering.
Your task is to refine the following user's prompt using the SCORER framework.
Analyze the user's prompt and extract or infer the key components:

1.  **Set the scene:** What is the context or background?
2.  **Clarify the task:** What specific task needs to be accomplished?
3.  **Offer options:** What are the possible approaches or solutions?
4.  **Refine the output:** How can the output be improved or made more precise?
5.  **Evaluate the results:** How will the results be assessed?
6.  **Reflect on the process:** What insights can be gained from this process?

If a component is missing from the user's prompt, you MUST infer a reasonable value for it.
Do not ask for clarification.

**User's Prompt:** "{prompt}"

Now, construct a new, refined prompt based on your analysis,
formatted clearly using the SCORER structure.
    """

    # Calling the LLM with the system prompt to get the refined prompt.
    refined_prompt = llm.invoke(system_prompt)

    # The tool returns only the final, refined prompt string.
    return refined_prompt.content

precision_tool_list = [risen_refine, scorer_refine]

# Prompt Frameworks For Creative and Brainstorming Tasks 
# 7. Tool: IDEA
@tool("idea_refiner", args_schema=RefinePromptArgs, return_direct=False)
def idea_refine(prompt: str) -> str:
    """
    Refines prompts using the IDEA framework (Inspire, Develop, Express, Assess).
    Best for: Creative prompts needing brainstorming and imaginative development.
    """
    if not prompt or not prompt.strip():
        return "Error: The prompt cannot be empty."

    # Instructing the LLM on how to perform the IDEA refinement.
    system_prompt = f"""
You are an expert in prompt engineering.
Your task is to refine the following user's prompt using the IDEA framework.
Analyze the user's prompt and extract or infer the key components:

1.  **Inspire:** How can the AI inspire creativity?
2.  **Develop:** What ideas need further development?
3.  **Express:** How can the ideas be expressed clearly?
4.  **Assess:** How will the effectiveness of the ideas be assessed?

If a component is missing from the user's prompt, you MUST infer a reasonable value for it.
Do not ask for clarification.

**User's Prompt:** "{prompt}"

Now, construct a new, refined prompt based on your analysis,
formatted clearly using the IDEA structure.
    """

    # Calling the LLM with the system prompt to get the refined prompt.
    refined_prompt = llm.invoke(system_prompt)

    # The tool returns only the final, refined prompt string.
    return refined_prompt.content

creative_tool_list = [idea_refine]

# RAG tools for document processing and search
@tool("document_search")
def search_documents(query: str) -> str:
    """
    Search uploaded documents for relevant context to help with prompt refinement.
    Use this when users need context from their uploaded files to improve their prompts.
    """
    try:
        # Initialize embeddings and vector store
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        
        # Check if vector store exists
        persist_directory = "./chroma_db"
        if not os.path.exists(persist_directory):
            return "No documents have been uploaded yet. Please upload some files first."

        # Loading existing vector store
        vector_store = Chroma(
            collection_name="uploads_collection",
            embedding_function=embeddings,
            persist_directory=persist_directory
        )
        
        # Searching for relevant documents
        results = vector_store.similarity_search(query, k=3)
        
        if not results:
            return "No relevant documents found for your query."
        
        # Format results
        context = "Relevant document context:\n\n"
        for i, doc in enumerate(results, 1):
            context += f"Document {i}:\n{doc.page_content}\n\n"
        
        return context
        
    except Exception as e:
        return f"Error searching documents: {str(e)}"

@tool("file_processor")
def process_uploaded_file(file_content: str) -> str:
    """
    Extracts text, generates embeddings, and stores in vector database.
    """
    try:
        # Creating documents from file content
        documents = [Document(page_content=file_content, metadata={"source": "user_upload"})]
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=100
        )
        split_docs = text_splitter.split_documents(documents)
        
        # Initializing embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )
        
        # Create or load vector store
        persist_directory = "./chroma_db"
        vector_store = Chroma(
            collection_name="uploads_collection",
            embedding_function=embeddings,
            persist_directory=persist_directory
        )
        
        # Add documents to vector store
        vector_store.add_documents(split_docs)
        vector_store.persist()
        
        return f"Successfully processed and embedded file. Created {len(split_docs)} chunks and stored in vector database."
        
    except Exception as e:
        return f"Error processing file: {str(e)}"

# Add RAG tools to the tool lists
rag_tool_list = [search_documents, process_uploaded_file]
    