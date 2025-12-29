<template>
  <div class="coach-chat-interface flex h-full bg-background relative overflow-hidden">
    <!-- Mobile Header -->
    <div class="mobile-header lg:hidden fixed top-0 left-0 right-0 h-16 bg-background border-b border-card-border z-[160] flex items-center justify-between px-4">
      <div class="flex items-center space-x-2">
        <span class="text-xs font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent uppercase tracking-widest">Master Prompting</span>
      </div>
      <button @click="toggleSidebar" class="p-2 rounded-lg hover:bg-secondary transition-colors">
        <svg v-if="sidebarCollapsed" class="w-6 h-6 text-text" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
        <svg v-else class="w-6 h-6 text-text" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <!-- Modular Sidebar -->
    <ChatSidebar
      ref="sidebarRef"
      :collapsed="sidebarCollapsed"
      :isDarkMode="isDarkMode"
      title="Progress Tracker"
      subtitle="Coaching Session"
      @toggle="toggleSidebar"
      @toggle-theme="toggleTheme"
    >
      <template #header-bottom>
        <!-- Current Step Display -->
        <div class="current-step mt-4" v-show="!sidebarCollapsed && progressInfo.currentStep && progressInfo.currentStep !== 'initializing'">
          <div class="flex items-center space-x-2 mb-2">
            <div class="w-2 h-2 rounded-full bg-gradient-to-r from-primary to-accent animate-pulse"></div>
            <span class="text-xs font-bold text-text uppercase tracking-tighter">Current Stage</span>
          </div>
          <div class="bg-gradient-to-r from-secondary to-secondary-bg border border-primary/20 rounded-xl px-4 py-2.5 shadow-sm">
            <span class="text-sm font-black text-primary">{{ currentStepDisplay }}</span>
          </div>
        </div>
      </template>

      <!-- Main Sidebar Content -->
      <div v-show="!sidebarCollapsed" class="animate-fade-in">
        <!-- Main Progress -->
        <div class="p-4 border-b border-card-border">
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center space-x-2">
              <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-zap text-primary opacity-70"><path d="M4 14.5 14 3l-2.5 9h8.5L10 21l2.5-9z"/></svg>
              <h3 class="text-[10px] font-black text-slate-800 dark:text-slate-200 opacity-60 uppercase tracking-widest">Efficiency</h3>
            </div>
            <span class="text-[10px] font-black text-primary">{{ Math.round(progressInfo.progressPercentage) }}%</span>
          </div>
          <div class="w-full bg-secondary rounded-full h-1.5 mb-4 overflow-hidden">
            <div 
              class="main-progress-bar h-full rounded-full transition-all duration-1000 ease-out"
              :style="{ width: `${progressInfo.progressPercentage}%` }"
            ></div>
          </div>
          
          <!-- Step Indicators -->
          <div class="grid grid-cols-4 gap-2">
            <div 
              v-for="(step, index) in coachingSteps" 
              :key="step.key"
              class="flex flex-col items-center group cursor-help"
              :title="step.description"
            >
              <div 
                class="w-8 h-8 rounded-lg flex items-center justify-center text-[10px] font-black transition-all duration-300 shadow-sm"
                :class="getStepCircleClasses(step, index)"
              >
                <span v-if="step.completed">✓</span>
                <span v-else>{{ index + 1 }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Captured Details -->
        <div class="p-4 border-b border-card-border">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center space-x-2">
              <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-lightbulb text-primary opacity-70"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/></svg>
              <h3 class="text-[10px] font-black text-slate-800 dark:text-slate-200 opacity-60 uppercase tracking-widest">Insights</h3>
            </div>
          </div>
          <div class="space-y-4">
            <div v-for="field in ['task', 'context']" :key="field" class="group">
              <div class="text-[10px] font-bold text-text opacity-40 uppercase mb-1.5 transition-opacity group-hover:opacity-70">{{ field }}</div>
              <div class="text-xs text-text bg-secondary/50 border border-card-border/50 rounded-xl p-3 leading-relaxed min-h-[40px] max-h-24 overflow-y-auto no-scrollbar font-medium">
                {{ progressInfo[field] || 'Awating input...' }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <template #footer-bottom>
        <button 
          @click="resetConversation"
          class="w-full bg-card-bg border border-card-border hover:bg-secondary text-text px-4 py-3 rounded-xl text-xs font-bold transition-all shadow-sm flex items-center justify-center group"
        >
          <svg class="w-4 h-4 transition-transform group-hover:rotate-180 duration-500" :class="sidebarCollapsed ? '' : 'mr-3'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span v-show="!sidebarCollapsed">Reset Session</span>
        </button>

        <button 
          v-if="progressInfo.currentStep === 'completed' || progressInfo.finalPrompt"
          @click="downloadPrompt(progressInfo.finalPrompt)"
          class="w-full mt-2 bg-primary hover:bg-primary-600 text-white px-4 py-3 rounded-xl text-xs font-bold transition-all shadow-lg shadow-primary/20 flex items-center justify-center animate-bounce-subtle"
        >
          <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          <span v-show="!sidebarCollapsed">Export Prompt</span>
        </button>
      </template>
    </ChatSidebar>

    <!-- Main Chat Area -->
    <div class="main-chat flex-1 flex flex-col relative bg-background">
      <div class="chat-header border-b border-card-border/50 bg-background/80 backdrop-blur-md p-6 transition-colors duration-300 z-10 pt-20 lg:pt-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <div class="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center text-primary">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-mic"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></svg>
            </div>
            <div>
              <h1 class="text-xl font-black text-text tracking-tight">Coach Interface</h1>
              <p class="text-xs text-text opacity-50 font-bold uppercase tracking-widest">Active Intelligence Session</p>
            </div>
          </div>
          
          <button @click="helpExpanded = !helpExpanded" class="p-2 rounded-lg hover:bg-secondary transition-colors" :class="{'text-primary': helpExpanded}">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Help Overlay -->
      <transition 
        enter-active-class="transition duration-300 ease-out"
        enter-from-class="transform translate-y-[-20px] opacity-0"
        enter-to-class="transform translate-y-0 opacity-100"
        leave-active-class="transition duration-200 ease-in"
        leave-from-class="transform translate-y-0 opacity-100"
        leave-to-class="transform translate-y-[-20px] opacity-0"
      >
        <div v-if="helpExpanded" class="help-overlay absolute top-24 left-6 right-6 bg-card-bg/95 backdrop-blur-xl border border-card-border rounded-3xl p-6 shadow-2xl z-20">
          <h3 class="text-sm font-black text-text uppercase tracking-widest mb-4">Coaching Methodology</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div v-for="(stage, i) in ['Task Definition', 'Context Injection', 'Resource Alignment', 'Prototype Creation']" :key="i" class="flex items-start space-x-3">
              <div class="w-5 h-5 rounded bg-primary/20 text-primary flex items-center justify-center text-[10px] font-bold">{{ i + 1 }}</div>
              <span class="text-xs font-semibold text-text opacity-80">{{ stage }}</span>
            </div>
          </div>
        </div>
      </transition>

      <!-- Messages -->
      <div class="messages-container flex-1 overflow-hidden">
        <div class="max-w-4xl mx-auto h-full w-full px-4 md:px-8 relative">
          <ChatMessageList 
            v-if="messages.length > 0 || isLoading"
            :messages="messages"
            :isLoading="isLoading"
            :loadingMessage="loadingMessage"
            variant="coach"
          />
          
          <!-- Welcome Screen -->
          <div v-else class="h-full flex items-center justify-center animate-fade-in text-center p-8">
            <div class="max-w-md space-y-6">
              <div class="w-16 h-16 bg-white dark:bg-slate-800 rounded-3xl mx-auto shadow-xl flex items-center justify-center transform hover:rotate-6 transition-transform duration-500 border border-card-border overflow-hidden">
                 <img :src="isDarkMode ? logoDark : logoLight" alt="Prompt Engine" class="w-full h-full object-cover" />
              </div>
              
              <div class="inline-block px-4 py-1.5 rounded-full border border-slate-300 dark:border-slate-700 bg-white/50 dark:bg-black/20 backdrop-blur-sm">
                <span class="text-[10px] font-black tracking-widest uppercase text-slate-800 dark:text-slate-200">Intelligence-Driven Coaching</span>
              </div>

              <div class="space-y-4">
                <h2 class="text-4xl lg:text-5xl font-black text-slate-900 dark:text-white tracking-tighter leading-[0.9]">
                  Build the <br/>
                  <span class="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent italic pr-1">Perfect Prompt.</span>
                </h2>
                <p class="text-xs text-slate-500 dark:text-slate-400 font-bold uppercase tracking-wide leading-relaxed max-w-sm mx-auto">
                  Transform vague requests into structured, high-performance instructions using our expert deep coaching methodology.
                </p>
                <div class="pt-4 flex items-center justify-center gap-3 text-[10px] font-black text-slate-400 dark:text-slate-600 uppercase tracking-widest opacity-70">
                   <span>4-Stage Loop</span>
                   <span class="w-1 h-1 rounded-full bg-current"></span>
                   <span>Context Analysis</span>
                   <span class="w-1 h-1 rounded-full bg-current"></span>
                   <span>Iterative Refinement</span>
                </div>
              </div>

              <div class="pt-6">
                <button 
                  @click="$emit('start-session')"
                  class="px-8 py-4 bg-primary text-white rounded-2xl font-black shadow-lg shadow-primary/20 hover:scale-105 hover:shadow-primary/40 transition-all duration-300 flex items-center justify-center gap-2 mx-auto"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-play"><polygon points="6 3 20 12 6 21 6 3"/></svg>
                  Launch Session
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="chat-input p-4 pt-10 bg-gradient-to-t from-background via-background/90 to-transparent">
        <div class="max-w-4xl mx-auto w-full px-4 md:px-8">
          <UnifiedChatInput
            :disabled="isLoading"
            @send-message="handleSendMessage"
          />
        </div>
      </div>

      <!-- Error -->
      <div v-if="error" class="absolute bottom-24 left-1/2 -translate-x-1/2 w-full max-w-lg px-4 animate-slide-up z-[200]">
        <div class="bg-card-bg/90 backdrop-blur-md border-2 border-primary/20 p-4 rounded-2xl shadow-2xl flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-alert-triangle"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>
            </div>
            <span class="text-xs font-bold text-slate-800 dark:text-slate-200">{{ error }}</span>
          </div>
          <button @click="clearError" class="p-1 hover:bg-secondary rounded-lg">✕</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import ChatSidebar from './ChatSidebar.vue'
import ChatMessageList from './ChatMessageList.vue'
import UnifiedChatInput from './UnifiedChatInput.vue'
import { useCoachChat } from './useCoachChat.js'
import './coach-chat.css'
import logoLight from '@/assets/images/logoLight.png'
import logoDark from '@/assets/images/logoDark.png'

const props = defineProps({
  messages: Array,
  isLoading: Boolean,
  loadingMessage: String,
  error: String,
  progressInfo: Object
})

const emit = defineEmits(['send-message', 'stop-generation', 'clear-error', 'reset-conversation', 'download-prompt', 'start-session'])

const {
  isDarkMode,
  sidebarCollapsed,
  sidebarRef,
  toggleTheme,
  toggleSidebar,
  handleSendMessage,
  clearError,
  resetConversation,
  downloadPrompt
} = useCoachChat(props, emit)

const helpExpanded = ref(false)

const coachingSteps = computed(() => [
  { key: 'task', title: 'Task', description: 'Defining the goal', completed: !!props.progressInfo.task, active: props.progressInfo.currentStep === 'task' },
  { key: 'context', title: 'Context', description: 'Adding background', completed: !!props.progressInfo.context, active: props.progressInfo.currentStep === 'context' },
  { key: 'references', title: 'Resource', description: 'Resource alignment', completed: props.progressInfo.references?.length > 0, active: props.progressInfo.currentStep === 'references' },
  { key: 'final', title: 'Prototype', description: 'Final prompt creation', completed: !!props.progressInfo.finalPrompt, active: props.progressInfo.currentStep === 'final_prompt' }
])

const currentStepDisplay = computed(() => {
  return props.progressInfo.currentStep.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
})

const getStepCircleClasses = (step, index) => {
  if (step.completed) return 'bg-success/20 text-success border border-success/30 scale-90'
  if (step.active) return 'bg-primary text-white border border-primary/50 scale-110 shadow-lg shadow-primary/30 animate-pulse'
  return 'bg-secondary text-text opacity-30 border border-card-border/50 scale-90'
}
</script>