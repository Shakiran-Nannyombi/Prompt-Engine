<template>
  <div class="flex h-screen bg-gray-50">
    <!-- Sidebar -->
    <div class="w-80 bg-white border-r border-gray-200 flex flex-col">
      <div class="p-6 border-b border-gray-200">
        <h2 class="text-lg font-semibold text-gray-800 mb-4">Actions</h2>
        <button 
          @click="startNewSession"
          class="w-full px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors mb-4"
        >
          New Session
        </button>

        <!-- Analysis View Button -->
        <button 
          v-if="refiner.showAnalysisView()"
          @click="showAnalysis = !showAnalysis"
          class="w-full px-4 py-2 text-sm font-medium text-blue-600 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors mb-4"
        >
          {{ showAnalysis ? 'Hide' : 'View' }} Analysis
        </button>
      </div>

      <!-- Document Upload Section -->
      <div class="p-6 border-b border-gray-200">
        <h3 class="text-md font-medium text-gray-800 mb-3">Document Upload</h3>
        <p class="text-sm text-gray-600 mb-3">Upload a document to enable Q&A.</p>
        
        <input
          ref="fileInput"
          type="file"
          accept=".txt,.md,.pdf"
          @change="handleFileUpload"
          class="hidden"
        />
        
        <button 
          @click="$refs.fileInput.click()"
          class="w-full px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors border-2 border-dashed border-gray-300 hover:border-gray-400"
        >
          <svg class="w-5 h-5 mx-auto mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
          </svg>
          Choose File
        </button>

        <!-- Uploaded Document Display -->
        <div v-if="uploadedDocument" class="mt-3 p-3 bg-green-50 border border-green-200 rounded-lg">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-green-800">{{ uploadedDocument.name }}</p>
              <p class="text-xs text-green-600">Document loaded successfully</p>
            </div>
            <button 
              @click="clearDocument"
              class="text-green-600 hover:text-green-800"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
        </div>

        <div v-if="uploading" class="mt-3 p-3 bg-blue-50 border border-blue-200 rounded-lg">
          <div class="flex items-center space-x-2">
            <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
            <span class="text-sm text-blue-600">Processing document...</span>
          </div>
        </div>
      </div>

      <!-- Analysis Display -->
      <div v-if="showAnalysis && refiner.refinementAnalysis" class="p-6 flex-1 overflow-y-auto">
        <h3 class="text-md font-medium text-gray-800 mb-3">Refinement Analysis</h3>
        <div class="space-y-3 text-sm">
          <div>
            <span class="font-medium text-gray-700">Category:</span>
            <span class="ml-2 px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">
              {{ refiner.promptCategory }}
            </span>
          </div>
          <div>
            <span class="font-medium text-gray-700">Framework:</span>
            <span class="ml-2 px-2 py-1 bg-green-100 text-green-800 rounded text-xs">
              {{ refiner.frameworkUsed }}
            </span>
          </div>
          <div>
            <span class="font-medium text-gray-700">Reasoning:</span>
            <p class="text-gray-600 mt-1">{{ refiner.refinementAnalysis.reasoning }}</p>
          </div>
          <div v-if="refiner.refinedPrompt">
            <span class="font-medium text-gray-700">Refined Prompt:</span>
            <div class="mt-2 p-3 bg-gray-50 rounded border">
              <p class="text-gray-800 text-sm">{{ refiner.refinedPrompt }}</p>
              <button 
                @click="copyPrompt"
                class="mt-2 text-xs text-blue-600 hover:text-blue-800"
              >
                Copy to clipboard
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Chat Area -->
    <div class="flex-1 flex flex-col">
      <!-- Header -->
      <div class="bg-white border-b border-gray-200 p-6">
        <h1 class="text-2xl font-bold text-gray-800">Prompt Refiner Agent</h1>
        <p class="text-gray-600 text-sm mt-1">Enter a prompt to refine, or ask a question about an uploaded document.</p>
      </div>

      <!-- Messages Container -->
      <div class="flex-1 overflow-y-auto p-6 space-y-4">
        <div
          v-for="(message, index) in refiner.messages"
          :key="index"
          class="flex"
          :class="message.role === 'human' ? 'justify-end' : 'justify-start'"
        >
          <div
            class="max-w-3xl rounded-lg px-4 py-3"
            :class="message.role === 'human' 
              ? 'bg-purple-500 text-white' 
              : 'bg-white border border-gray-200 text-gray-800'"
          >
            <div class="text-sm whitespace-pre-wrap">{{ message.content }}</div>
            <div class="text-xs mt-2 opacity-70">
              {{ formatTime(message.timestamp) }}
            </div>
          </div>
        </div>

        <!-- Loading Indicator -->
        <div v-if="refiner.loading" class="flex justify-start">
          <div class="bg-white border border-gray-200 rounded-lg px-4 py-3">
            <div class="flex items-center space-x-2">
              <div class="flex space-x-1">
                <div class="w-2 h-2 bg-purple-400 rounded-full animate-bounce"></div>
                <div class="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                <div class="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
              </div>
              <span class="text-sm text-gray-500">Thinking...</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="bg-white border-t border-gray-200 p-6">
        <div class="flex space-x-4">
          <input
            v-model="currentInput"
            @keyup.enter="sendMessage"
            :disabled="refiner.loading"
            placeholder="Enter your prompt or question..."
            class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent disabled:bg-gray-100"
          />
          <button
            @click="sendMessage"
            :disabled="refiner.loading || !currentInput.trim()"
            class="px-6 py-3 bg-purple-500 text-white rounded-lg hover:bg-purple-600 focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Send
          </button>
        </div>

        <!-- Error Display -->
        <div v-if="refiner.error" class="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p class="text-sm text-red-600">{{ refiner.error }}</p>
          <button 
            @click="refiner.clearError()"
            class="text-xs text-red-500 hover:text-red-700 mt-1"
          >
            Dismiss
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import { useRefinerStore } from '@/stores/refiner'

// Store
const refiner = useRefinerStore()

// Reactive state
const currentInput = ref('')
const uploadedDocument = ref(null)
const uploading = ref(false)
const showAnalysis = ref(false)

// Methods
const sendMessage = async () => {
  if (!currentInput.value.trim() || refiner.loading) return
  
  const message = currentInput.value.trim()
  currentInput.value = ''
  
  try {
    await refiner.sendMessage(message)
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('Error sending message:', error)
  }
}

const startNewSession = async () => {
  if (confirm('Start a new session? This will clear your current conversation.')) {
    refiner.clearConversation()
    uploadedDocument.value = null
    showAnalysis.value = false
    await refiner.createNewSession()
  }
}

const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  const validTypes = ['text/plain', 'text/markdown', 'application/pdf']
  const validExtensions = ['.txt', '.md', '.pdf']
  
  if (!validTypes.includes(file.type) && !validExtensions.some(ext => file.name.toLowerCase().endsWith(ext))) {
    alert('Please select a .txt, .md, or .pdf file')
    return
  }

  uploading.value = true
  
  try {
    // Simulate document processing (in real app, you'd send to backend)
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    uploadedDocument.value = {
      name: file.name,
      size: file.size,
      type: file.type
    }
    
    // Set has_document flag in refiner store
    refiner.setHasDocument(true)
    
    // Clear the file input
    event.target.value = ''
    
  } catch (error) {
    console.error('Error processing document:', error)
    alert('Error processing document. Please try again.')
  } finally {
    uploading.value = false
  }
}

const clearDocument = () => {
  uploadedDocument.value = null
  refiner.setHasDocument(false)
}

const copyPrompt = async () => {
  if (!refiner.refinedPrompt) return
  
  try {
    await navigator.clipboard.writeText(refiner.refinedPrompt)
    // You could add a toast notification here
    console.log('Prompt copied to clipboard!')
  } catch (error) {
    console.error('Failed to copy prompt:', error)
  }
}

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const scrollToBottom = () => {
  const container = document.querySelector('.overflow-y-auto')
  if (container) {
    container.scrollTop = container.scrollHeight
  }
}
</script>