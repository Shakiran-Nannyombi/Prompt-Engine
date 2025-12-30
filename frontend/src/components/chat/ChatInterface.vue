<template>
  <div class="chat-interface flex flex-col h-full bg-background">
    <!-- Chat Header (Optional) -->
    <div v-if="showHeader || $slots.header" class="chat-header border-b border-card-border bg-background">
      <slot name="header">
        <div class="p-4">
          <h2 class="text-lg font-semibold text-text">{{ title }}</h2>
          <p v-if="subtitle" class="text-sm text-text opacity-70 mt-1">{{ subtitle }}</p>
        </div>
      </slot>
    </div>

    <!-- Messages Container -->
    <div class="chat-messages flex-1 overflow-hidden relative">
      <div class="max-w-4xl mx-auto h-full w-full px-4 md:px-8">
        <!-- Empty State with Welcome Screen -->
        <div v-if="messages.length === 0 && !isLoading" class="h-full flex items-center justify-center animate-fade-in text-center p-8">
          <div v-if="variant === 'refiner'" class="max-w-md space-y-6">
            <div class="w-16 h-16 mx-auto flex items-center justify-center transform hover:rotate-6 transition-transform duration-500 overflow-hidden">
               <img src="@/assets/images/logo.svg" alt="Prompt Engine" class="w-full h-full object-contain" />
            </div>
            
            <div class="inline-block px-4 py-1.5 rounded-full border border-card-border bg-card-bg/50 backdrop-blur-sm">
              <span class="text-[10px] font-black tracking-widest uppercase text-text">AI Prompt Optimization</span>
            </div> <br><br>

            <div class="space-y-4">
              <h2 class="text-4xl lg:text-5xl font-black text-text tracking-tighter leading-[0.9]">
                Polish Your <br/>Prompts to Gold.
              </h2> <br>
              <p class="text-xs text-text opacity-70 font-bold uppercase tracking-wide leading-relaxed max-w-sm mx-auto">
                Fine-tune, optimize, and structurally enhance your prompt templates for maximum AI performance.
              </p>
              <div class="pt-4 flex items-center justify-center gap-3 text-[10px] font-black text-text opacity-90 uppercase tracking-widest">
                 <span>Structural Clarity</span>
                 <span class="w-1 h-1 rounded-full bg-current"></span>
                 <span>Tone Control</span>
                 <span class="w-1 h-1 rounded-full bg-current"></span>
                 <span>Logic Validation</span>
              </div>
            </div>

            <div class="pt-6">
              <button 
                @click="$emit('start-session')"
                class="px-8 py-4 bg-primary text-text rounded-2xl font-black shadow-lg shadow-primary/20 hover:scale-105 hover:shadow-primary/40 transition-all duration-300 flex items-center justify-center gap-2 mx-auto"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-play"><polygon points="6 3 20 12 6 21 6 3"/></svg>
                Launch Session
              </button>
            </div>
          </div>
          
          <!-- Default Empty State -->
          <div v-else class="flex flex-col items-center justify-center h-full text-center">
            <div class="w-16 h-16 bg-secondary rounded-full flex items-center justify-center mb-4">
              <svg class="w-8 h-8 text-text opacity-70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <h3 class="text-lg font-medium text-text mb-2">Start a conversation</h3>
            <p class="text-text opacity-70 max-w-md">
              {{ inputPlaceholder }}
            </p>
          </div>
        </div>

        <ChatMessageList 
          v-else
          :messages="messages"
          :isLoading="isLoading"
          :loadingMessage="loadingMessage"
          :variant="variant"
          @scroll-to-bottom="handleScrollToBottom"
        />
      </div>
    </div>

    <!-- Input Area -->
    <div class="chat-input p-4 pt-10 bg-gradient-to-t from-background via-background/90 to-transparent">
      <div class="max-w-4xl mx-auto w-full px-4 md:px-8">
        <UnifiedChatInput
          :disabled="isLoading"
          :placeholder="inputPlaceholder"
          @send-message="handleSendMessage"
          @stop-generation="handleStopGeneration"
        />
      </div>
    </div>

    <!-- Error Display -->
    <div v-if="error" class="chat-error border-t border-error bg-error-50">
      <div class="p-3 flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-alert-circle text-error"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12" y1="16" y2="16.01"/></svg>
          <span class="text-sm text-error">{{ error }}</span>
        </div>
        <button
          @click="$emit('clear-error')"
          class="text-error hover:text-error-600 transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Footer Actions (Optional) -->
    <div v-if="$slots.footer" class="chat-footer border-t border-card-border bg-card-bg">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import ChatMessageList from './ChatMessageList.vue'
import UnifiedChatInput from './UnifiedChatInput.vue'
import { useTheme } from '@/composables/useTheme'
import logo from '@/assets/images/logo.svg'

const { isDarkMode } = useTheme()

const props = defineProps({
  messages: {
    type: Array,
    default: () => []
  },
  isLoading: {
    type: Boolean,
    default: false
  },
  loadingMessage: {
    type: String,
    default: 'Thinking...'
  },
  showHeader: {
    type: Boolean,
    default: true
  },
  title: {
    type: String,
    default: 'Chat'
  },
  subtitle: {
    type: String,
    default: ''
  },
  inputPlaceholder: {
    type: String,
    default: 'Type your message...'
  },
  showStopButton: {
    type: Boolean,
    default: false
  },
  variant: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'coach', 'refiner'].includes(value)
  },
  error: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['send-message', 'stop-generation', 'clear-error', 'scroll-to-bottom'])

const handleSendMessage = (message) => {
  emit('send-message', message)
}

const handleStopGeneration = () => {
  emit('stop-generation')
}

const handleScrollToBottom = () => {
  emit('scroll-to-bottom')
}

// Expose methods for parent components
defineExpose({
  scrollToBottom: () => {
    // This will be called by the ChatMessageList component
    nextTick(() => {
      const messagesContainer = document.querySelector('.chat-messages')
      if (messagesContainer) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight
      }
    })
  }
})
</script>

<style scoped>
.chat-interface {
  min-height: 0;
  background-color: var(--color-background);
  color: var(--color-text);
  transition: background-color 0.3s ease, color 0.3s ease;
}

.chat-header {
  flex-shrink: 0;
  background-color: var(--color-background);
  border-color: var(--color-card-border);
}

.chat-messages {
  flex: 1;
  min-height: 0;
  background-color: var(--color-background);
}

.chat-input {
  flex-shrink: 0;
}

.chat-error {
  flex-shrink: 0;
  background-color: var(--color-card-bg);
  border-color: var(--color-primary);
}

.chat-footer {
  flex-shrink: 0;
  background-color: var(--color-card-bg);
  border-color: var(--color-card-border);
}
</style>