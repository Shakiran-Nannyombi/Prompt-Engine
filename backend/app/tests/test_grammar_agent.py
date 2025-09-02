#!/usr/bin/env python3
"""
Simple test for the grammar agent functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.grammar_agent import grammar_graph, extract_message_content
from langchain_core.messages import HumanMessage

def test_grammar_agent_basic():
    """Test basic grammar correction functionality"""
    print("Testing grammar agent...")
    
    # Test input with grammar errors
    test_input = "i want to create a semester palnner"
    
    try:
        # Create initial state with thread_id for checkpointer
        initial_state = {
            "messages": [HumanMessage(content=test_input)],
            "current_step": "awaiting_text"
        }
        
        # Run the graph with thread_id
        result = grammar_graph.invoke(initial_state, config={"configurable": {"thread_id": "test-thread-1"}})
        
        print("✅ Grammar agent test completed successfully!")
        print(f"Input: {test_input}")
        print(f"Corrected text: {result.get('corrected_text', 'N/A')}")
        print(f"Corrections made: {result.get('corrections_made', [])}")
        print(f"Confidence score: {result.get('confidence_score', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Grammar agent test failed: {e}")
        return False

def test_grammar_tool():
    """Test the grammar checker tool directly"""
    print("\nTesting grammar checker tool...")
    
    try:
        from backend.app.agents.tools.coach_tools import check_grammar
        
        test_text = "i want to create a semester palnner"
        result = check_grammar.invoke({"text": test_text})
        
        print("✅ Grammar tool test completed successfully!")
        print(f"Tool result: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Grammar tool test failed: {e}")
        return False

if __name__ == "__main__":
    print("Running grammar agent connectivity tests...\n")
    
    tool_test = test_grammar_tool()
    agent_test = test_grammar_agent_basic()
    
    if tool_test and agent_test:
        print("\n🎉 All tests passed! Grammar agent is properly connected.")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
