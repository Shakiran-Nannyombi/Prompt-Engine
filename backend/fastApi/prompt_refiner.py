from fastapi import APIRouter, HTTPException
from models.refinerResponse import RefinerResponse
from models.refinerRequest import RefinerRequest
from models.refine_prompt import RefinementAnalysis
from agents import refiner_agent
import uuid
from typing import Dict

router = APIRouter()

@router.post("/refine_chat", response_model=RefinerResponse)
async def refine_prompt(request: RefinerRequest):
    try:
        # Validating user input
        if not request.original_prompt or not request.original_prompt.strip():
            raise HTTPException(status_code=400, detail="Original prompt cannot be empty")
        
        # preserving conversation state
        messages = []
        
        # Adding conversation history
        if request.conversation_history:
            for msg in request.conversation_history:
                if msg["role"] == "user":
                    messages.append(("human", msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(("ai", msg["content"]))
        
        # Adding current user input
        messages.append(("human", request.original_prompt))
        
        # Generating unique thread ID for conversation persistence
        thread_id = request.thread_id if hasattr(request, 'thread_id') and request.thread_id else "default_thread"
        
        # Invoking compiled refiner graph with conversation context and thread management
        final_state = refiner_agent.refiner_graph.invoke(
            {
                "messages": messages,
                "original_prompt": request.original_prompt,
                "has_document": request.has_document or False
            },
            config={"configurable": {"thread_id": thread_id}}
        )
        
        # Validating for agent response
        if not final_state.get("messages") or len(final_state["messages"]) == 0:
            raise HTTPException(status_code=500, detail="No response generated from refiner agent")
        
        # Getting latest message from the agent
        agent_output = final_state["messages"][-1].content
        
        # creating conversation history
        serialized_history = []
        for msg in final_state.get("messages", []):
            role, content = refiner_agent.extract_message_content(msg)
            serialized_history.append({"role": role, "content": content})
        
        # Getting refinement analysis
        refined_prompt = final_state.get("refined_prompt")
        prompt_category = final_state.get("prompt_category")
        framework_used = final_state.get("framework_used")
        
        # Creating refinement analysis if we have the data
        refinement_analysis = None
        if refined_prompt and prompt_category and framework_used:
            refinement_analysis = RefinementAnalysis(
                category=prompt_category,
                framework_used=framework_used,
                reasoning=f"Applied {framework_used} framework for {prompt_category} improvement",
                refined_prompt=refined_prompt
            )
        
        return RefinerResponse(
            agent_output=agent_output,
            refined_prompt=refined_prompt,
            prompt_category=prompt_category,
            framework_used=framework_used,
            refinement_analysis=refinement_analysis,
            conversation_history=serialized_history
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/threads")
async def create_new_refiner_thread() -> Dict[str, str]:
    """Creating a new conversation thread ID for refiner"""
    try:
        thread_id = str(uuid.uuid4())
        return {"thread_id": thread_id}
    except Exception as e:
        print(f"Error creating refiner thread: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

