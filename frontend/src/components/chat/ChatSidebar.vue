<template>
  <div 
    ref="sidebarRef"
    class="chat-sidebar border-r border-card-border bg-background flex flex-col transition-all duration-300 ease-in-out fixed lg:relative h-full z-[150] lg:z-40 overflow-y-auto no-scrollbar"
    :class="[
      collapsed ? '-translate-x-full lg:translate-x-0 lg:w-20' : 'translate-x-0 w-full lg:w-80',
      !collapsed ? 'inset-0 lg:inset-auto shadow-2xl lg:shadow-none backdrop-blur-xl lg:backdrop-blur-none' : ''
    ]"
  >
    <!-- Sidebar Header -->
    <div class="sidebar-header p-4 border-b border-card-border bg-gradient-to-r from-primary/5 to-accent/5">
      <div class="flex items-center" :class="collapsed ? 'justify-center flex-col gap-8' : 'justify-between mb-8'">
        <div class="flex items-center" :class="collapsed ? 'flex-col gap-6' : 'space-x-6'">
          <div class="logo-container relative transition-all duration-300 flex items-center justify-center overflow-hidden" :class="collapsed ? 'w-10 h-10' : 'w-14 h-14'">
            <img src="@/assets/images/logo.svg" alt="Prompt Engine" class="w-full h-full object-contain" />
          </div>
          <div v-show="!collapsed" class="whitespace-nowrap overflow-hidden transition-all duration-300 ml-3">
              <h2 class="text-lg font-black text-text tracking-tight leading-none">
              {{ title }}
            </h2>
            <p class="text-[10px] text-text opacity-80 font-bold uppercase tracking-widest mt-1">{{ subtitle }}</p>
          </div>
        </div>
        
        <!-- Sidebar Toggle Button (Desktop only) -->
        <div class="hidden lg:flex items-center">
          <button 
            @click="$emit('toggle')"
            class="p-2 rounded-lg border border-card-border bg-card-bg hover:bg-secondary transition-all duration-200 group shadow-sm"
            title="Toggle Sidebar"
          >
            <svg v-if="!collapsed" class="w-5 h-5 text-text" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
            <svg v-else class="w-5 h-5 text-text rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
            </svg>
          </button>
        </div>
      </div>
      
      <!-- Slot for dynamic header content (e.g. current step) -->
      <slot name="header-bottom"/>
    </div>

    <!-- Navigation Section -->
    <div class="sidebar-nav border-b border-card-border" :class="collapsed ? 'p-2' : 'p-4'">
      <h3 class="text-[10px] font-bold text-text mb-3 opacity-80 uppercase tracking-widest" :class="collapsed ? 'text-center' : ''">
          Navigation
      </h3>
      <div class="space-y-1">
        <router-link to="/" class="nav-item group" :class="collapsed ? 'justify-center p-2' : 'space-x-3 px-3 py-2'" title="Home">
          <svg class="w-5 h-5 opacity-70 group-hover:text-primary transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
          <span v-show="!collapsed" class="text-sm font-semibold">Home</span>
        </router-link>
        
        <router-link to="/coach" class="nav-item group" :class="[collapsed ? 'justify-center p-2' : 'space-x-3 px-3 py-2', $route.path === '/coach' ? 'active' : '']" title="Coach">
          <svg class="w-5 h-5 opacity-70 group-hover:text-primary transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
          <span v-show="!collapsed" class="text-sm font-semibold">Coach</span>
        </router-link>

        <router-link to="/refiner" class="nav-item group" :class="[collapsed ? 'justify-center p-2' : 'space-x-3 px-3 py-2', $route.path === '/refiner' ? 'active' : '']" title="Refiner">
          <svg class="w-5 h-5 opacity-70 group-hover:text-primary transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
          </svg>
          <span v-show="!collapsed" class="text-sm font-semibold">Refiner</span>
        </router-link>

         <router-link to="/about" class="nav-item group" :class="collapsed ? 'justify-center p-2' : 'space-x-3 px-3 py-2'" title="About">
          <svg class="w-5 h-5 opacity-70 group-hover:text-primary transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span v-show="!collapsed" class="text-sm font-semibold">About</span>
        </router-link>
      </div>
    </div>

    <!-- Main Content Slot (Threads, Progress, etc.) -->
    <div class="flex-1 overflow-y-auto no-scrollbar">
      <slot />
    </div>

    <!-- Footer Actions -->
    <div class="sidebar-actions space-y-2 border-t border-card-border p-4 mt-auto">
      <button 
        @click="$emit('toggle-theme')"
        class="w-full p-2.5 rounded-xl border border-card-border bg-card-bg hover:bg-secondary transition-all duration-300 group shadow-sm flex items-center justify-center"
        :title="isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
      >
        <svg v-if="isDarkMode" class="w-5 h-5 text-text group-hover:rotate-12 transition-transform" :class="collapsed ? '' : 'mr-3'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
        <svg v-else class="w-5 h-5 text-text group-hover:rotate-12 transition-transform" :class="collapsed ? '' : 'mr-3'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
        </svg>
        <span v-show="!collapsed" class="text-sm font-bold text-text">Theme Mode</span>
      </button> <br>

      <slot name="footer-bottom" />

      <div class="pt-2">
          <p class="text-[10px] text-text opacity-80 text-center font-bold tracking-tighter" v-show="!collapsed">Prompt Engine Premium v1.0</p>
          <p class="text-[10px] text-text opacity-80 text-center font-bold" v-show="collapsed">v1.0</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import logo from '@/assets/images/logo.svg'

const props = defineProps({
  collapsed: Boolean,
  isDarkMode: Boolean,
  title: {
    type: String,
    default: 'Progress Tracker'
  },
  subtitle: {
    type: String,
    default: 'Coaching Session'
  }
})

const emit = defineEmits(['toggle', 'toggle-theme'])
const sidebarRef = ref(null)

defineExpose({
  sidebarRef
})
</script>

<style scoped>
.chat-sidebar {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-item {
  display: flex;
  align-items: center;
  border-radius: 0.75rem;
  color: var(--color-text);
  text-decoration: none;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.nav-item:hover {
  background: var(--color-secondary);
  color: var(--color-primary);
  transform: translateX(4px);
}

.nav-item.active {
  background: var(--color-primary-5);
  color: var(--color-primary);
  border-color: var(--color-primary-20);
}

.nav-item.active svg {
  color: var(--color-primary);
  opacity: 1;
}

/* Custom Hide Scrollbar */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
