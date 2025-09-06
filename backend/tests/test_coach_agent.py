"""
Simple pytest tests for the coach agent.
Tests basic functionality using actual environment variables.
"""
import os
import pytest
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the backend directory to Python path for imports
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import after loading env vars
from agents.coach_agent import (
    coach_graph, 
    CoachingState, 
    start_coaching, 
    process_task_input,
    process_context_input,
    process_reference_input,
    process_final_prompt,
    extract_message_content
)


class TestCoachAgent:
    """Test class for coach agent functionality."""
    
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup method that runs before each test."""
        # Verify required environment variables are set
        required_vars = [
            "GROQ_API_KEY",
            "COACH_LANGSMITH_API_KEY", 
            "COACH_LANGSMITH_PROJECT",
            "TAVILY_API_KEY",
            "DATABASE_URL"
        ]
        
        missing_vars = [var for var in required_vars if not os.environ.get(var)]
        if missing_vars:
            pytest.skip(f"Missing required environment variables: {missing_vars}")
    
    def test_environment_variables_loaded(self):
        """Test that all required environment variables are loaded."""
        assert os.environ.get("GROQ_API_KEY") is not None
        assert os.environ.get("COACH_LANGSMITH_API_KEY") is not None
        assert os.environ.get("COACH_LANGSMITH_PROJECT") is not None
        assert os.environ.get("TAVILY_API_KEY") is not None
        assert os.environ.get("DATABASE_URL") is not None
    
    def test_coach_graph_initialization(self):
        """Test that the coach graph initializes without errors."""
        assert coach_graph is not None
        assert hasattr(coach_graph, 'nodes')
        assert hasattr(coach_graph, 'edges')
    
    def test_start_coaching_node(self):
        """Test the start_coaching node functionality."""
        initial_state = {
            "messages": [],
            "current_step": "initial",
            "task": "",
            "context": "",
            "references": [],
            "final_prompt": "",
            "task_corrected": "",
            "context_corrected": "",
            "references_corrected": [],
            "final_prompt_corrected": ""
        }
        
        result = start_coaching(initial_state)
        
        assert "messages" in result
        assert len(result["messages"]) > 0
        assert result["current_step"] == "awaiting_task_input"
    
    def test_process_task_input_with_greeting(self):
        """Test process_task_input with a greeting message."""
        state = {
            "messages": [("human", "Hello!")],
            "current_step": "awaiting_task_input",
            "task": "",
            "context": "",
            "references": [],
            "final_prompt": "",
            "task_corrected": "",
            "context_corrected": "",
            "references_corrected": [],
            "final_prompt_corrected": ""
        }
        
        result = process_task_input(state)
        
        assert "messages" in result
        assert result["current_step"] == "awaiting_task_input"
    
    def test_process_task_input_with_task(self):
        """Test process_task_input with an actual task."""
        state = {
            "messages": [("human", "I want to write a prompt for generating marketing copy")],
            "current_step": "awaiting_task_input",
            "task": "",
            "context": "",
            "references": [],
            "final_prompt": "",
            "task_corrected": "",
            "context_corrected": "",
            "references_corrected": [],
            "final_prompt_corrected": ""
        }
        
        result = process_task_input(state)
        
        assert "messages" in result
        assert "task_corrected" in result
        # Should either accept the task or provide feedback
        assert result["current_step"] in ["awaiting_context_input", "awaiting_task_input"]
    
    def test_extract_message_content(self):
        """Test the extract_message_content helper function."""
        messages = [
            ("human", "Hello"),
            ("ai", "Hi there!"),
            ("human", "How are you?")
        ]
        
        result = extract_message_content(messages)
        
        assert isinstance(result, list)
        assert len(result) == 3
        assert result[0]["role"] == "human"
        assert result[0]["content"] == "Hello"
        assert result[1]["role"] == "ai"
        assert result[1]["content"] == "Hi there!"
    
    @patch('agents.coach_agent.llm')
    def test_grammar_correction_integration(self, mock_llm):
        """Test that grammar correction is integrated into the workflow."""
        # Mock the LLM response for grammar correction
        mock_response = MagicMock()
        mock_response.content = "I want to write a prompt for generating marketing copy."
        mock_llm.invoke.return_value = mock_response
        
        state = {
            "messages": [("human", "i want to write a prompt for generating marketing copy")],
            "current_step": "awaiting_task_input",
            "task": "",
            "context": "",
            "references": [],
            "final_prompt": "",
            "task_corrected": "",
            "context_corrected": "",
            "references_corrected": [],
            "final_prompt_corrected": ""
        }
        
        result = process_task_input(state)
        
        # Verify that grammar correction was attempted
        assert "task_corrected" in result
        mock_llm.invoke.assert_called()
    
    def test_coaching_state_structure(self):
        """Test that CoachingState has the expected structure."""
        state = CoachingState(
            task="test task",
            context="test context", 
            references=["ref1", "ref2"],
            evaluation_criteria="test criteria",
            final_prompt="test prompt",
            messages=[],
            current_step="test_step",
            evaluation_result=None,
            summary="test summary",
            task_corrected="corrected task",
            context_corrected="corrected context",
            references_corrected=["corrected ref1", "corrected ref2"],
            final_prompt_corrected="corrected prompt"
        )
        
        assert state["task"] == "test task"
        assert state["context"] == "test context"
        assert state["references"] == ["ref1", "ref2"]
        assert state["task_corrected"] == "corrected task"
        assert state["context_corrected"] == "corrected context"
        assert state["references_corrected"] == ["corrected ref1", "corrected ref2"]
        assert state["final_prompt_corrected"] == "corrected prompt"


if __name__ == "__main__":
    pytest.main([__file__])
