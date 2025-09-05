import { defineStore } from 'pinia';
import { refinerAPI, extractMessages, getLatestMessage, getRefinedPrompt,getPromptCategory,getFrameworkUsed,getRefinementAnalysis} from '@/service/api';

export const useRefinerStore = defineStore('refiner', {
  state: () => ({
    messages: [],
    loading: false,
    error: null,
    refinedPrompt: null,
    promptCategory: null,
    frameworkUsed: null,
    refinementAnalysis: null,
    threadId: null,
    hasDocument: false,
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
    },

    isConversational: (state) => {
      return ['greeting', 'help_request'].includes(state.promptCategory);
    },

    isRefineable: (state) => {
      return ['clarity', 'precision', 'creative'].includes(state.promptCategory);
    },

    showAnalysisView: (state) => {
      return state.refinementAnalysis !== null || (state.promptCategory && state.frameworkUsed);
    },

    analysisDetails: (state) => {
      if (!state.refinementAnalysis) return null;
      return {
        category: state.refinementAnalysis.category,
        framework: state.refinementAnalysis.framework_used,
        reasoning: state.refinementAnalysis.reasoning,
        refinedPrompt: state.refinementAnalysis.refined_prompt
      };
    }
  },

  actions: {
    async sendMessage(originalPrompt) {
      this.loading = true;
      this.error = null;
      
      // Add user message to conversation
      this.messages.push({
        role: 'human',
        content: originalPrompt,
        timestamp: new Date().toISOString()
      });

      try {
        const response = await refinerAPI.sendMessage(
          originalPrompt,
          this.messages,
          this.threadId,
          this.hasDocument
        );

        const latestMessage = getLatestMessage(response);
        const conversationHistory = extractMessages(response);
        const refinedPrompt = getRefinedPrompt(response);
        const promptCategory = getPromptCategory(response);
        const frameworkUsed = getFrameworkUsed(response);
        const refinementAnalysis = getRefinementAnalysis(response); 
        
        // Add assistant message
        if (latestMessage) {
          this.messages.push({
            role: 'assistant',
            content: latestMessage,
            timestamp: new Date().toISOString()
          });
        }
        
        // Role mapping for conversation history
        if (conversationHistory.length > 0) {
          this.messages = conversationHistory.map(msg => ({
            role: msg.role === 'user' ? 'human' : 'assistant', 
            timestamp: msg.timestamp || new Date().toISOString()
          }));
        }
        
        this.refinedPrompt = refinedPrompt;
        this.promptCategory = promptCategory;
        this.frameworkUsed = frameworkUsed;
        this.refinementAnalysis = refinementAnalysis;
        
        return response;
        
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'An error occurred';
        console.error('Refiner API Error:', err);
        throw err;
      } finally {
        this.loading = false;
      }
    },

    async createNewSession() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await refinerAPI.createNewThread();
        this.threadId = response.data.thread_id;
        this.clearConversation();
        return response;
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Failed to create new session';
        throw err;
      } finally {
        this.loading = false;
      }
    },

    clearConversation() {
      this.messages = [];
      this.refinedPrompt = null;
      this.promptCategory = null;
      this.frameworkUsed = null;
      this.refinementAnalysis = null;
      this.hasDocument = false;
      this.error = null;
    },

    setHasDocument(hasDoc) {
      this.hasDocument = hasDoc;
    },

    clearError() {
      this.error = null;
    },

    getAnalysisViewData() {
      return {
        category: this.promptCategory,
        framework: this.frameworkUsed,
        analysis: this.refinementAnalysis
      };
    }
  }
});