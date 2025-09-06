<template>
  <div class="coach-view h-screen flex flex-col bg-background">
    <!-- Navigation Header -->
    <div class="nav-header border-b border-card-border bg-card-bg px-6 py-4 transition-colors duration-300">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <router-link to="/" class="flex items-center space-x-2 text-text hover:text-primary transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            <span class="text-sm font-medium">Back to Home</span>
          </router-link>
        </div>
        
        <div class="flex items-center space-x-3">
          <img src="/PE_logo.svg" alt="Prompt Engine" class="w-8 h-8" />
          <span class="text-lg font-semibold text-text">Prompt Engine</span>
        </div>
        
        <div class="flex items-center space-x-2">
          <button 
            @click="toggleFullscreen"
            class="p-2 text-text opacity-70 hover:opacity-100 transition-opacity"
            title="Toggle fullscreen"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Main Chat Interface -->
    <div class="flex-1 overflow-hidden">
      <CoachChatInterface
        :messages="messages"
        :isLoading="isLoading"
        :loadingMessage="loadingMessage"
        :showStopButton="showStopButton"
        :error="error"
        :progressInfo="progressInfo"
        @send-message="handleSendMessage"
        @stop-generation="handleStopGeneration"
        @clear-error="clearError"
        @reset-conversation="handleResetConversation"
        @download-prompt="handleDownloadPrompt"
        @load-thread="handleLoadThread"
        @create-thread="handleCreateThread"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import CoachChatInterface from '@/components/chat/CoachChatInterface.vue'
import { coachingAPI, extractMessages, getLatestMessage, getRefinedPrompt } from '@/service/api.js'

// State management
const messages = ref([])
const isLoading = ref(false)
const loadingMessage = ref('Coach is thinking...')
const showStopButton = ref(false)
const error = ref('')
const isFullscreen = ref(false)
const currentThreadId = ref(null)

// Progress tracking state
const progressInfo = reactive({
  task: '',
  context: '',
  references: [],
  finalPrompt: '',
  currentStep: 'initializing',
  stepsCompleted: 0,
  totalSteps: 4,
  progressPercentage: 0
})

// Computed properties
const currentStepDisplay = computed(() => {
  return progressInfo.currentStep.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
})

// Methods
const handleSendMessage = async (message) => {
  try {
    // Add user message to chat
    messages.value.push({
      id: Date.now(),
      sender: 'user',
      content: message,
      timestamp: new Date().toISOString()
    })

    // Set loading state
    isLoading.value = true
    error.value = ''

    // Prepare conversation history for API
    const conversationHistory = messages.value
      .filter(msg => msg.sender !== 'system')
      .map(msg => ({
        role: msg.sender === 'user' ? 'user' : 'assistant',
        content: msg.content
      }))

    // Call the real coaching API
    const response = await coachingAPI.sendMessage(
      message,
      conversationHistory,
      currentThreadId.value
    )
    
    // Extract response data
    const agentOutput = getLatestMessage(response)
    const refinedPrompt = getRefinedPrompt(response)
    const fullHistory = extractMessages(response)
    
    // Add assistant response
    messages.value.push({
      id: Date.now() + 1,
      sender: 'assistant',
      content: agentOutput,
      timestamp: new Date().toISOString()
    })

    // Update progress info based on conversation
    updateProgressFromConversation(fullHistory)

  } catch (err) {
    error.value = 'Failed to get response from coach. Please try again.'
    console.error('Error sending message:', err)
  } finally {
    isLoading.value = false
  }
}

const handleStopGeneration = () => {
  isLoading.value = false
  showStopButton.value = false
}

const clearError = () => {
  error.value = ''
}

const handleResetConversation = async () => {
  messages.value = []
  error.value = ''
  isLoading.value = false
  
  // Reset progress info
  Object.assign(progressInfo, {
    task: '',
    context: '',
    references: [],
    finalPrompt: '',
    currentStep: 'initializing',
    stepsCompleted: 0,
    totalSteps: 4,
    progressPercentage: 0
  })
  
  // Create new thread
  await createNewThread()
  
  // Start new conversation
  startNewConversation()
}

const handleDownloadPrompt = (prompt) => {
  if (!prompt) return
  
  const blob = new Blob([prompt], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'engineered_prompt.txt'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

const toggleFullscreen = () => {
  isFullscreen.value = !isFullscreen.value
  // You could implement fullscreen logic here
}

const handleLoadThread = (thread) => {
  // Load conversation history for the selected thread
  console.log('Loading thread:', thread)
  
  // Set current thread ID
  currentThreadId.value = thread.id
  
  // Load messages from thread
  messages.value = thread.messages || []
  
  // Reset progress if starting fresh
  if (messages.value.length === 0) {
    Object.assign(progressInfo, {
      task: '',
      context: '',
      references: [],
      finalPrompt: '',
      currentStep: 'initializing',
      stepsCompleted: 0,
      totalSteps: 4,
      progressPercentage: 0
    })
    startNewConversation()
  } else {
    // Update progress from existing conversation
    updateProgressFromConversation(messages.value)
  }
}

const handleCreateThread = async (thread) => {
  // Create a new conversation thread
  console.log('Creating new thread:', thread)
  
  // Create new thread on backend
  await createNewThread()
  
  // Reset everything for new thread
  messages.value = []
  error.value = ''
  isLoading.value = false
  
  // Reset progress info
  Object.assign(progressInfo, {
    task: '',
    context: '',
    references: [],
    finalPrompt: '',
    currentStep: 'initializing',
    stepsCompleted: 0,
    totalSteps: 4,
    progressPercentage: 0
  })
  
  // Start new conversation
  startNewConversation()
}

const createNewThread = async () => {
  try {
    const response = await coachingAPI.createNewThread()
    currentThreadId.value = response.data.thread_id
    console.log('Created new thread:', currentThreadId.value)
  } catch (error) {
    console.error('Failed to create new thread:', error)
    // Fallback to a local thread ID
    currentThreadId.value = `thread-${Date.now()}`
  }
}

const updateProgressFromConversation = (conversationHistory) => {
  // Analyze conversation to determine progress
  const userMessages = conversationHistory.filter(msg => msg.role === 'user')
  const assistantMessages = conversationHistory.filter(msg => msg.role === 'assistant')
  
  // Simple progress detection based on conversation content
  let currentStep = 'initializing'
  let task = ''
  let context = ''
  let references = []
  let finalPrompt = ''
  
  // Look for task definition
  if (userMessages.length > 0) {
    const firstUserMessage = userMessages[0].content.toLowerCase()
    if (firstUserMessage.includes('task') || firstUserMessage.includes('want to') || firstUserMessage.includes('need to')) {
      currentStep = 'task'
      task = userMessages[0].content
    }
  }
  
  // Look for context
  if (userMessages.length > 1) {
    const contextMessage = userMessages.find(msg => 
      msg.content.toLowerCase().includes('context') || 
      msg.content.toLowerCase().includes('background') ||
      msg.content.toLowerCase().includes('situation')
    )
    if (contextMessage) {
      currentStep = 'context'
      context = contextMessage.content
    }
  }
  
  // Look for references
  const referenceMessage = userMessages.find(msg => 
    msg.content.toLowerCase().includes('reference') || 
    msg.content.toLowerCase().includes('example') ||
    msg.content.toLowerCase().includes('resource')
  )
  if (referenceMessage) {
    currentStep = 'references'
    references = [referenceMessage.content]
  }
  
  // Look for final prompt
  const finalPromptMessage = assistantMessages.find(msg => 
    msg.content.toLowerCase().includes('final prompt') || 
    msg.content.toLowerCase().includes('here is your prompt')
  )
  if (finalPromptMessage) {
    currentStep = 'final_prompt'
    finalPrompt = finalPromptMessage.content
  }
  
  // Calculate progress
  const stepsCompleted = [task, context, references.length > 0, finalPrompt].filter(Boolean).length
  const progressPercentage = (stepsCompleted / 4) * 100
  
  // Update progress info
  Object.assign(progressInfo, {
    task,
    context,
    references,
    finalPrompt,
    currentStep,
    stepsCompleted,
    totalSteps: 4,
    progressPercentage
  })
}


const startNewConversation = () => {
  // Add welcome message
  messages.value.push({
    id: Date.now(),
    sender: 'assistant',
    content: "Hello! I'm your Prompt Engineering Coach. I'm here to help you create effective prompts through a structured process. Let's start by understanding what you want to accomplish. What task or goal do you have in mind?",
    timestamp: new Date().toISOString()
  })
}

// Initialize
onMounted(async () => {
  // Create initial thread
  await createNewThread()
  // Start new conversation
  startNewConversation()
})
</script>

<style scoped>
.coach-view {
  min-height: 0;
}

.nav-header {
  flex-shrink: 0;
}

/* Theme-aware styling */
.coach-view {
  background-color: var(--color-background);
  color: var(--color-text);
  transition: background-color 0.3s ease, color 0.3s ease;
}

.nav-header {
  background-color: var(--color-card-bg);
  border-color: var(--color-card-border);
  color: var(--color-text);
  transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .nav-header {
    padding: 1rem;
  }
  
  .nav-header .flex {
    flex-direction: column;
    space-y: 0.5rem;
  }
}
</style>