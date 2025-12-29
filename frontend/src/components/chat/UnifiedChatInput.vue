<template>
  <div 
    class="relative w-full max-w-2xl mx-auto transition-all duration-300 font-sans"
    @dragover.prevent="onDragOver"
    @dragleave.prevent="onDragLeave"
    @drop.prevent="onDrop"
  >
    <!-- Main Container -->
    <div class="!box-content flex flex-col mx-2 md:mx-0 items-stretch transition-all duration-200 relative z-10 rounded-2xl cursor-text border border-card-border shadow-sm hover:shadow-md focus-within:shadow-lg bg-card-bg font-sans antialiased">
      <div class="flex flex-col px-3 pt-3 pb-2 gap-2">
        
        <!-- Artifacts (Files & Pastes) -->
        <div v-if="files.length > 0 || pastedContent.length > 0" class="flex gap-3 overflow-x-auto custom-scrollbar pb-2 px-1">
          <PastedContentCard
            v-for="content in pastedContent"
            :key="content.id"
            :content="content"
            @remove="removePastedContent"
          />
          <FilePreviewCard
            v-for="file in files"
            :key="file.id"
            :file="file"
            @remove="removeFile"
          />
        </div>

        <!-- Input Area -->
        <div class="relative mb-1">
          <div class="max-h-96 w-full overflow-y-auto custom-scrollbar font-sans break-words transition-opacity duration-200 min-h-[2.5rem] pl-1">
            <textarea
              ref="textareaRef"
              v-model="message"
              @input="handleInput"
              @paste="handlePaste"
              @keydown="handleKeyDown"
              placeholder="How can I help you today?"
              class="w-full bg-transparent border-0 outline-none text-text text-[16px] placeholder:text-text/40 resize-none overflow-hidden py-0 leading-relaxed block font-normal antialiased"
              rows="1"
              autofocus
              style="min-height: 1.5em; height: auto;"
            ></textarea>
          </div>
        </div>

        <!-- Action Bar -->
        <div class="flex gap-2 w-full items-center">
          <!-- Left Tools -->
          <div class="relative flex-1 flex items-center shrink min-w-0 gap-1">
            <!-- Attach Button -->
            <button
              @click="triggerFileUpload"
              class="inline-flex items-center justify-center relative shrink-0 transition-colors duration-200 h-8 w-8 rounded-lg active:scale-95 text-text opacity-50 hover:opacity-100 hover:bg-secondary"
              type="button"
              aria-label="Attach file"
            >
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
              </svg>
            </button>

            <!-- Thinking Mode Button -->
            <div class="flex shrink min-w-8 !shrink-0 group relative">
              <button
                @click="isThinkingEnabled = !isThinkingEnabled"
                class="transition-all duration-200 h-8 w-8 flex items-center justify-center rounded-lg active:scale-95"
                :class="isThinkingEnabled ? 'text-primary bg-primary/10' : 'text-text opacity-50 hover:opacity-100 hover:bg-secondary'"
              >
                <!-- Brain/Thinking Icon -->
                <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </button>
              
              <!-- Tooltip -->
              <div class="absolute top-full left-1/2 -translate-x-1/2 mt-2 px-2 py-1 bg-card-bg border border-card-border text-text text-[11px] font-medium rounded-[6px] opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none z-50 flex items-center gap-1 shadow-sm tracking-wide">
                <span>Extended thinking</span>
              </div>
            </div>
          </div>

          <!-- Right Tools -->
          <div class="flex flex-row items-center min-w-0 gap-1">
            <button
              @click="handleSend"
              :disabled="!hasContent"
              class="inline-flex items-center justify-center relative shrink-0 transition-all h-8 w-8 rounded-xl"
              :class="hasContent ? 'bg-primary text-white hover:bg-primary-600 shadow-md transform hover:translate-y-[-1px]' : 'bg-secondary text-text opacity-40 cursor-default'"
            >
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 10l7-7m0 0l7 7m-7-7v18" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Drag Overlay -->
    <div 
      v-if="isDragging" 
      class="absolute inset-0 bg-card-bg/90 border-2 border-dashed border-primary rounded-2xl z-50 flex flex-col items-center justify-center backdrop-blur-sm pointer-events-none"
    >
      <svg class="w-10 h-10 text-primary mb-2 animate-bounce" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
      </svg>
      <p class="text-primary font-medium">Drop files to upload</p>
    </div>

    <!-- Hidden File Input -->
    <input
      ref="fileInputRef"
      type="file"
      multiple
      class="hidden"
      @change="handleFileSelect"
    />

    <div class="text-center mt-4">
      <p class="text-xs text-text opacity-50">
        AI can make mistakes. Please check important information.
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, shallowRef } from 'vue'
import FilePreviewCard from './input/FilePreviewCard.vue'
import PastedContentCard from './input/PastedContentCard.vue'
import ModelSelector from './input/ModelSelector.vue'

const emit = defineEmits(['send-message', 'file-upload', 'update:model'])

// State
const message = ref('')
const files = ref([])
const pastedContent = ref([])
const isDragging = ref(false)
const selectedModel = ref('sonnet-4.5')
const isThinkingEnabled = ref(false)
const textareaRef = ref(null)
const fileInputRef = ref(null)

const models = [
  { id: 'opus-4.5', name: 'Opus 4.5', description: 'Most capable for complex work', badge: 'Upgrade' },
  { id: 'sonnet-4.5', name: 'Sonnet 4.5', description: 'Best for everyday tasks' },
  { id: 'haiku-4.5', name: 'Haiku 4.5', description: 'Fastest for quick answers' }
]

const hasContent = computed(() => {
  return message.value.trim().length > 0 || files.value.length > 0 || pastedContent.value.length > 0
})

// Handlers
const handleInput = () => {
  adjustTextareaHeight()
}

const adjustTextareaHeight = () => {
  nextTick(() => {
    if (textareaRef.value) {
      textareaRef.value.style.height = 'auto'
      textareaRef.value.style.height = Math.min(textareaRef.value.scrollHeight, 384) + 'px'
    }
  })
}

const handleKeyDown = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    handleSend()
  }
}

const handleSend = () => {
  if (!hasContent.value) return

  emit('send-message', {
    message: message.value,
    files: files.value,
    pastedContent: pastedContent.value,
    model: selectedModel.value,
    isThinkingEnabled: isThinkingEnabled.value
  })

  // clear state
  message.value = ''
  files.value = []
  pastedContent.value = []
  adjustTextareaHeight()
}

// File Handling
const triggerFileUpload = () => {
  fileInputRef.value.click()
}

const handleFileSelect = (e) => {
  if (e.target.files) {
    processFiles(e.target.files)
  }
  e.target.value = ''
}

const processFiles = (fileList) => {
  const newFiles = Array.from(fileList).map(file => {
    const isImage = file.type.startsWith('image/') || /\.(jpg|jpeg|png|gif|webp|svg)$/i.test(file.name)
    return {
      id: Math.random().toString(36).substr(2, 9),
      file,
      type: isImage ? 'image/unknown' : (file.type || 'application/octet-stream'),
      preview: isImage ? URL.createObjectURL(file) : null,
      uploadStatus: 'complete' // Simulating instant upload completion for now
    }
  })
  files.value = [...files.value, ...newFiles]
}

const removeFile = (id) => {
  files.value = files.value.filter(f => f.id !== id)
}

// Paste Handling
const handlePaste = (e) => {
  const items = e.clipboardData.items
  const pastedFiles = []
  
  for (let i = 0; i < items.length; i++) {
    if (items[i].kind === 'file') {
      const file = items[i].getAsFile()
      if (file) pastedFiles.push(file)
    }
  }

  if (pastedFiles.length > 0) {
    e.preventDefault()
    processFiles(pastedFiles)
    return
  }

  // Handle large text paste
  const text = e.clipboardData.getData('text')
  if (text.length > 500) { // arbitrary threshold for "large" text
    e.preventDefault()
    const snippet = {
      id: Math.random().toString(36).substr(2, 9),
      content: text,
      timestamp: new Date()
    }
    pastedContent.value.push(snippet)
  }
}

const removePastedContent = (id) => {
  pastedContent.value = pastedContent.value.filter(c => c.id !== id)
}

// Drag & Drop
const onDragOver = (e) => {
  isDragging.value = true
}

const onDragLeave = (e) => {
  isDragging.value = false
}

const onDrop = (e) => {
  isDragging.value = false
  if (e.dataTransfer.files) {
    processFiles(e.dataTransfer.files)
  }
}
</script>

<style scoped>
/* Custom Scrollbar */
.custom-scrollbar::-webkit-scrollbar {
  height: 6px;
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: var(--color-scrollbar-thumb);
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: var(--color-accent);
}
</style>
