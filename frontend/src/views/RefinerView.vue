<template>
  <div class="refiner-view flex h-screen bg-background relative overflow-hidden">
    <!-- Mobile Header/Navbar -->
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

    <!-- Sidebar -->
    <div 
      ref="sidebarRef"
      class="sidebar border-r border-card-border bg-background flex flex-col pt-0 transition-all duration-300 ease-in-out fixed lg:relative h-full z-[150] lg:z-40 overflow-y-auto no-scrollbar"
      :class="[
        sidebarCollapsed ? '-translate-x-full lg:translate-x-0 lg:w-20' : 'translate-x-0 w-full lg:w-72',
        !sidebarCollapsed ? 'inset-0 shadow-2xl' : ''
      ]"
    >
      <!-- Sidebar Header -->
      <div class="sidebar-header p-4 border-b border-card-border bg-gradient-to-r from-primary/5 to-accent/5 mt-0 lg:mt-0">
        <div class="flex items-center" :class="sidebarCollapsed ? 'justify-center flex-col gap-4' : 'justify-between mb-4'">
          <div class="flex items-center" :class="sidebarCollapsed ? 'flex-col gap-2' : 'space-x-3'">
            <div class="logo-container relative bg-white dark:bg-card-bg rounded-full transition-all duration-300" :class="sidebarCollapsed ? 'w-8 h-8' : 'w-10 h-10'">
              <img :src="isDarkMode ? logoDark : logoLight" alt="Prompt Engine" class="w-full h-full drop-shadow-lg" />
              <div class="absolute -inset-1 bg-gradient-to-r from-primary/20 to-accent/20 rounded-full blur-sm"></div>
            </div>
            <div v-show="!sidebarCollapsed" class="whitespace-nowrap overflow-hidden transition-all duration-300">
              <h2 class="text-lg font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                Refiner
              </h2>
              <p class="text-sm text-text opacity-80 font-medium">Prompt Polishing</p>
            </div>
          </div>
          
           <!-- Sidebar Toggle (Desktop only) -->
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
      </div>

      <!-- Navigation Section -->
      <div class="sidebar-nav border-b border-card-border" :class="sidebarCollapsed ? 'p-2' : 'p-4'">
        <h3 class="text-xs font-medium text-text mb-2 opacity-70" :class="sidebarCollapsed ? 'text-center' : ''">
            <span v-if="!sidebarCollapsed">Navigation</span>
            <span v-else class="text-[10px]">Nav</span>
        </h3>
        <div class="space-y-1">
          <router-link to="/" class="flex items-center rounded-lg text-xs font-medium text-text hover:bg-secondary transition-colors" :class="sidebarCollapsed ? 'justify-center p-2' : 'space-x-2 px-2 py-1.5'">
            <svg class="w-4 h-4 opacity-70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
            <span v-show="!sidebarCollapsed">Home</span>
          </router-link>
          
          <router-link to="/coach" class="flex items-center rounded-lg text-xs font-medium text-text hover:bg-secondary transition-colors" :class="sidebarCollapsed ? 'justify-center p-2' : 'space-x-2 px-2 py-1.5'">
            <svg class="w-4 h-4 opacity-70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
            <span v-show="!sidebarCollapsed">Coach</span>
          </router-link>

          <div class="flex items-center rounded-lg text-xs font-medium bg-primary/10 text-primary cursor-default" :class="sidebarCollapsed ? 'justify-center p-2' : 'space-x-2 px-2 py-1.5'">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
            </svg>
            <span v-show="!sidebarCollapsed">Refiner (Active)</span>
          </div>

           <router-link to="/about" class="flex items-center rounded-lg text-xs font-medium text-text hover:bg-secondary transition-colors" :class="sidebarCollapsed ? 'justify-center p-2' : 'space-x-2 px-2 py-1.5'">
            <svg class="w-4 h-4 opacity-70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <span v-show="!sidebarCollapsed">Documentation</span>
          </router-link>
        </div>
      </div>
      
      <div class="flex-1"></div>
      
      <!-- Footer Info and Actions -->
      <div class="sidebar-actions space-y-2 border-t border-card-border mt-auto" :class="sidebarCollapsed ? 'p-2' : 'p-4'">
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

        <div class="pt-2">
            <p class="text-xs text-text opacity-50 text-center" v-show="!sidebarCollapsed">Prompt Engine v1.0</p>
            <p class="text-[10px] text-text opacity-50 text-center" v-show="sidebarCollapsed">v1.0</p>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden pt-16 lg:pt-0">
      <ChatInterface 
        title="Refiner Assistant" 
        subtitle="Optimize and polish your prompts"
        variant="refiner"
        :showHeader="true" 
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ChatInterface from '@/components/chat/ChatInterface.vue'
import gsap from 'gsap'
import logoLight from '@/assets/images/logoLight.png'
import logoDark from '@/assets/images/logoDark.png'

// Theme Management
const isDarkMode = ref(false)
const sidebarCollapsed = ref(window.innerWidth < 1024)
const sidebarRef = ref(null)

const toggleSidebar = () => {
    const isOpening = sidebarCollapsed.value
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
                ease: 'power3.in'
            })
        }
    }
}

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
}

onMounted(() => {
  // Check theme preference
  const savedTheme = localStorage.getItem('theme')
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  
  if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
    isDarkMode.value = true
    document.documentElement.classList.add('dark')
  } else {
    isDarkMode.value = false
    document.documentElement.classList.remove('dark')
  }
})
</script>