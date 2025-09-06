<template>
  <div class="chat-interface flex flex-col h-full bg-background">
    <!-- Chat Header (Optional) -->
    <div v-if="showHeader || $slots.header" class="chat-header border-b border-card-border bg-card-bg">
      <slot name="header">
        <div class="p-4">
          <h2 class="text-lg font-semibold text-text">{{ title }}</h2>
          <p v-if="subtitle" class="text-sm text-text opacity-70 mt-1">{{ subtitle }}</p>
        </div>
      </slot>
    </div>

    <!-- Messages Container -->
    <div class="chat-messages flex-1 overflow-hidden">
      <ChatMessageList 
        :messages="messages"
        :isLoading="isLoading"
        :loadingMessage="loadingMessage"
        :variant="variant"
        @scroll-to-bottom="handleScrollToBottom"
      />
    </div>

    <!-- Input Area -->
    <div class="chat-input border-t border-card-border bg-card-bg">
      <ChatInput
        :disabled="isLoading"
        :placeholder="inputPlaceholder"
        :showStopButton="showStopButton"
        :variant="variant"
        @send-message="handleSendMessage"
        @stop-generation="handleStopGeneration"
      />
    </div>

    <!-- Error Display -->
    <div v-if="error" class="chat-error border-t border-error bg-error-50">
      <div class="p-3 flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <svg class="w-4 h-4 text-error" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
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
import ChatInput from './ChatInput.vue'

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
  min-height: 0; /* Important for flexbox */
}

.chat-header {
  flex-shrink: 0;
}

.chat-messages {
  flex: 1;
  min-height: 0; /* Important for flexbox */
}

.chat-input {
  flex-shrink: 0;
}

.chat-error {
  flex-shrink: 0;
}

.chat-footer {
  flex-shrink: 0;
}
</style>