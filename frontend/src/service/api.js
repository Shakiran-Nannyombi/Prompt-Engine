import axios from "axios";

const API_BASE_URL = "http://localhost:8000/api";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000
});

export const coachingAPI = {
  sendMessage(userInput, conversationHistory) {
    return apiClient.post("/coaching/chat/", {
      user_input: userInput,
      conversation_history: conversationHistory
    });
  },

  createNewThread() {
    return apiClient.post("/coaching/threads/");
  }
};

export const refinerAPI = {
  sendMessage(prompt, conversationHistory) {
    return apiClient.post("/refiner/refine_chat/", {
      prompt: prompt,
      conversation_history: conversationHistory
    });
  },

  createNewThread() {
    return apiClient.post("/refiner/threads/");
  }
};

export default apiClient;
