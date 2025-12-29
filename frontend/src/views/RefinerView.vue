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
      <!-- Main Sidebar Content (Optional for Refiner) -->
      <div v-show="!sidebarCollapsed" class="p-4 animate-fade-in">
        <div class="bg-gradient-to-br from-primary/10 to-accent/10 rounded-2xl p-5 border border-primary/20">
          <h3 class="text-xs font-black text-primary uppercase tracking-widest mb-2">Pro Tip</h3>
          <p class="text-xs text-text opacity-70 leading-relaxed font-medium">Use the Refiner to improve clarity, tone, and structural integrity of your prompts before deployment.</p>
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
              <h1 class="text-xl font-black text-slate-800 dark:text-white tracking-tight">Refiner Assistant</h1>
              <p class="text-xs text-slate-500 dark:text-slate-400 font-bold uppercase tracking-widest leading-none mt-1">Optimize and polish your prompts</p>
            </div>
          </div>
        </div>
      </div>

      <ChatInterface 
        :showHeader="false" 
        variant="refiner"
        class="flex-1"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ChatSidebar from '@/components/chat/ChatSidebar.vue'
import ChatInterface from '@/components/chat/ChatInterface.vue'
import { useTheme } from '@/composables/useTheme'
import gsap from 'gsap'

// Theme & Sidebar State
const { isDarkMode, toggleTheme, initTheme } = useTheme()
const sidebarCollapsed = ref(window.innerWidth < 1024)
const sidebarRef = ref(null)

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

onMounted(() => {
  initTheme()
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