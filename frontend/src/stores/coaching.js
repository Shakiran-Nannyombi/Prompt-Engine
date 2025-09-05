import { defineStore } from 'pinia';
import { coachingAPI, extractMessages, getLatestMessage, getRefinedPrompt } from '@/service/api';

export const useCoachingStore = defineStore('coaching', {
  state: () => ({
    messages: [],
    loading: false,
    error: null,
    currentStep: 'start',
    refinedPrompt: null,
    threadId: null,
  }),

  getters: {
    lastMessage: (state) => {
      return state.messages.length > 0 ? state.messages[state.messages.length - 1] : null;
    },
    
    userMessages: (state) => {
      return state.messages.filter(msg => msg.role === 'human');
    },
    
    assistantMessages: (state) => {
      return state.messages.filter(msg => msg.role === 'assistant');
    }
  },

  actions: {
    async sendMessage(userInput) {
      this.loading = true;
      this.error = null;
      
      // Add user message to conversation
      this.messages.push({
        role: 'human',
        content: userInput,
        timestamp: new Date().toISOString()
      });

      try {
        // Pass threadId to API
        const response = await coachingAPI.sendMessage(
          userInput, 
          this.messages, 
          this.threadId
        );
        
        // Extract data from response
        const latestMessage = getLatestMessage(response);
        const conversationHistory = extractMessages(response);
        const refinedPrompt = getRefinedPrompt(response);
        
        // Add assistant message
        if (latestMessage) {
          this.messages.push({
            role: 'assistant',
            content: latestMessage,
            timestamp: new Date().toISOString()
          });
        }
        
        // Update conversation history if provided
        if (conversationHistory.length > 0) {
          this.messages = conversationHistory.map(msg => ({
            role: msg.role === 'user' ? 'human' : 'assistant',
            content: msg.content,
            timestamp: msg.timestamp || new Date().toISOString()
          }));
        }
        
        // Update refined prompt if available
        if (refinedPrompt) {
          this.refinedPrompt = refinedPrompt;
        }
        
        return response;
        
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'An error occurred';
        console.error('Coaching API Error:', err);
      } finally {
        this.loading = false;
      }
    },

    async createNewSession() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await coachingAPI.createNewThread();
        this.threadId = response.data.thread_id; // thread_id from backend
        this.clearConversation();
        return response;
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Failed to create new session';
      } finally {
        this.loading = false;
      }
    },

    clearConversation() {
      this.messages = [];
      this.refinedPrompt = null;
      this.currentStep = 'start';
      this.error = null;
    },

    updateStep(step) {
      this.currentStep = step;
    },

    clearError() {
      this.error = null;
    }
  }
});