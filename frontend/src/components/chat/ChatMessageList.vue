<template>
  <div 
    ref="messagesContainer"
    class="chat-message-list h-full overflow-y-auto p-4 space-y-4"
    @scroll="handleScroll"
  >
    <!-- Empty State -->
    <div v-if="messages.length === 0 && !isLoading" class="flex flex-col items-center justify-center h-full text-center">
      <div class="w-16 h-16 bg-secondary rounded-full flex items-center justify-center mb-4">
        <svg class="w-8 h-8 text-text opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
      </div>
      <h3 class="text-lg font-medium text-text mb-2">Start a conversation</h3>
      <p class="text-text opacity-70 max-w-md">
        {{ emptyStateMessage }}
      </p>
    </div>

    <!-- Messages -->
    <div v-else class="space-y-4">
      <ChatMessage
        v-for="(message, index) in messages"
        :key="message.id || index"
        :message="message"
        :variant="variant"
        :showTimestamp="showTimestamps"
        :enableMarkdown="enableMarkdown"
        @copy-message="handleCopyMessage"
        @regenerate-message="handleRegenerateMessage"
      />
    </div>

    <!-- Loading Indicator -->
    <div v-if="isLoading" class="flex justify-start">
      <div class="bg-card-bg border border-card-border rounded-lg px-4 py-3 max-w-xs">
        <div class="flex items-center space-x-3">
          <BaseSpinner 
            :variant="variant === 'coach' ? 'dots' : 'logo'"
            :size="'small'"
            :color="variant === 'coach' ? 'primary' : 'accent'"
          />
          <span class="text-sm text-text opacity-70">{{ loadingMessage }}</span>
        </div>
      </div>
    </div>

    <!-- Scroll to Bottom Button -->
    <Transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="opacity-0 transform scale-95"
      enter-to-class="opacity-100 transform scale-100"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100 transform scale-100"
      leave-to-class="opacity-0 transform scale-95"
    >
      <button
        v-if="showScrollButton"
        @click="scrollToBottom"
        class="fixed bottom-20 right-6 bg-primary text-white p-3 rounded-full shadow-lg hover:bg-primary-600 transition-all duration-200 z-10"
        :title="'Scroll to bottom'"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
        </svg>
      </button>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue'
import ChatMessage from './ChatMessage.vue'
import { BaseSpinner } from '@/components/base'

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
  variant: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'coach', 'refiner'].includes(value)
  },
  showTimestamps: {
    type: Boolean,
    default: true
  },
  enableMarkdown: {
    type: Boolean,
    default: true
  },
  autoScroll: {
    type: Boolean,
    default: true
  },
  emptyStateMessage: {
    type: String,
    default: 'Send a message to get started!'
  }
})

const emit = defineEmits(['scroll-to-bottom', 'copy-message', 'regenerate-message'])

const messagesContainer = ref(null)
const showScrollButton = ref(false)
const isNearBottom = ref(true)

const handleScroll = () => {
  if (!messagesContainer.value) return
  
  const { scrollTop, scrollHeight, clientHeight } = messagesContainer.value
  const distanceFromBottom = scrollHeight - scrollTop - clientHeight
  
  // Show scroll button if not near bottom
  showScrollButton.value = distanceFromBottom > 100
  isNearBottom.value = distanceFromBottom < 50
}

const scrollToBottom = (smooth = true) => {
  if (!messagesContainer.value) return
  
  messagesContainer.value.scrollTo({
    top: messagesContainer.value.scrollHeight,
    behavior: smooth ? 'smooth' : 'auto'
  })
  
  emit('scroll-to-bottom')
}

const handleCopyMessage = (message) => {
  emit('copy-message', message)
}

const handleRegenerateMessage = (message) => {
  emit('regenerate-message', message)
}

// Auto-scroll when new messages are added
watch(() => props.messages.length, () => {
  if (props.autoScroll && isNearBottom.value) {
    nextTick(() => {
      scrollToBottom(false)
    })
  }
})

// Auto-scroll when loading state changes
watch(() => props.isLoading, (newLoading, oldLoading) => {
  if (newLoading && !oldLoading && props.autoScroll) {
    nextTick(() => {
      scrollToBottom(false)
    })
  }
})

// Scroll to bottom on mount
onMounted(() => {
  nextTick(() => {
    scrollToBottom(false)
  })
})

// Handle keyboard shortcuts
const handleKeydown = (event) => {
  // Ctrl/Cmd + End to scroll to bottom
  if ((event.ctrlKey || event.metaKey) && event.key === 'End') {
    event.preventDefault()
    scrollToBottom()
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})

// Expose methods for parent components
defineExpose({
  scrollToBottom,
  scrollToTop: () => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }
})
</script>

<style scoped>
.chat-message-list {
  scroll-behavior: smooth;
}

/* Custom scrollbar */
.chat-message-list::-webkit-scrollbar {
  width: 6px;
}

.chat-message-list::-webkit-scrollbar-track {
  background: var(--color-scrollbar-track);
  border-radius: 3px;
}

.chat-message-list::-webkit-scrollbar-thumb {
  background: var(--color-scrollbar-thumb);
  border-radius: 3px;
}

.chat-message-list::-webkit-scrollbar-thumb:hover {
  background: var(--color-accent);
}

/* Smooth transitions for new messages */
.chat-message-list > div > div {
  animation: fadeInUp 0.3s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
