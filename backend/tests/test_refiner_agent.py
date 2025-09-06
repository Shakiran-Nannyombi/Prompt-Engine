"""
Simple pytest tests for the refiner agent.
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
from agents.refiner_agent import (
    refiner_graph,
    RefinerState,
    classify_category,
    handle_conversation,
    process_prompt_refinement,
    generate_analysis
)


class TestRefinerAgent:
    """Test class for refiner agent functionality."""
    
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup method that runs before each test."""
        # Verify required environment variables are set
        required_vars = [
            "GROQ_API_KEY",
            "REFINER_LANGSMITH_API_KEY",
            "REFINER_LANGSMITH_PROJECT", 
            "DATABASE_URL"
        ]
        
        missing_vars = [var for var in required_vars if not os.environ.get(var)]
        if missing_vars:
            pytest.skip(f"Missing required environment variables: {missing_vars}")
    
    def test_environment_variables_loaded(self):
        """Test that all required environment variables are loaded."""
        assert os.environ.get("GROQ_API_KEY") is not None
        assert os.environ.get("REFINER_LANGSMITH_API_KEY") is not None
        assert os.environ.get("REFINER_LANGSMITH_PROJECT") is not None
        assert os.environ.get("DATABASE_URL") is not None
    
    def test_refiner_graph_initialization(self):
        """Test that the refiner graph initializes without errors."""
        assert refiner_graph is not None
        assert hasattr(refiner_graph, 'nodes')
        assert hasattr(refiner_graph, 'edges')
    
    def test_classify_category_greeting(self):
        """Test category classification for greeting messages."""
        state = {
            "messages": [("human", "Hello! How are you?")],
            "original_prompt": "",
            "refined_prompt": "",
            "prompt_category": "",
            "framework_used": "",
            "has_document": False
        }
        
        result = classify_category(state)
        
        assert result["prompt_category"] == "greeting"
        assert result["original_prompt"] == "Hello! How are you?"
        assert result["has_document"] == False
    
    def test_classify_category_help_request(self):
        """Test category classification for help requests."""
        state = {
            "messages": [("human", "Can you help me understand the C.O.R.E. framework?")],
            "original_prompt": "",
            "refined_prompt": "",
            "prompt_category": "",
            "framework_used": "",
            "has_document": False
        }
        
        result = classify_category(state)
        
        assert result["prompt_category"] == "help_request"
        assert result["original_prompt"] == "Can you help me understand the C.O.R.E. framework?"
        assert result["has_document"] == False
    
    def test_classify_category_clarity_prompt(self):
        """Test category classification for clarity prompts."""
        state = {
            "messages": [("human", "Write a prompt that helps me organize my thoughts better")],
            "original_prompt": "",
            "refined_prompt": "",
            "prompt_category": "",
            "framework_used": "",
            "has_document": False
        }
        
        result = classify_category(state)
        
        assert result["prompt_category"] == "clarity"
        assert result["original_prompt"] == "Write a prompt that helps me organize my thoughts better"
        assert result["has_document"] == False
    
    def test_classify_category_precision_prompt(self):
        """Test category classification for precision prompts."""
        state = {
            "messages": [("human", "Create a technical prompt with specific parameters and constraints")],
            "original_prompt": "",
            "refined_prompt": "",
            "prompt_category": "",
            "framework_used": "",
            "has_document": False
        }
        
        result = classify_category(state)
        
        assert result["prompt_category"] == "precision"
        assert result["original_prompt"] == "Create a technical prompt with specific parameters and constraints"
        assert result["has_document"] == False
    
    def test_classify_category_creative_prompt(self):
        """Test category classification for creative prompts."""
        state = {
            "messages": [("human", "Design a creative and engaging prompt for storytelling")],
            "original_prompt": "",
            "refined_prompt": "",
            "prompt_category": "",
            "framework_used": "",
            "has_document": False
        }
        
        result = classify_category(state)
        
        assert result["prompt_category"] == "creative"
        assert result["original_prompt"] == "Design a creative and engaging prompt for storytelling"
        assert result["has_document"] == False
    
    def test_handle_conversation_greeting(self):
        """Test conversation handling for greeting messages."""
        state = {
            "messages": [("human", "Hello!")],
            "original_prompt": "Hello!",
            "refined_prompt": "",
            "prompt_category": "greeting",
            "framework_used": "",
            "has_document": False
        }
        
        result = handle_conversation(state)
        
        assert "messages" in result
        assert len(result["messages"]) > 1  # Should have greeting + response
        # Should end the conversation
        assert result.get("__end__") == True
    
    def test_handle_conversation_help_request(self):
        """Test conversation handling for help requests."""
        state = {
            "messages": [("human", "What frameworks do you support?")],
            "original_prompt": "What frameworks do you support?",
            "refined_prompt": "",
            "prompt_category": "help_request",
            "framework_used": "",
            "has_document": False
        }
        
        result = handle_conversation(state)
        
        assert "messages" in result
        assert len(result["messages"]) > 1  # Should have question + response
        # Should end the conversation
        assert result.get("__end__") == True
    
    @patch('agents.refiner_agent.llm')
    def test_process_prompt_refinement_clarity(self, mock_llm):
        """Test prompt refinement for clarity category."""
        # Mock the LLM response for refinement
        mock_response = MagicMock()
        mock_response.content = "Here's a refined prompt with better structure..."
        mock_llm.invoke.return_value = mock_response
        
        state = {
            "messages": [("human", "Write a prompt that helps me organize my thoughts better")],
            "original_prompt": "Write a prompt that helps me organize my thoughts better",
            "refined_prompt": "",
            "prompt_category": "clarity",
            "framework_used": "",
            "has_document": False
        }
        
        result = process_prompt_refinement(state)
        
        assert "messages" in result
        assert "refined_prompt" in result
        assert "framework_used" in result
        mock_llm.invoke.assert_called()
    
    @patch('agents.refiner_agent.llm')
    def test_process_prompt_refinement_with_document(self, mock_llm):
        """Test prompt refinement with document processing (RAG)."""
        # Mock the LLM response for refinement
        mock_response = MagicMock()
        mock_response.content = "Here's a refined prompt using document context..."
        mock_llm.invoke.return_value = mock_response
        
        state = {
            "messages": [("human", "Refine this prompt using the uploaded document")],
            "original_prompt": "Refine this prompt using the uploaded document",
            "refined_prompt": "",
            "prompt_category": "clarity",
            "framework_used": "",
            "has_document": True  # RAG processing enabled
        }
        
        result = process_prompt_refinement(state)
        
        assert "messages" in result
        assert "refined_prompt" in result
        assert "framework_used" in result
        # Should have RAG tools available when has_document is True
        mock_llm.invoke.assert_called()
    
    def test_refiner_state_structure(self):
        """Test that RefinerState has the expected structure."""
        state = RefinerState(
            original_prompt="test prompt",
            refined_prompt="refined prompt",
            prompt_category="clarity",
            framework_used="C.O.R.E.",
            has_document=False,
            messages=[]
        )
        
        assert state["original_prompt"] == "test prompt"
        assert state["refined_prompt"] == "refined prompt"
        assert state["prompt_category"] == "clarity"
        assert state["framework_used"] == "C.O.R.E."
        assert state["has_document"] == False
        assert state["messages"] == []
    
    def test_prompt_categories_enum(self):
        """Test that prompt categories are properly defined."""
        valid_categories = ["clarity", "precision", "creative", "greeting", "help_request"]
        
        for category in valid_categories:
            state = {
                "messages": [("human", f"Test {category} message")],
                "original_prompt": "",
                "refined_prompt": "",
                "prompt_category": "",
                "framework_used": "",
                "has_document": False
            }
            
            result = classify_category(state)
            assert result["prompt_category"] in valid_categories
    
    @patch('agents.refiner_agent.llm')
    def test_generate_analysis(self, mock_llm):
        """Test the generate_analysis function."""
        # Mock the LLM response for analysis
        mock_response = MagicMock()
        mock_response.content = "Analysis: This prompt was refined using the C.O.R.E. framework..."
        mock_llm.invoke.return_value = mock_response
        
        state = {
            "messages": [("human", "Test prompt"), ("ai", "Refined prompt")],
            "original_prompt": "Test prompt",
            "refined_prompt": "Refined prompt",
            "prompt_category": "clarity",
            "framework_used": "C.O.R.E.",
            "has_document": False
        }
        
        result = generate_analysis(state)
        
        assert "messages" in result
        assert len(result["messages"]) > 2  # Should have original + refined + analysis
        mock_llm.invoke.assert_called()


if __name__ == "__main__":
    pytest.main([__file__])