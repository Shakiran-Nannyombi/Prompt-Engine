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
              class="w-full bg-transparent border-0 outline-none text-text text-[16px] placeholder:text-text/70 resize-none overflow-hidden py-0 leading-relaxed block font-normal antialiased"
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
              class="inline-flex items-center justify-center relative shrink-0 transition-colors duration-200 h-8 w-8 rounded-lg active:scale-95 text-text opacity-70 hover:opacity-100 hover:bg-secondary"
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
                :class="isThinkingEnabled ? 'text-primary bg-primary/10' : 'text-text opacity-70 hover:opacity-100 hover:bg-secondary'"
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
      <p class="text-xs text-text opacity-70">
        AI can make mistakes. Please check important information.
      </p>
    </div>
  </div>
</template>

<script setup>
import { useChatInput } from './input/useChatInput'
import FilePreviewCard from './input/FilePreviewCard.vue'
import PastedContentCard from './input/PastedContentCard.vue'
import './input/input-styles.css'

const emit = defineEmits(['send-message', 'file-upload', 'update:model'])

const {
  message,
  files,
  pastedContent,
  isDragging,
  selectedModel,
  isThinkingEnabled,
  textareaRef,
  fileInputRef,
  hasContent,
  handleInput,
  handleKeyDown,
  handleSend,
  triggerFileUpload,
  handleFileSelect,
  removeFile,
  removePastedContent,
  handlePaste,
  onDragOver,
  onDragLeave,
  onDrop
} = useChatInput(emit)
</script>

<style scoped>
/* Scoped overrides if needed */
</style>
