from fastapi import APIRouter, HTTPException
from app.models.coachResponse import CoachingResponse
from app.models.coachRequest import CoachingRequest
from app.agents import coach_agent

router = APIRouter()

@router.post("/chat", response_model=CoachingResponse)
async def chat_with_coach(request: CoachingRequest):
    try:
        # inputting a list of messages to graph
        conversation_history = request.conversation_history or []
        graph_input = [("human", request.user_input)]

        final_state = coach_agent.invoke({"messages": graph_input})
        
        # responding with the latest message from the agent
        agent_output = final_state["messages"][-1].content
        
        return CoachingRequest(
            agent_output=agent_output,
            refined_prompt=final_state.get("final_prompt"),
            conversation_history=final_state["messages"] # sending back full history
        )
        
    except Exception as e:
       print(f"An error ocurred: {e}")
       raise HTTPException(status_code=500,detail="Internet Server Error") 