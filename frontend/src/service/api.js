import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000
});

export const coachingAPI = {
  sendMessage(userInput, conversationHistory = [], threadId = null) {
    return apiClient.post("/coaching/chat", {
      user_input: userInput,              
      conversation_history: conversationHistory,
      thread_id: threadId
    });
  },

  createNewThread() {
    return apiClient.post("/coaching/threads/");
  }
};

export const refinerAPI = {
  sendMessage(originalPrompt, conversationHistory = [], threadId = null, hasDocument = false) {
    return apiClient.post("/refiner/refine_chat", {
      original_prompt: originalPrompt,    
      conversation_history: conversationHistory,
      thread_id: threadId,
      has_document: hasDocument            
    });
  },

  createNewThread() {
    return apiClient.post("/refiner/threads/");
  }
};

// functions to extract data from responses in stores/coaching.js and stores/refiner.js
export const extractMessages = (response) => {
  return response.data.conversation_history || [];
};

export const getLatestMessage = (response) => {
  return response.data.agent_output || '';
};

export const getRefinedPrompt = (response) => {
  return response.data.refined_prompt || null;
};

// Refiner-specific response extractors from stores/refiner.js
export const getPromptCategory = (response) => {
  return response.data.prompt_category || null;
};

export const getFrameworkUsed = (response) => {
  return response.data.framework_used || null;
};

export const getRefinementAnalysis = (response) => {
  return response.data.refinement_analysis || null;
};

export default apiClient;
