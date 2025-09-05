<template>
  <div class="flex h-screen bg-gray-50">
    <!-- Sidebar Progress Tracker -->
    <div class="w-80 bg-white border-r border-gray-200 flex flex-col">
      <div class="p-6 border-b border-gray-200">
        <h2 class="text-lg font-semibold text-gray-800 mb-2">Progress Tracker</h2>
        <div class="text-sm text-gray-600 mb-3">
          Current Step: <span class="font-medium text-blue-600">{{ formattedCurrentStep }}</span>
        </div>
        
        <!-- Progress Bar -->
        <div class="w-full bg-gray-200 rounded-full h-2.5 mb-3">
          <div 
            class="bg-blue-500 h-2.5 rounded-full transition-all duration-300" 
            :style="{ width: `${progressPercentage}%` }"
          ></div>
        </div>
        <div class="text-xs text-gray-500">
          Progress: {{ stepsCompleted }}/{{ totalSteps }} steps completed
        </div>
      </div>

      <!-- Captured Details -->
      <div class="p-6 flex-1 overflow-y-auto">
        <div class="space-y-4">
          <div v-if="coaching.messages.length > 0">
            <button 
              @click="showDetails = !showDetails"
              class="flex items-center justify-between w-full text-sm font-medium text-gray-700 hover:text-gray-900"
            >
              <span>View Captured Details</span>
              <svg 
                class="w-4 h-4 transform transition-transform" 
                :class="{ 'rotate-180': showDetails }"
                fill="none" stroke="currentColor" viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
              </svg>
            </button>
            
            <div v-show="showDetails" class="mt-3 space-y-3 text-sm">
              <div>
                <span class="font-medium text-gray-700">Task:</span>
                <p class="text-gray-600 mt-1">{{ taskPreview || 'Not provided yet' }}</p>
              </div>
              <div>
                <span class="font-medium text-gray-700">Context:</span>
                <p class="text-gray-600 mt-1">{{ contextPreview || 'Not provided yet' }}</p>
              </div>
              <div>
                <span class="font-medium text-gray-700">References:</span>
                <p class="text-gray-600 mt-1">{{ referencesStatus }}</p>
              </div>
              <div>
                <span class="font-medium text-gray-700">Final Prompt:</span>
                <p class="text-gray-600 mt-1">{{ finalPromptStatus }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="p-6 border-t border-gray-200 space-y-3">
        <button 
          @click="resetConversation"
          class="w-full px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
        >
          Reset Conversation
        </button>
        
        <!-- Completion Section -->
        <div v-if="isCompleted" class="space-y-3">
          <div class="text-center">
            <div class="text-2xl mb-2">🎉</div>
            <p class="text-sm font-medium text-green-600">Congratulations! Your prompt is ready.</p>
          </div>
          <button 
            v-if="coaching.refinedPrompt"
            @click="downloadPrompt"
            class="w-full px-4 py-2 text-sm font-medium text-white bg-green-600 hover:bg-green-700 rounded-lg transition-colors"
          >
            Download Final Prompt
          </button>
        </div>
      </div>
    </div>

    <!-- Main Chat Area -->
    <div class="flex-1 flex flex-col">
      <!-- Header -->
      <div class="bg-white border-b border-gray-200 p-6">
        <h1 class="text-2xl font-bold text-gray-800">Prompt Engineering Coach</h1>
        <p class="text-gray-600 text-sm mt-1">Master the art of prompt engineering with guided assistance!</p>
      </div>

      <!-- Messages Container -->
      <div class="flex-1 overflow-y-auto p-6 space-y-4">
        <div
          v-for="(message, index) in coaching.messages"
          :key="index"
          class="flex"
          :class="message.role === 'human' ? 'justify-end' : 'justify-start'"
        >
          <div
            class="max-w-3xl rounded-lg px-4 py-3"
            :class="message.role === 'human' 
              ? 'bg-blue-500 text-white' 
              : 'bg-white border border-gray-200 text-gray-800'"
          >
            <div class="text-sm">{{ message.content }}</div>
            <div class="text-xs mt-2 opacity-70">
              {{ formatTime(message.timestamp) }}
            </div>
          </div>
        </div>

        <!-- Loading Indicator -->
        <div v-if="coaching.loading" class="flex justify-start">
          <div class="bg-white border border-gray-200 rounded-lg px-4 py-3">
            <div class="flex items-center space-x-2">
              <div class="flex space-x-1">
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
              </div>
              <span class="text-sm text-gray-500">Coach is thinking...</span>
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
            :disabled="coaching.loading"
            placeholder="Type your response here..."
            class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
          />
          <button
            @click="sendMessage"
            :disabled="coaching.loading || !currentInput.trim()"
            class="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Send
          </button>
        </div>

        <!-- Error Display -->
        <div v-if="coaching.error" class="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p class="text-sm text-red-600">{{ coaching.error }}</p>
          <button 
            @click="coaching.clearError()"
            class="text-xs text-red-500 hover:text-red-700 mt-1"
          >
            Dismiss
          </button>
        </div>
      </div>

      <!-- Help Section -->
      <div class="bg-gray-50 border-t border-gray-200">
        <button 
          @click="showHelp = !showHelp"
          class="w-full p-4 text-left text-sm font-medium text-gray-700 hover:text-gray-900 flex items-center justify-between"
        >
          <span>💡 Need Help?</span>
          <svg 
            class="w-4 h-4 transform transition-transform" 
            :class="{ 'rotate-180': showHelp }"
            fill="none" stroke="currentColor" viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
          </svg>
        </button>
        
        <div v-show="showHelp" class="px-4 pb-4 text-sm text-gray-600 space-y-2">
          <div>
            <p class="font-medium mb-2">How to use the Prompt Engineering Coach:</p>
            <ol class="list-decimal list-inside space-y-1 ml-4">
              <li><strong>Task:</strong> Describe what you want to accomplish</li>
              <li><strong>Context:</strong> Provide background information and requirements</li>
              <li><strong>References:</strong> Share any resources or examples</li>
              <li><strong>Final Prompt:</strong> Create your complete engineered prompt</li>
            </ol>
          </div>
          
          <div>
            <p class="font-medium mb-2">Tips:</p>
            <ul class="list-disc list-inside space-y-1 ml-4">
              <li>Be specific about your needs</li>
              <li>Provide concrete examples when possible</li>
              <li>Don't worry if you're not sure - the coach will guide you!</li>
              <li>You can say "suggest some tasks" if you need ideas</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useCoachingStore } from '@/stores/coaching'

// Store
const coaching = useCoachingStore()

// Reactive state
const currentInput = ref('')
const showDetails = ref(false)
const showHelp = ref(false)

// Computed properties for progress tracking
const formattedCurrentStep = computed(() => {
  return coaching.currentStep.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
})

const totalSteps = 4
const stepsCompleted = computed(() => {
  // This is a simplified version - you might want to track actual steps from your backend
  const messages = coaching.assistantMessages
  if (messages.length === 0) return 0
  if (messages.length <= 2) return 1
  if (messages.length <= 4) return 2  
  if (messages.length <= 6) return 3
  return 4
})

const progressPercentage = computed(() => {
  return (stepsCompleted.value / totalSteps) * 100
})

const isCompleted = computed(() => {
  return coaching.currentStep === 'completed' || coaching.refinedPrompt !== null
})

// Preview text for captured details
const taskPreview = computed(() => {
  // Extract task from conversation - this is simplified
  const userMessages = coaching.userMessages
  if (userMessages.length > 0) {
    const firstMessage = userMessages[0].content
    return firstMessage.length > 50 ? firstMessage.substring(0, 50) + '...' : firstMessage
  }
  return ''
})

const contextPreview = computed(() => {
  // Extract context from conversation - simplified
  const userMessages = coaching.userMessages
  if (userMessages.length > 1) {
    const secondMessage = userMessages[1].content
    return secondMessage.length > 50 ? secondMessage.substring(0, 50) + '...' : secondMessage
  }
  return ''
})

const referencesStatus = computed(() => {
  return coaching.userMessages.length > 2 ? 'Provided' : 'Not provided yet'
})

const finalPromptStatus = computed(() => {
  return coaching.refinedPrompt ? 'Created' : 'Not created yet'
})

// Methods
const sendMessage = async () => {
  if (!currentInput.value.trim() || coaching.loading) return
  
  const message = currentInput.value.trim()
  currentInput.value = ''
  
  try {
    await coaching.sendMessage(message)
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('Error sending message:', error)
  }
}

const resetConversation = async () => {
  if (confirm('Are you sure you want to reset the conversation? This will clear all progress.')) {
    coaching.clearConversation()
    await coaching.createNewSession()
  }
}

const downloadPrompt = () => {
  if (!coaching.refinedPrompt) return
  
  const element = document.createElement('a')
  const file = new Blob([coaching.refinedPrompt], { type: 'text/plain' })
  element.href = URL.createObjectURL(file)
  element.download = 'engineered_prompt.txt'
  document.body.appendChild(element)
  element.click()
  document.body.removeChild(element)
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

// Initialize conversation on mount
onMounted(async () => {
  if (coaching.messages.length === 0) {
    try {
      await coaching.createNewSession()
      // Send initial empty message to trigger welcome
      await coaching.sendMessage('')
    } catch (error) {
      console.error('Error initializing conversation:', error)
    }
  }
})
</script>