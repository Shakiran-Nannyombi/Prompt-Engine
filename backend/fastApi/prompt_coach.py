from fastapi import APIRouter, HTTPException
from models.coachResponse import CoachingResponse
from models.coachRequest import CoachingRequest
from agents import coach_agent
import uuid
from typing import Dict

router = APIRouter()

@router.post("/chat", response_model=CoachingResponse)
async def chat_with_coach(request: CoachingRequest):
    try:
        # Validating user input
        if not request.user_input or not request.user_input.strip():
            raise HTTPException(status_code=400, detail="User input cannot be empty")
        
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
        messages.append(("human", request.user_input))
        
        # Generating unique thread ID for conversation persistence
        thread_id = request.thread_id if hasattr(request, 'thread_id') and request.thread_id else "default_thread"
        
        # Invoking compiled coaching graph with conversation context and thread management
        final_state = coach_agent.coach_graph.invoke(
            {"messages": messages},
            config={"configurable": {"thread_id": thread_id}}
        )
        
        # Validating if agent response exists
        if not final_state.get("messages") or len(final_state["messages"]) == 0:
            raise HTTPException(status_code=500, detail="No response generated from coach agent")
        
        # Getting the latest message from the agent
        agent_output = final_state["messages"][-1].content
        
        # creating conversation history
        serialized_history = []
        for msg in final_state.get("messages", []):
            role, content = coach_agent.extract_message_content(msg)
            serialized_history.append({"role": role, "content": content})
        
        refined_prompt = (
            final_state.get("final_prompt_corrected") or 
            final_state.get("final_prompt")
        )
        
        return CoachingResponse(
            agent_output=agent_output,
            refined_prompt=refined_prompt,
            conversation_history=serialized_history
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/threads")
async def create_new_thread() -> Dict[str, str]:
    """Creating a new conversation thread ID"""
    try:
        thread_id = str(uuid.uuid4())
        return {"thread_id": thread_id}
    except Exception as e:
        print(f"Error creating thread: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
