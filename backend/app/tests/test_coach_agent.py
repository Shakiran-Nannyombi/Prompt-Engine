import sys
import os

sys.path.append(os.path.abspath(".."))

from dotenv import load_dotenv
from unittest.mock import MagicMock, patch
from langchain_core.messages import HumanMessage, AIMessage

# Loading environment variables from .env file
load_dotenv(dotenv_path="../.env")

from agents.coach_agent import process_task_input, process_context_input, process_reference_input, extract_message_content
from models.evaluation import EvaluationResult

def test_process_task_input_sufficient():
    """Test that a well-defined task moves to context phase"""
    # Mock state with a good task description
    state = {
        "messages": [HumanMessage(content="I want to create a customer service feedback chatbot for my e-commerce company that can categorize complaints and generate appropriate responses.")],
        "current_step": "awaiting_task_input"
    }

    # Mock the language model's response for evaluation
    mock_evaluation_result = EvaluationResult(
        is_correct=True, 
        feedback="Task is well-defined and actionable.", 
        updated_prompt=None
    )
    
    # Mock the evaluation_llm.invoke method
    with patch('agents.coach_agent.evaluation_llm') as mock_llm:
        mock_llm.invoke.return_value = mock_evaluation_result
        result = process_task_input(state)

    # Verify the result - use actual step names from implementation
    assert result["current_step"] == "awaiting_context_input"
    assert result["task"] is not None
    assert "context" in result["messages"][0].content.lower()
    assert result["evaluation_result"].is_correct == True

def test_process_task_input_insufficient():
    """Test that a vague task description requires refinement"""
    # Mock state with vague task
    state = {
        "messages": [HumanMessage(content="a chatbot")],
        "current_step": "awaiting_task_input"
    }
    
    # Mock evaluation result for insufficient task
    mock_evaluation_result = EvaluationResult(
        is_correct=False, 
        feedback="The task is too vague. Please specify what kind of chatbot, its purpose, target audience, and desired functionality.", 
        updated_prompt="a chatbot"
    )

    # Mock the evaluation_llm.invoke method
    with patch('agents.coach_agent.evaluation_llm') as mock_llm:
        mock_llm.invoke.return_value = mock_evaluation_result
        result = process_task_input(state)

    # Verify feedback is provided and step remains the same
    assert result["current_step"] == "awaiting_task_input"
    assert result["evaluation_result"].is_correct == False
    assert "clearer understanding" in result["messages"][0].content.lower()

def test_process_task_input_suggestions():
    """Test that asking for suggestions provides task ideas"""
    # Mock state asking for suggestions
    state = {
        "messages": [HumanMessage(content="Can you suggest some tasks for me?")],
        "current_step": "awaiting_task_input"
    }

    # Mock the regular LLM response for suggestions
    mock_llm_response = MagicMock()
    mock_llm_response.content = """
    1. Create a customer service chatbot for an e-commerce platform
    2. Design a creative writing assistant for fantasy stories  
    3. Build a code review assistant for Python projects
    4. Develop a meal planning assistant for dietary restrictions
    """

    with patch('agents.coach_agent.llm') as mock_llm:
        mock_llm.invoke.return_value = mock_llm_response
        result = process_task_input(state)

    # Verify suggestions are provided
    assert result["current_step"] == "awaiting_task_input"
    assert "creative task suggestions" in result["messages"][0].content
    assert "customer service chatbot" in result["messages"][0].content

def test_process_task_input_greeting():
    """Test that greetings are handled appropriately"""
    # Mock state with greeting
    state = {
        "messages": [HumanMessage(content="hi")],
        "current_step": "awaiting_task_input"
    }

    result = process_task_input(state)

    # Verify greeting response
    assert result["current_step"] == "awaiting_task_input"
    assert "excited to help" in result["messages"][0].content

def test_process_context_input_sufficient():
    """Test that good context moves to references phase"""
    # Mock state with good context
    state = {
        "messages": [HumanMessage(content="The chatbot will be used by our customer support team to handle common inquiries about orders, returns, and product information. It should integrate with our existing CRM system and maintain a friendly, professional tone.")],
        "current_step": "awaiting_context_input",
        "task": "Create a customer service chatbot"
    }

    # Mock evaluation result for good context
    mock_evaluation_result = EvaluationResult(
        is_correct=True,
        feedback="Context is comprehensive and relevant.",
        updated_prompt=None
    )

    with patch('agents.coach_agent.evaluation_llm') as mock_llm:
        mock_llm.invoke.return_value = mock_evaluation_result
        result = process_context_input(state)

    # Verify progression to references
    assert result["current_step"] == "awaiting_reference_input"
    assert result["context"] is not None
    assert "references" in result["messages"][0].content.lower()

def test_process_context_input_insufficient():
    """Test that insufficient context requires more detail"""
    # Mock state with insufficient context
    state = {
        "messages": [HumanMessage(content="It's for customer service.")],
        "current_step": "awaiting_context_input",
        "task": "Create a customer service chatbot"
    }

    # Mock evaluation result for insufficient context
    mock_evaluation_result = EvaluationResult(
        is_correct=False,
        feedback="The context lacks specific details about the use case, target audience, and requirements.",
        updated_prompt=None
    )

    with patch('agents.coach_agent.evaluation_llm') as mock_llm:
        mock_llm.invoke.return_value = mock_evaluation_result
        result = process_context_input(state)

    # Verify feedback and staying in same step
    assert result["current_step"] == "awaiting_context_input"
    assert result["evaluation_result"].is_correct == False
    assert "more detailed context" in result["messages"][0].content.lower()

def test_process_reference_input_sufficient():
    """Test that good references move to final prompt phase"""
    # Mock state with good references
    state = {
        "messages": [HumanMessage(content="I can provide examples of successful customer service conversations, our company's tone guide, and links to our product documentation. We also have a knowledge base with FAQs.")],
        "current_step": "awaiting_reference_input",
        "task": "Create a customer service chatbot",
        "context": "For handling customer inquiries in e-commerce"
    }

    # Mock evaluation result for good references
    mock_evaluation_result = EvaluationResult(
        is_correct=True,
        feedback="References are relevant and comprehensive.",
        updated_prompt=None
    )

    with patch('agents.coach_agent.evaluation_llm') as mock_llm:
        mock_llm.invoke.return_value = mock_evaluation_result
        result = process_reference_input(state)

    # Verify progression to final prompt
    assert result["current_step"] == "awaiting_final_prompt"
    assert len(result["references"]) > 0
    assert "final prompt" in result["messages"][0].content.lower()
    assert result["summary"] is not None

def test_process_reference_input_insufficient():
    """Test that insufficient references require improvement"""
    # Mock state with insufficient references
    state = {
        "messages": [HumanMessage(content="Some docs.")],
        "current_step": "awaiting_reference_input",
        "task": "Create a customer service chatbot",
        "context": "For handling customer inquiries"
    }

    # Mock evaluation result for insufficient references
    mock_evaluation_result = EvaluationResult(
        is_correct=False,
        feedback="References are too vague. Please specify what documents, examples, or resources you can provide.",
        updated_prompt=None
    )

    with patch('agents.coach_agent.evaluation_llm') as mock_llm:
        mock_llm.invoke.return_value = mock_evaluation_result
        result = process_reference_input(state)

    # Verify feedback and staying in same step
    assert result["current_step"] == "awaiting_reference_input"
    assert result["evaluation_result"].is_correct == False
    assert "better references" in result["messages"][0].content.lower()

def test_edge_cases():
    """Test edge cases and error handling"""
    
    # Test with no messages
    state_no_messages = {
        "messages": [],
        "current_step": "awaiting_task_input"
    }
    
    result = process_task_input(state_no_messages)
    assert result["current_step"] == "error"
    
    # Test with non-HumanMessage
    state_wrong_message_type = {
        "messages": [AIMessage(content="Hello")],
        "current_step": "awaiting_task_input"
    }
    
    result = process_task_input(state_wrong_message_type)
    assert result["current_step"] == "error"

def test_message_extraction():
    """Test the extract_message_content function"""
    
    # Test different message types
    ai_message = AIMessage(content="Hello from AI")
    human_message = HumanMessage(content="Hello from human")
    
    ai_role, ai_content = extract_message_content(ai_message)
    assert ai_role == "assistant"
    assert ai_content == "Hello from AI"
    
    human_role, human_content = extract_message_content(human_message)
    assert human_role == "user"
    assert human_content == "Hello from human"

# Integration test
def test_full_workflow_integration():
    """Test a complete workflow from task to context"""
    
    # Start with task input
    initial_state = {
        "messages": [HumanMessage(content="Create a customer service chatbot for handling order inquiries and returns")],
        "current_step": "awaiting_task_input"
    }
    
    # Mock successful task evaluation
    mock_task_result = EvaluationResult(is_correct=True, feedback="", updated_prompt=None)
    
    with patch('agents.coach_agent.evaluation_llm') as mock_llm:
        mock_llm.invoke.return_value = mock_task_result
        task_result = process_task_input(initial_state)
    
    # Verify task was processed and moved to context
    assert task_result["current_step"] == "awaiting_context_input"
    assert task_result["task"] is not None
    
    # Continue to context input
    context_state = {
        **task_result,
        "messages": task_result["messages"] + [HumanMessage(content="This will be used by our support team to handle common customer questions about orders, shipping, and returns. It needs to integrate with our CRM.")],
        "current_step": "awaiting_context_input"  # Make sure step is set correctly
    }
    
    # Mock successful context evaluation
    mock_context_result = EvaluationResult(is_correct=True, feedback="", updated_prompt=None)
    
    with patch('agents.coach_agent.evaluation_llm') as mock_llm:
        mock_llm.invoke.return_value = mock_context_result
        context_result = process_context_input(context_state)
    
    # Verify context was processed and moved to references
    assert context_result["current_step"] == "awaiting_reference_input"
    assert context_result["context"] is not None

def test_process_final_prompt():
    """Test processing of final prompt"""
    from agents.coach_agent import process_final_prompt
    
    # Mock state with final prompt
    state = {
        "messages": [HumanMessage(content="You are a customer service chatbot for an e-commerce platform. Your role is to assist customers with order inquiries, returns, and product information. Use a friendly, professional tone and always try to be helpful. If you cannot resolve an issue, escalate to a human agent.")],
        "current_step": "awaiting_final_prompt",
        "summary": "Task: Create customer service chatbot\nContext: E-commerce support\nReferences: Documentation provided"
    }
    
    # Mock evaluation result for good final prompt
    mock_evaluation_result = EvaluationResult(
        is_correct=True,
        feedback="Prompt is well-structured and complete.",
        updated_prompt=None
    )
    
    with patch('agents.coach_agent.evaluation_llm') as mock_llm:
        mock_llm.invoke.return_value = mock_evaluation_result
        result = process_final_prompt(state)
    
    # Verify final prompt is accepted
    assert result["current_step"] == "ready_to_refine"
    assert result["final_prompt"] is not None
    assert "polish it for you" in result["messages"][0].content

def test_process_final_prompt_insufficient():
    """Test insufficient final prompt"""
    from agents.coach_agent import process_final_prompt
    
    # Mock state with insufficient final prompt
    state = {
        "messages": [HumanMessage(content="Be a chatbot.")],
        "current_step": "awaiting_final_prompt",
        "summary": "Task: Create customer service chatbot"
    }
    
    # Mock evaluation result for insufficient final prompt
    mock_evaluation_result = EvaluationResult(
        is_correct=False,
        feedback="The prompt lacks specificity and clear instructions.",
        updated_prompt=None
    )
    
    with patch('agents.coach_agent.evaluation_llm') as mock_llm:
        mock_llm.invoke.return_value = mock_evaluation_result
        result = process_final_prompt(state)
    
    # Verify feedback and staying in same step
    assert result["current_step"] == "awaiting_final_prompt"
    assert result["evaluation_result"].is_correct == False
    assert "refine your prompt" in result["messages"][0].content

if __name__ == "__main__":
    # Run tests
    print("Running tests...")
    
    test_process_task_input_sufficient()
    print("✓ Task input sufficient test passed")
    
    test_process_task_input_insufficient()
    print("✓ Task input insufficient test passed")
    
    test_process_task_input_suggestions()
    print("✓ Task suggestions test passed")
    
    test_process_task_input_greeting()
    print("✓ Task greeting test passed")
    
    test_process_context_input_sufficient()
    print("✓ Context input sufficient test passed")
    
    test_process_context_input_insufficient()
    print("✓ Context input insufficient test passed")
    
    test_process_reference_input_sufficient()
    print("✓ Reference input sufficient test passed")
    
    test_process_reference_input_insufficient()
    print("✓ Reference input insufficient test passed")
    
    test_edge_cases()
    print("✓ Edge cases test passed")
    
    test_message_extraction()
    print("✓ Message extraction test passed")
    
    test_full_workflow_integration()
    print("✓ Full workflow integration test passed")
    
    test_process_final_prompt()
    print("✓ Process final prompt test passed")
    
    test_process_final_prompt_insufficient()
    print("✓ Process final prompt insufficient test passed")
    
    print("\nAll tests passed!")