<template>
  <div class="chat-input-container p-4">
    <div class="flex items-end space-x-3">
      <!-- Text Input Area -->
      <div class="flex-1 relative">
        <textarea
          ref="textareaRef"
          v-model="inputText"
          :placeholder="placeholder"
          :disabled="disabled"
          :rows="textareaRows"
          class="chat-textarea w-full resize-none rounded-lg border border-input-border bg-input-bg text-text placeholder-text placeholder-opacity-50 focus:border-primary focus:ring-2 focus:ring-primary-500 focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
          @keydown="handleKeydown"
          @input="handleInput"
          @paste="handlePaste"
        ></textarea>
        
        <!-- Character Count -->
        <div v-if="showCharacterCount" class="absolute bottom-2 right-2 text-xs text-text opacity-50">
          {{ inputText.length }}/{{ maxLength }}
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-col space-y-2">
        <!-- Send Button -->
        <BaseButton
          type="primary"
          size="medium"
          :disabled="!canSend"
          :isLoading="isLoading"
          @click="handleSend"
        >
          <template v-if="!isLoading">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </template>
        </BaseButton>

        <!-- Stop Button (when generating) -->
        <BaseButton
          v-if="showStopButton"
          type="outline"
          size="small"
          @click="handleStop"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 10h6v4H9z" />
          </svg>
        </BaseButton>
      </div>
    </div>

    <!-- Additional Actions Row -->
    <div v-if="showAdditionalActions" class="flex items-center justify-between mt-3 pt-3 border-t border-card-border">
      <!-- Left Actions -->
      <div class="flex items-center space-x-2">
        <!-- File Upload -->
        <button
          v-if="allowFileUpload"
          @click="handleFileUpload"
          class="p-2 text-text hover:text-primary hover:bg-secondary rounded-lg transition-colors"
          title="Upload file"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
          </svg>
        </button>

        <!-- Voice Input -->
        <button
          v-if="allowVoiceInput"
          @click="handleVoiceInput"
          class="p-2 text-text hover:text-primary hover:bg-secondary rounded-lg transition-colors"
          :class="{ 'bg-primary text-white': isRecording }"
          title="Voice input"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
          </svg>
        </button>

        <!-- Clear Input -->
        <button
          v-if="inputText && !disabled"
          @click="clearInput"
          class="p-2 text-text hover:text-primary hover:bg-secondary rounded-lg transition-colors"
          title="Clear input"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Right Actions -->
      <div class="flex items-center space-x-2">
        <!-- Keyboard Shortcuts Info -->
        <button
          @click="showShortcuts = !showShortcuts"
          class="text-xs text-text opacity-50 hover:opacity-100 transition-opacity"
          title="Keyboard shortcuts"
        >
          ⌘K
        </button>
      </div>
    </div>

    <!-- Keyboard Shortcuts Modal -->
    <BaseModal
      v-model:isOpen="showShortcuts"
      title="Keyboard Shortcuts"
      size="small"
    >
      <div class="space-y-3 text-sm">
        <div class="flex justify-between">
          <span>Send message</span>
          <kbd class="px-2 py-1 bg-secondary rounded text-xs">Enter</kbd>
        </div>
        <div class="flex justify-between">
          <span>New line</span>
          <kbd class="px-2 py-1 bg-secondary rounded text-xs">Shift + Enter</kbd>
        </div>
        <div class="flex justify-between">
          <span>Clear input</span>
          <kbd class="px-2 py-1 bg-secondary rounded text-xs">Esc</kbd>
        </div>
        <div class="flex justify-between">
          <span>Focus input</span>
          <kbd class="px-2 py-1 bg-secondary rounded text-xs">⌘K</kbd>
        </div>
      </div>
    </BaseModal>

    <!-- File Upload Input (Hidden) -->
    <input
      ref="fileInputRef"
      type="file"
      class="hidden"
      :accept="acceptedFileTypes"
      @change="handleFileSelect"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue'
import { BaseButton, BaseModal } from '@/components/base'

const props = defineProps({
  placeholder: {
    type: String,
    default: 'Type your message...'
  },
  disabled: {
    type: Boolean,
    default: false
  },
  isLoading: {
    type: Boolean,
    default: false
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
  maxLength: {
    type: Number,
    default: 4000
  },
  showCharacterCount: {
    type: Boolean,
    default: false
  },
  allowFileUpload: {
    type: Boolean,
    default: false
  },
  allowVoiceInput: {
    type: Boolean,
    default: false
  },
  acceptedFileTypes: {
    type: String,
    default: '.txt,.md,.pdf,.doc,.docx'
  },
  showAdditionalActions: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['send-message', 'stop-generation', 'file-upload', 'voice-input'])

const textareaRef = ref(null)
const fileInputRef = ref(null)
const inputText = ref('')
const showShortcuts = ref(false)
const isRecording = ref(false)

const textareaRows = computed(() => {
  const lines = inputText.value.split('\n').length
  return Math.min(Math.max(lines, 1), 6) // Min 1 row, max 6 rows
})

const canSend = computed(() => {
  return inputText.value.trim().length > 0 && 
         !props.disabled && 
         !props.isLoading &&
         inputText.value.length <= props.maxLength
})

const handleKeydown = (event) => {
  // Send on Enter (but not Shift+Enter)
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    if (canSend.value) {
      handleSend()
    }
  }
  
  // Clear on Escape
  if (event.key === 'Escape') {
    clearInput()
  }
  
  // Focus input with Cmd/Ctrl + K
  if ((event.metaKey || event.ctrlKey) && event.key === 'k') {
    event.preventDefault()
    focusInput()
  }
}

const handleInput = () => {
  // Auto-resize textarea
  nextTick(() => {
    if (textareaRef.value) {
      textareaRef.value.style.height = 'auto'
      textareaRef.value.style.height = textareaRef.value.scrollHeight + 'px'
    }
  })
}

const handlePaste = (event) => {
  // Handle file paste
  const items = event.clipboardData?.items
  if (items && props.allowFileUpload) {
    for (let item of items) {
      if (item.kind === 'file') {
        const file = item.getAsFile()
        if (file) {
          emit('file-upload', file)
        }
      }
    }
  }
}

const handleSend = () => {
  if (!canSend.value) return
  
  const message = inputText.value.trim()
  inputText.value = ''
  
  emit('send-message', message)
  
  // Reset textarea height
  nextTick(() => {
    if (textareaRef.value) {
      textareaRef.value.style.height = 'auto'
    }
  })
}

const handleStop = () => {
  emit('stop-generation')
}

const clearInput = () => {
  inputText.value = ''
  focusInput()
}

const focusInput = () => {
  nextTick(() => {
    textareaRef.value?.focus()
  })
}

const handleFileUpload = () => {
  fileInputRef.value?.click()
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    emit('file-upload', file)
  }
  // Clear the input so the same file can be selected again
  event.target.value = ''
}

const handleVoiceInput = () => {
  if (isRecording.value) {
    // Stop recording
    isRecording.value = false
    // You would implement actual voice recording logic here
  } else {
    // Start recording
    isRecording.value = true
    // You would implement actual voice recording logic here
  }
  
  emit('voice-input', { isRecording: isRecording.value })
}

// Handle keyboard shortcuts globally
const handleGlobalKeydown = (event) => {
  // Focus input with Cmd/Ctrl + K
  if ((event.metaKey || event.ctrlKey) && event.key === 'k') {
    event.preventDefault()
    focusInput()
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleGlobalKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleGlobalKeydown)
})

// Expose methods for parent components
defineExpose({
  focus: focusInput,
  clear: clearInput,
  setValue: (value) => {
    inputText.value = value
  }
})
</script>

<style scoped>
.chat-textarea {
  min-height: 44px; /* Minimum height for touch targets */
  max-height: 200px; /* Maximum height before scrolling */
  line-height: 1.5;
}

/* Custom scrollbar for textarea */
.chat-textarea::-webkit-scrollbar {
  width: 4px;
}

.chat-textarea::-webkit-scrollbar-track {
  background: transparent;
}

.chat-textarea::-webkit-scrollbar-thumb {
  background: var(--color-scrollbar-thumb);
  border-radius: 2px;
}

.chat-textarea::-webkit-scrollbar-thumb:hover {
  background: var(--color-accent);
}

/* Kbd styling */
kbd {
  font-family: ui-monospace, SFMono-Regular, "SF Mono", Consolas, "Liberation Mono", Menlo, monospace;
}
</style>
