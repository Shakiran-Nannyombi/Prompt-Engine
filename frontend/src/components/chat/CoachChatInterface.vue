<template>
    <div class="coach-chat-interface flex h-full bg-background relative overflow-hidden">
    <!-- Mobile Header/Navbar -->
    <div class="mobile-header lg:hidden fixed top-0 left-0 right-0 h-16 bg-card-bg border-b border-card-border z-[70] flex items-center justify-between px-4">
      <div class="flex items-center space-x-2">
        <div class="logo-container w-8 h-8 bg-white rounded-full relative">
          <img src="/PE_logo.svg" alt="Prompt Engine" class="w-full h-full" />
          <div class="absolute -inset-1 bg-gradient-to-r from-primary/20 to-accent/20 rounded-full blur-sm"></div>
        </div>
        <span class="text-sm font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">Prompt Engine</span>
      </div>
      <button @click="toggleSidebar" class="p-2 rounded-lg hover:bg-secondary transition-colors" aria-label="Toggle Menu">
        <svg v-if="sidebarCollapsed" class="w-6 h-6 text-text" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
        <svg v-else class="w-6 h-6 text-text" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <!-- Progress Tracker Sidebar -->
    <div 
      ref="sidebarRef"
      class="progress-sidebar border-r border-card-border bg-card-bg flex flex-col transition-all duration-300 ease-in-out fixed lg:relative h-full z-[60] lg:z-40 overflow-y-auto no-scrollbar"
      :class="[
        sidebarCollapsed ? '-translate-x-full lg:translate-x-0 lg:w-20' : 'translate-x-0 w-full lg:w-72',
        !sidebarCollapsed ? 'top-0 left-0 right-0 bottom-0 shadow-2xl' : ''
      ]"
    >
      <!-- Sidebar Header -->
      <div class="sidebar-header p-4 border-b border-card-border bg-gradient-to-r from-primary/5 to-accent/5 mt-0 lg:mt-0">
        <!-- Logo and Title Section -->
        <div class="flex items-center" :class="sidebarCollapsed ? 'justify-center flex-col gap-4' : 'justify-between mb-4'">
          <div class="flex items-center" :class="sidebarCollapsed ? 'flex-col gap-2' : 'space-x-3'">
            <div class="logo-container relative bg-white rounded-full transition-all duration-300" :class="sidebarCollapsed ? 'w-8 h-8' : 'w-10 h-10'">
              <img src="/PE_logo.svg" alt="Prompt Engine" class="w-full h-full drop-shadow-lg" />
              <div class="absolute -inset-1 bg-gradient-to-r from-primary/20 to-accent/20 rounded-full blur-sm"></div>
            </div>
            <div v-show="!sidebarCollapsed" class="whitespace-nowrap overflow-hidden transition-all duration-300">
              <h2 class="text-lg font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                Progress Tracker
              </h2>
              <p class="text-sm text-text opacity-80 font-medium">Coaching Session</p>
            </div>
          </div>
          
           <!-- Sidebar Toggle Button (Desktop only) -->
            <div class="hidden lg:flex items-center">
              <button 
                @click="toggleSidebar"
                class="p-2 rounded-lg border border-card-border bg-card-bg hover:bg-secondary transition-all duration-200 group shadow-sm"
                title="Toggle Sidebar"
              >
                <svg v-if="!sidebarCollapsed" class="w-5 h-5 text-text" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
                <svg v-else class="w-5 h-5 text-text transition-transform" :class="sidebarCollapsed ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
                </svg>
              </button>
            </div>
        </div>
        
        
        <!-- Current Step Display -->
        <div class="current-step" v-show="!sidebarCollapsed && progressInfo.currentStep && progressInfo.currentStep !== 'initializing'">
          <div class="flex items-center space-x-2 mb-2">
            <div class="w-2 h-2 rounded-full bg-gradient-to-r from-primary to-accent animate-pulse"></div>
            <span class="text-sm font-semibold text-text">Current Step</span>
          </div>
          <div class="bg-gradient-to-r from-secondary to-secondary-bg border border-primary/20 rounded-lg px-3 py-2 shadow-sm">
            <span class="text-sm font-mono font-medium text-text">{{ currentStepDisplay }}</span>
          </div>
        </div>
      </div>

      <!-- Navigation Section -->
      <div class="sidebar-nav border-b border-card-border" :class="sidebarCollapsed ? 'p-2' : 'p-4'">
        <h3 class="text-xs font-medium text-text mb-2 opacity-70" :class="sidebarCollapsed ? 'text-center' : ''">
            <span v-if="!sidebarCollapsed">Navigation</span>
            <span v-else class="text-[10px]">Nav</span>
        </h3>
        <div class="space-y-1">
          <router-link to="/" class="flex items-center rounded-lg text-xs font-medium text-text hover:bg-secondary transition-colors" :class="sidebarCollapsed ? 'justify-center p-2' : 'space-x-2 px-2 py-1.5'" title="Home">
            <svg class="w-4 h-4 opacity-70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
            <span v-show="!sidebarCollapsed">Home</span>
          </router-link>
          
          <div class="flex items-center rounded-lg text-xs font-medium bg-primary/10 text-primary cursor-default" :class="sidebarCollapsed ? 'justify-center p-2' : 'space-x-2 px-2 py-1.5'" title="Coach (Active)">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
            <span v-show="!sidebarCollapsed">Coach (Active)</span>
          </div>

          <router-link to="/refiner" class="flex items-center rounded-lg text-xs font-medium text-text hover:bg-secondary transition-colors" :class="sidebarCollapsed ? 'justify-center p-2' : 'space-x-2 px-2 py-1.5'" title="Refiner">
            <svg class="w-4 h-4 opacity-70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
            </svg>
            <span v-show="!sidebarCollapsed">Refiner</span>
          </router-link>

           <router-link to="/about" class="flex items-center rounded-lg text-xs font-medium text-text hover:bg-secondary transition-colors" :class="sidebarCollapsed ? 'justify-center p-2' : 'space-x-2 px-2 py-1.5'" title="Documentation">
            <svg class="w-4 h-4 opacity-70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <span v-show="!sidebarCollapsed">Documentation</span>
          </router-link>
        </div>
      </div>

      <!-- Main Progress Bar Section -->
      <div class="main-progress-section border-b border-card-border" :class="sidebarCollapsed ? 'p-2' : 'p-4'" v-show="!sidebarCollapsed">
        <div class="flex items-center justify-between mb-2">
          <h3 class="text-xs font-medium text-text">Overall Progress</h3>
          <span class="text-xs text-text opacity-70">{{ progressInfo.stepsCompleted }}/{{ progressInfo.totalSteps }} steps</span>
        </div>
        
        <!-- Large Progress Bar -->
        <div class="progress-bar-container mb-2">
          <div class="w-full bg-secondary rounded-full h-3">
            <div 
              class="main-progress-bar h-3 rounded-full transition-all duration-700 ease-out"
              :style="{ width: `${progressInfo.progressPercentage}%` }"
            ></div>
          </div>
          <div class="text-xs text-text opacity-70 mt-1 text-center">
            {{ Math.round(progressInfo.progressPercentage) }}% Complete
          </div>
        </div>
        
        <!-- Progress Steps -->
        <div class="progress-steps flex justify-between mt-1 gap-1">
          <div 
            v-for="(step, index) in coachingSteps" 
            :key="step.key"
            class="progress-step flex flex-col items-center"
          >
            <div 
              class="step-circle w-4 h-4 rounded-full flex items-center justify-center text-xs font-medium mb-0.5 transition-all duration-300"
              :class="getStepCircleClasses(step, index)"
            >
              <span v-if="step.completed" class="text-xs">✓</span>
              <span v-else class="text-xs">{{ index + 1 }}</span>
            </div>
            <div class="step-label text-xs text-center max-w-8">
              <div class="font-medium leading-tight">{{ step.title.split(' ')[0] }}</div>
            </div>
          </div>
        </div>
      </div>
  
  
      <!-- Conversation History -->
      <div class="conversation-history border-b border-card-border" :class="sidebarCollapsed ? 'p-2' : 'p-4'" v-show="!sidebarCollapsed">
        <div class="flex items-center justify-between mb-3">
          <h3 class="text-xs font-medium text-text">Conversation History</h3>
          <button 
            @click="toggleHistoryExpanded"
            class="text-xs text-text opacity-70 hover:opacity-100 transition-opacity"
          >
            {{ historyExpanded ? 'Hide' : 'Show' }}
          </button>
        </div>
        
        <div v-if="historyExpanded" class="space-y-2">
          <div class="flex items-center space-x-2 mb-2">
            <input 
              v-model="newThreadName"
              @keyup.enter="createNewThread"
              placeholder="New thread name..."
              class="flex-1 text-xs bg-secondary border border-card-border rounded px-2 py-1 text-text placeholder-text opacity-70"
            />
            <button 
              @click="createNewThread"
              class="text-xs bg-primary text-white px-2 py-1 rounded hover:bg-primary-600 transition-colors"
            >
              New
            </button>
          </div>
          
          <div class="thread-list max-h-32 overflow-y-auto space-y-1">
            <div 
              v-for="thread in conversationThreads" 
              :key="thread.id"
              @click="loadThread(thread.id)"
              class="thread-item p-2 rounded cursor-pointer transition-colors text-xs"
              :class="currentThreadId === thread.id ? 'bg-primary text-white' : 'bg-secondary hover:bg-secondary-bg text-text'"
            >
              <div class="font-medium truncate">{{ thread.name }}</div>
              <div class="opacity-70 text-xs">{{ formatThreadDate(thread.lastMessage) }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Captured Details -->
      <div class="captured-details border-b border-card-border flex-1" :class="sidebarCollapsed ? 'p-2' : 'p-4'" v-show="!sidebarCollapsed">
        <div class="flex items-center justify-between mb-3">
          <h3 class="text-xs font-medium text-text">Captured Details</h3>
          <button 
            @click="toggleDetailsExpanded"
            class="text-xs text-text opacity-70 hover:opacity-100 transition-opacity"
          >
            {{ detailsExpanded ? 'Hide' : 'Show' }}
          </button>
        </div>
        
        <div v-if="detailsExpanded" class="space-y-2">
          <div class="detail-item">
            <div class="detail-label text-xs font-medium text-text opacity-70 mb-1">Task</div>
            <div class="detail-content text-xs text-text bg-secondary rounded p-2 min-h-[1.5rem] max-h-16 overflow-y-auto">
              {{ progressInfo.task || 'Not provided yet' }}
            </div>
          </div>
          
          <div class="detail-item">
            <div class="detail-label text-xs font-medium text-text opacity-70 mb-1">Context</div>
            <div class="detail-content text-xs text-text bg-secondary rounded p-2 min-h-[1.5rem] max-h-16 overflow-y-auto">
              {{ progressInfo.context || 'Not provided yet' }}
            </div>
          </div>
          
          <div class="detail-item">
            <div class="detail-label text-xs font-medium text-text opacity-70 mb-1">References</div>
            <div class="detail-content text-xs text-text bg-secondary rounded p-2 min-h-[1.5rem] max-h-16 overflow-y-auto">
              {{ progressInfo.references ? 'Provided' : 'Not provided yet' }}
            </div>
          </div>
          
          <div class="detail-item">
            <div class="detail-label text-xs font-medium text-text opacity-70 mb-1">Final Prompt</div>
            <div class="detail-content text-xs text-text bg-secondary rounded p-2 min-h-[1.5rem] max-h-16 overflow-y-auto">
              {{ progressInfo.finalPrompt ? 'Created' : 'Not created yet' }}
            </div>
          </div>
        </div>
      </div>
  
      <div class="sidebar-actions space-y-2 border-t border-card-border pt-4 mt-auto" :class="sidebarCollapsed ? 'p-2' : 'p-4'">
        <!-- Dark/Light Mode Toggle -->
        <button 
          @click="toggleTheme"
          class="w-full p-2 rounded-lg border border-card-border bg-card-bg hover:bg-secondary transition-all duration-200 group shadow-sm flex items-center justify-center mb-2"
          :title="isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
        >
          <svg v-if="isDarkMode" class="w-4 h-4 text-text group-hover:scale-110 transition-transform" :class="sidebarCollapsed ? '' : 'mr-2'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
          <svg v-else class="w-4 h-4 text-text group-hover:scale-110 transition-transform" :class="sidebarCollapsed ? '' : 'mr-2'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
          </svg>
          <span v-show="!sidebarCollapsed" class="text-xs font-medium">Theme Mode</span>
        </button>

        <!-- Reset Button -->
        <button 
          @click="handleResetConversation"
          class="w-full bg-card-bg border border-card-border hover:bg-secondary text-text px-3 py-2 rounded-lg text-xs font-medium transition-colors shadow-sm flex items-center justify-center"
          :title="sidebarCollapsed ? 'Reset Conversation' : ''"
        >
          <svg class="w-4 h-4" :class="sidebarCollapsed ? '' : 'mr-2'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span v-show="!sidebarCollapsed">Reset Conversation</span>
        </button>
        
        <!-- Download Button (when completed) -->
        <button 
          v-if="progressInfo.currentStep === 'completed' && progressInfo.finalPrompt"
          @click="handleDownloadPrompt"
          class="w-full bg-primary hover:bg-primary-600 text-white px-3 py-2 rounded-lg text-xs font-medium transition-colors"
        >
          <span v-show="sidebarCollapsed">⬇️</span>
          <span v-show="!sidebarCollapsed">Download Final Prompt</span>
        </button>
      </div>  
        <!-- Completion Celebration -->
        <div v-if="progressInfo.currentStep === 'completed'" class="completion-celebration text-center">
          <div class="text-lg mb-1">🎉</div>
          <div class="text-xs font-medium text-text">Congratulations!</div>
          <div class="text-xs text-text opacity-70">Your prompt is ready</div>
        </div>
      </div>
  
    <!-- Main Chat Area -->
    <div class="main-chat flex-1 flex flex-col relative">
      <!-- Chat Header -->
      <div class="chat-header border-b border-card-border/50 bg-card-bg/80 backdrop-blur-sm p-6 transition-colors duration-300 z-10 pt-20 lg:pt-6">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4 flex-1">
              <div>
                <h1 class="text-xl font-semibold text-text">Prompt Engineering Coach</h1>
                <p class="text-sm text-text opacity-70">Master the art of prompt engineering with guided assistance!</p>
              </div>
            </div>
            
            <!-- Help Toggle -->
            <button 
              @click="toggleHelp"
              class="help-button text-text opacity-70 hover:opacity-100 transition-opacity"
              :class="{ 'text-primary': helpExpanded }"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </button>
          </div>
        </div>
  
        <!-- Help Section -->
        <div v-if="helpExpanded" class="help-section border-b border-card-border bg-secondary p-6">
          <div class="help-content">
            <h3 class="text-sm font-semibold text-text mb-3">How to use the Prompt Engineering Coach:</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-text">
              <div>
                <div class="font-medium mb-2">Coaching Process:</div>
                <ol class="list-decimal list-inside space-y-1 text-xs opacity-80">
                  <li><strong>Task:</strong> Describe what you want to accomplish</li>
                  <li><strong>Context:</strong> Provide background information and requirements</li>
                  <li><strong>References:</strong> Share any resources or examples</li>
                  <li><strong>Final Prompt:</strong> Create your complete engineered prompt</li>
                </ol>
              </div>
              <div>
                <div class="font-medium mb-2">Tips:</div>
                <ul class="list-disc list-inside space-y-1 text-xs opacity-80">
                  <li>Be specific about your needs</li>
                  <li>Provide concrete examples when possible</li>
                  <li>Don't worry if you're not sure - the coach will guide you!</li>
                  <li>You can say "suggest some tasks" if you need ideas</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Messages Container -->
      <div class="messages-container flex-1 overflow-hidden relative">
        <div class="max-w-4xl mx-auto h-full w-full px-4 md:px-8 lg:px-16">
          <ChatMessageList 
            :messages="messages"
            :isLoading="isLoading"
            :loadingMessage="loadingMessage"
            variant="coach"
            @scroll-to-bottom="handleScrollToBottom"
          />
        </div>
      </div>

      <!-- Chat Input -->
      <div class="chat-input absolute bottom-0 left-0 right-0 p-4 pt-10 z-20">
        <div class="max-w-4xl mx-auto w-full px-4 md:px-8 lg:px-16">
          <UnifiedChatInput
            :disabled="isLoading"
            @send-message="handleSendMessage"
          />
        </div>
      </div>
  
        <!-- Error Display -->
        <div v-if="error" class="error-display border-t border-error bg-error-50 p-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-2">
              <svg class="w-4 h-4 text-error" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span class="text-sm text-error">{{ error }}</span>
            </div>
            <button
              @click="clearError"
              class="text-error hover:text-error-600 transition-colors"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted, watch } from 'vue'
  import ChatMessageList from './ChatMessageList.vue'
  import UnifiedChatInput from './UnifiedChatInput.vue'
  import gsap from 'gsap'
  
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
      default: 'Coach is thinking...'
    },
    showStopButton: {
      type: Boolean,
      default: false
    },
    error: {
      type: String,
      default: ''
    },
    progressInfo: {
      type: Object,
      default: () => ({
        task: '',
        context: '',
        references: [],
        finalPrompt: '',
        currentStep: 'initializing',
        stepsCompleted: 0,
        totalSteps: 4,
        progressPercentage: 0
      })
    }
  })
  
const emit = defineEmits(['send-message', 'stop-generation', 'clear-error', 'reset-conversation', 'download-prompt', 'load-thread', 'create-thread'])

// Local state
const detailsExpanded = ref(false)
const helpExpanded = ref(false)
const historyExpanded = ref(false)
const newThreadName = ref('')
const currentThreadId = ref('')
const isDarkMode = ref(false)
const sidebarCollapsed = ref(window.innerWidth < 1024)
const sidebarRef = ref(null)

// Conversation threads state
const conversationThreads = ref([
  {
    id: 'thread-1',
    name: 'Customer Service Bot',
    lastMessage: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
    messages: []
  },
  {
    id: 'thread-2', 
    name: 'Code Review Assistant',
    lastMessage: new Date(Date.now() - 24 * 60 * 60 * 1000), // 1 day ago
    messages: []
  },
  {
    id: 'thread-3',
    name: 'Email Template Generator',
    lastMessage: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000), // 3 days ago
    messages: []
  }
])
  
  // Coaching steps configuration
  const coachingSteps = computed(() => [
    {
      key: 'task',
      title: 'Define Task',
      description: 'What do you want to accomplish?',
      completed: !!props.progressInfo.task,
      active: props.progressInfo.currentStep === 'task'
    },
    {
      key: 'context',
      title: 'Add Context',
      description: 'Background information and requirements',
      completed: !!props.progressInfo.context,
      active: props.progressInfo.currentStep === 'context'
    },
    {
      key: 'references',
      title: 'Provide References',
      description: 'Resources and examples',
      completed: props.progressInfo.references && props.progressInfo.references.length > 0,
      active: props.progressInfo.currentStep === 'references'
    },
    {
      key: 'final_prompt',
      title: 'Create Final Prompt',
      description: 'Your engineered prompt',
      completed: !!props.progressInfo.finalPrompt,
      active: props.progressInfo.currentStep === 'final_prompt'
    }
  ])
  
  // Computed properties
  const currentStepDisplay = computed(() => {
    return props.progressInfo.currentStep.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
  })
  
// Methods
const toggleDetailsExpanded = () => {
  detailsExpanded.value = !detailsExpanded.value
}

const toggleHelp = () => {
  helpExpanded.value = !helpExpanded.value
}

const toggleHistoryExpanded = () => {
  historyExpanded.value = !historyExpanded.value
}

const toggleSidebar = () => {
  const isOpening = sidebarCollapsed.value // It's currently collapsed
  sidebarCollapsed.value = !sidebarCollapsed.value
  
  if (window.innerWidth < 1024) {
    if (isOpening) {
      // Menu is Opening
      gsap.fromTo(sidebarRef.value, 
        { x: '-100%', opacity: 0 },
        { x: 0, opacity: 1, duration: 0.5, ease: 'power3.out' }
      )
    } else {
      // Menu is Closing
      gsap.to(sidebarRef.value, {
        x: '-100%',
        opacity: 0,
        duration: 0.4,
        ease: 'power3.in',
        onComplete: () => {
          // Ensure it's fully hidden if needed
        }
      })
    }
  }
}

const createNewThread = () => {
  if (!newThreadName.value.trim()) return
  
  const newThread = {
    id: `thread-${Date.now()}`,
    name: newThreadName.value.trim(),
    lastMessage: new Date(),
    messages: []
  }
  
  conversationThreads.value.unshift(newThread)
  newThreadName.value = ''
  
  // Emit to parent to handle thread creation
  emit('create-thread', newThread)
}

const loadThread = (threadId) => {
  currentThreadId.value = threadId
  const thread = conversationThreads.value.find(t => t.id === threadId)
  if (thread) {
    emit('load-thread', thread)
  }
}

const formatThreadDate = (date) => {
  if (!date) return ''
  
  const now = new Date()
  const diffInHours = (now - date) / (1000 * 60 * 60)
  
  if (diffInHours < 1) {
    return 'Just now'
  } else if (diffInHours < 24) {
    return `${Math.floor(diffInHours)}h ago`
  } else {
    const diffInDays = Math.floor(diffInHours / 24)
    return `${diffInDays}d ago`
  }
}

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  
  // Toggle theme on document root - this will automatically use your existing CSS variables
  const root = document.documentElement
  if (isDarkMode.value) {
    root.classList.add('dark')
  } else {
    root.classList.remove('dark')
  }
  
  // Save theme preference to localStorage
  localStorage.setItem('theme', isDarkMode.value ? 'dark' : 'light')
}
  
  const handleSendMessage = (message) => {
    emit('send-message', message)
  }
  
  const handleStopGeneration = () => {
    emit('stop-generation')
  }
  
  const handleScrollToBottom = () => {
    // Handle scroll to bottom
  }
  
  const handleResetConversation = () => {
    emit('reset-conversation')
  }
  
  const handleDownloadPrompt = () => {
    emit('download-prompt', props.progressInfo.finalPrompt)
  }
  
  const clearError = () => {
    emit('clear-error')
  }
  
const getStepClasses = (step, index) => {
  const baseClasses = 'transition-colors'
  
  if (step.completed) {
    return `${baseClasses} bg-success-50 border border-success-200`
  } else if (step.active) {
    return `${baseClasses} bg-primary-50 border border-primary-200`
  } else {
    return `${baseClasses} bg-secondary hover:bg-secondary-bg`
  }
}

const getStepCircleClasses = (step, index) => {
  const baseClasses = 'transition-all duration-300'
  
  if (step.completed) {
    return `${baseClasses} bg-success text-white shadow-sm`
  } else if (step.active) {
    return `${baseClasses} bg-primary text-white shadow-md scale-110`
  } else {
    return `${baseClasses} bg-secondary text-text opacity-60`
  }
}
  
// Initialize with welcome message if no messages exist
onMounted(() => {
  if (props.messages.length === 0) {
    // This would typically be handled by the parent component
    // to start the conversation with the coach
  }
  
  // Initialize theme from localStorage
  const savedTheme = localStorage.getItem('theme')
  const root = document.documentElement
  
  if (savedTheme === 'dark') {
    isDarkMode.value = true
    root.classList.add('dark')
  } else {
    isDarkMode.value = false
    root.classList.remove('dark')
  }
})
  </script>
  
  <style scoped>
  .coach-chat-interface {
    min-height: 0;
  }
  
  .progress-sidebar {
    flex-shrink: 0;
    min-height: 0;
  }
  
  .main-chat {
    min-height: 0;
  }
  
  .messages-container {
    flex: 1;
    min-height: 0;
  }
  
.progress-bar {
  background: linear-gradient(90deg, var(--color-primary) 0%, var(--color-accent) 100%);
}

.main-progress-bar {
  background: linear-gradient(90deg, var(--color-primary) 0%, var(--color-accent) 100%);
  box-shadow: 0 2px 4px var(--color-primary)/30;
}

.logo-container {
  position: relative;
}

.logo-container img {
  position: relative;
  z-index: 1;
  filter: drop-shadow(0 0 8px rgba(102, 126, 234, 0.3));
}

.theme-toggle {
  position: relative;
  overflow: hidden;
  background-color: var(--color-card-bg);
  border: 1px solid var(--color-card-border);
  color: var(--color-text);
  transition: all 0.3s ease;
}

.theme-toggle:hover {
  background-color: var(--color-secondary);
  border-color: var(--color-primary);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.theme-toggle:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.theme-toggle svg {
  color: var(--color-text);
  transition: all 0.3s ease;
}

.theme-toggle:hover svg {
  color: var(--color-primary);
}

.theme-toggle::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, var(--color-primary)/20, transparent);
  transition: left 0.5s;
}

.theme-toggle:hover::before {
  left: 100%;
}

/* Theme transition animations */
.coach-chat-interface,
.progress-sidebar,
.sidebar-header,
.main-progress-section,
.conversation-history,
.captured-details,
.sidebar-actions {
  transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease;
}

/* Use existing theme variables */
.coach-chat-interface {
  background-color: var(--color-background);
  color: var(--color-text);
}

.progress-sidebar {
  background-color: var(--color-card-bg);
  border-color: var(--color-card-border);
}

.sidebar-header {
  background: linear-gradient(to right, var(--color-primary)/10, var(--color-accent)/10);
  border-color: var(--color-card-border);
}

.main-progress-section,
.conversation-history,
.captured-details,
.sidebar-actions {
  background-color: var(--color-card-bg);
  border-color: var(--color-card-border);
  color: var(--color-text);
}

.main-chat {
  background-color: var(--color-background);
  color: var(--color-text);
}

.chat-header {
  background-color: var(--color-card-bg);
  border-color: var(--color-card-border);
  color: var(--color-text);
}

.help-section {
  background-color: var(--color-secondary);
  border-color: var(--color-card-border);
  color: var(--color-text);
}

.chat-input {
  background-color: var(--color-card-bg);
  border-color: var(--color-card-border);
}

.error-display {
  background-color: var(--color-card-bg);
  border-color: var(--color-primary);
  color: var(--color-text);
}
  
  .step-icon {
    background: var(--color-secondary);
    color: var(--color-text);
    transition: all 0.3s ease;
  }
  
  .step-indicator.completed .step-icon {
    background: var(--color-success);
    color: white;
  }
  
  .step-indicator.active .step-icon {
    background: var(--color-primary);
    color: white;
  }
  
  .coach-avatar {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }
  
  .help-button {
    transition: all 0.2s ease;
  }
  
  .help-button:hover {
    transform: scale(1.1);
  }
  
  .completion-celebration {
    animation: celebrate 0.6s ease-in-out;
  }
  
  @keyframes celebrate {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
  }
  
/* Responsive adjustments */
@media (max-width: 1024px) {
  .progress-sidebar {
    width: 260px;
  }
}

@media (max-width: 768px) {
  .coach-chat-interface {
    flex-direction: column;
  }
  
  .progress-sidebar {
    width: 100%;
    max-height: 35vh;
    overflow-y: auto;
  }
  
  .main-chat {
    flex: 1;
    min-height: 65vh;
  }
}

@media (max-width: 480px) {
  .progress-sidebar {
    max-height: 30vh;
  }
  
  .main-chat {
    min-height: 70vh;
  }
}
  </style>