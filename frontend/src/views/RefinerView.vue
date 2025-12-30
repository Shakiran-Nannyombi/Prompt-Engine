<template>
  <div class="refiner-view flex h-screen bg-background relative overflow-hidden">
    <!-- Mobile Header -->
    <div class="mobile-header lg:hidden fixed top-0 left-0 right-0 h-16 bg-background border-b border-card-border z-[160] flex items-center justify-between px-4">
      <div class="flex items-center space-x-2">
        <span class="text-xs font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent uppercase tracking-widest">Refine Prompt</span>
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

    <!-- Modular Sidebar -->
    <ChatSidebar
      ref="sidebarRef"
      :collapsed="sidebarCollapsed"
      :isDarkMode="isDarkMode"
      title="Prompt Refiner"
      subtitle="Polishing Assistant"
      @toggle="toggleSidebar"
      @toggle-theme="toggleTheme"
    >
      <template #header-bottom v-if="currentThreadId">
        <div class="px-4 py-2 mt-2 bg-primary/5 rounded-lg border border-primary/10">
          <span class="text-[10px] font-bold text-primary uppercase tracking-widest">Active Refiner Session</span>
        </div>
      </template>
      <!-- Main Sidebar Content (Optional for Refiner) -->
      <div v-show="!sidebarCollapsed" class="p-4 animate-fade-in">
        <div class="bg-gradient-to-br from-primary/10 to-accent/10 rounded-2xl p-5 border border-primary/20">
          <h3 class="text-xs font-black text-primary uppercase tracking-widest mb-2">Pro Tip</h3>
          <p class="text-xs text-text opacity-70 leading-relaxed font-medium">Use the Refiner to improve clarity, tone, and structural integrity of your prompts before deployment.</p>
        </div>
        
        <div class="mt-8 space-y-2">
          <button 
            @click="handleResetSession"
            class="w-full bg-card-bg border border-card-border hover:bg-secondary text-text px-4 py-3 rounded-xl text-xs font-bold transition-all shadow-sm flex items-center justify-center group"
          >
            <svg class="w-4 h-4 mr-3 transition-transform group-hover:rotate-180 duration-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Reset Session
          </button>
        </div>
      </div>
    </ChatSidebar>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden bg-background">
      <div class="chat-header border-b border-card-border/50 bg-background/80 backdrop-blur-md p-6 transition-colors duration-300 z-10 pt-20 lg:pt-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <div class="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center text-primary">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-wand-2"><path d="m21 21-2.156-2.156"/><path d="M18 5 5 18"/><path d="M4 11V9"/><path d="M9 4V2"/><path d="M4 4h2"/><path d="M10 10V8"/><path d="M15 15v-2"/><path d="M10 15h2"/><path d="M15 10h2"/></svg>
            </div>
            <div>
              <h1 class="text-xl font-black text-text tracking-tight leading-none">Refiner Assistant</h1>
              <p class="text-[10px] text-text opacity-80 font-bold uppercase tracking-widest mt-1">AI Prompt Optimization</p>
            </div>
          </div>
        </div>
      </div>

      <ChatInterface 
        :messages="messages"
        :isLoading="isLoading"
        :loadingMessage="loadingMessage"
        :error="error"
        :showHeader="false" 
        variant="refiner"
        class="flex-1"
        @send-message="handleSendMessage"
        @start-session="startNewSession"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import ChatSidebar from '@/components/chat/ChatSidebar.vue'
import ChatInterface from '@/components/chat/ChatInterface.vue'
import { refinerAPI, getLatestMessage, extractMessages } from '@/service/api.js'
import { useTheme } from '@/composables/useTheme'
import gsap from 'gsap'

// Theme & Sidebar State
const { isDarkMode, toggleTheme, initTheme } = useTheme()
const sidebarCollapsed = ref(window.innerWidth < 1024)
const sidebarRef = ref(null)

// Chat State
const messages = ref([])
const isLoading = ref(false)
const loadingMessage = ref('Refiner is analyzing...')
const error = ref('')
const currentThreadId = ref(null)

const toggleSidebar = () => {
    const isOpening = sidebarCollapsed.value
    sidebarCollapsed.value = !sidebarCollapsed.value
    
    if (window.innerWidth < 1024) {
        if (isOpening) {
            gsap.fromTo(sidebarRef.value.$el || sidebarRef.value, 
                { x: '-100%', opacity: 0 },
                { x: 0, opacity: 1, duration: 0.5, ease: 'power3.out' }
            )
        } else {
            gsap.to(sidebarRef.value.$el || sidebarRef.value, {
                x: '-100%',
                opacity: 0,
                duration: 0.4,
                ease: 'power3.in'
            })
        }
    }
}

const handleSendMessage = async (payload) => {
  try {
    const messageContent = typeof payload === 'string' ? payload : payload.message
    
    // Add user message
    messages.value.push({
      id: Date.now(),
      sender: 'user',
      content: messageContent,
      timestamp: new Date().toISOString()
    })

    isLoading.value = true
    error.value = ''

    // Prepare history
    const history = messages.value.map(msg => ({
      role: msg.sender === 'user' ? 'user' : 'assistant',
      content: msg.content
    }))

    // Call Refiner API
    const response = await refinerAPI.sendMessage(messageContent, history, currentThreadId.value)
    
    const output = getLatestMessage(response)
    
    // Add assistant response
    messages.value.push({
      id: Date.now() + 1,
      sender: 'assistant',
      content: output,
      timestamp: new Date().toISOString()
    })

  } catch (err) {
    error.value = err.response?.data?.detail || err.message || 'Optimization failed. Please try again.'
    console.error('Refiner error:', err)
  } finally {
    isLoading.value = false
  }
}

const startNewSession = () => {
  messages.value = [{
    id: Date.now(),
    sender: 'assistant',
    content: "Ready to polish! Paste your prompt here, and I'll help you optimize it for clarity, tone, and performance.",
    timestamp: new Date().toISOString()
  }]
}

const handleResetSession = async () => {
  messages.value = []
  error.value = ''
  await createNewThread()
  startNewSession()
}

const createNewThread = async () => {
  try {
    const response = await refinerAPI.createNewThread()
    currentThreadId.value = response.data.thread_id
  } catch (e) {
    currentThreadId.value = `refiner-${Date.now()}`
  }
}

onMounted(async () => {
  initTheme()
  await createNewThread()
  const handleResize = () => {
    if (window.innerWidth >= 1024) {
      sidebarCollapsed.value = false
    } else {
      sidebarCollapsed.value = true
    }
  }
  window.addEventListener('resize', handleResize)
})
</script>

<style scoped>
.refiner-view {
  background-color: var(--color-background);
  color: var(--color-text);
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>