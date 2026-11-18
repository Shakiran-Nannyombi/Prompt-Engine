<script setup>
/* The Home page's floating navbar, shared by every public page. */
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import gsap from 'gsap'
import { useTheme } from '@/composables/useTheme'
import { useAuthStore } from '@/stores/useAuthStore'
import logo from '@/assets/images/logo.svg'

const links = [
  { to: '/', label: 'Home' },
  { to: '/coach', label: 'Coach' },
  { to: '/refiner', label: 'Refiner' },
  { to: '/tutorials', label: 'Tutorials' },
  { to: '/about', label: 'About' },
]

const { isDarkMode, toggleTheme, initTheme } = useTheme()
const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()

const scrolled = ref(false)
const showMobileMenu = ref(false)

const onScroll = () => {
  scrolled.value = window.scrollY > 50
}
const handleLogout = () => {
  authStore.logout()
  showMobileMenu.value = false
  router.push('/')
}
const onMenuEnter = (el, done) => {
  gsap.fromTo(el, { y: '-100%', opacity: 0 }, { y: '0%', opacity: 1, duration: 0.4, ease: 'power2.out', onComplete: done })
}
const onMenuLeave = (el, done) => {
  gsap.to(el, { y: '-100%', opacity: 0, duration: 0.3, ease: 'power2.in', onComplete: done })
}
const onKey = (e) => {
  if (e.key === 'Escape') showMobileMenu.value = false
}

watch(() => route.fullPath, () => (showMobileMenu.value = false))

onMounted(() => {
  initTheme()
  onScroll()
  window.addEventListener('scroll', onScroll, { passive: true })
  window.addEventListener('keydown', onKey)
})
onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
  window.removeEventListener('keydown', onKey)
})
</script>

<template>
  <nav class="navbar" :class="{ scrolled }" aria-label="Main">
    <div class="navbar-content">
      <RouterLink to="/" class="navbar-brand">
        <img :src="logo" alt="Prompt-Engine Logo" class="logo-icon" />
        <span class="brand-name">Prompt-Engine</span>
      </RouterLink>

      <div class="navbar-links hidden md:flex">
        <RouterLink v-for="l in links" :key="l.to" :to="l.to" class="nav-link" exact-active-class="is-current">
          {{ l.label }}
        </RouterLink>
      </div>

      <div class="navbar-actions-wrapper flex items-center justify-end flex-1">
        <div class="navbar-actions hidden md:flex">
          <button type="button" class="theme-toggle" :aria-label="isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'" @click="toggleTheme">
            <svg v-if="!isDarkMode" class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M12 2.25a.75.75 0 01.75.75v2.25a.75.75 0 01-1.5 0V3a.75.75 0 01.75-.75zM7.5 12a4.5 4.5 0 119 0 4.5 4.5 0 01-9 0zM18.894 6.166a.75.75 0 00-1.06-1.06l-1.591 1.59a.75.75 0 101.06 1.061l1.591-1.59zM21.75 12a.75.75 0 01-.75.75h-2.25a.75.75 0 010-1.5H21a.75.75 0 01.75.75zM17.834 18.894a.75.75 0 001.06-1.06l-1.59-1.591a.75.75 0 10-1.061 1.06l1.59 1.591zM12 18a.75.75 0 01.75.75V21a.75.75 0 01-1.5 0v-2.25A.75.75 0 0112 18zM7.758 17.303a.75.75 0 00-1.061-1.06l-1.591 1.59a.75.75 0 001.06 1.061l1.591-1.59zM6 12a.75.75 0 01-.75.75H3a.75.75 0 010-1.5h2.25A.75.75 0 016 12zM6.697 7.757a.75.75 0 001.06-1.06l-1.59-1.591a.75.75 0 00-1.061 1.06l1.59 1.591z" />
            </svg>
            <svg v-else class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path fill-rule="evenodd" d="M9.528 1.718a.75.75 0 01.162.819A8.97 8.97 0 009 6a9 9 0 009 9 8.97 8.97 0 003.463-.69.75.75 0 01.981.98 10.503 10.503 0 01-9.694 6.46c-5.799 0-10.5-4.701-10.5-10.5 0-4.368 2.667-8.112 6.46-9.694a.75.75 0 01.818.162z" clip-rule="evenodd" />
            </svg>
          </button>
          <button v-if="authStore.isAuthenticated" type="button" class="navbar-cta" @click="handleLogout">Logout</button>
          <RouterLink v-else to="/login" class="navbar-cta">Login</RouterLink>
        </div>
      </div>

      <button type="button" class="menu-toggle md:hidden" :aria-expanded="showMobileMenu" aria-label="Toggle menu" @click="showMobileMenu = !showMobileMenu">
        <svg v-if="!showMobileMenu" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
        <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  </nav>

  <Transition @enter="onMenuEnter" @leave="onMenuLeave">
    <div v-if="showMobileMenu" class="mobile-menu md:hidden fixed inset-0 z-[1000000] flex flex-col">
      <div class="mobile-menu-header p-4 border-b border-card-border flex items-center justify-between">
        <div class="navbar-brand">
          <img :src="logo" alt="Prompt-Engine Logo" class="logo-icon" />
          <span class="brand-name">Prompt-Engine</span>
        </div>
        <button type="button" class="p-2" aria-label="Close menu" @click="showMobileMenu = false">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      <div class="mobile-menu-links">
        <RouterLink v-for="l in links" :key="l.to" :to="l.to" class="mobile-nav-link">{{ l.label }}</RouterLink>
      </div>
      <div class="mobile-menu-actions">
        <button type="button" class="mobile-theme-toggle" @click="toggleTheme">
          <span class="mr-2">{{ isDarkMode ? 'Light Mode' : 'Dark Mode' }}</span>
        </button>
        <button v-if="authStore.isAuthenticated" type="button" class="mobile-cta" @click="handleLogout">Logout</button>
        <RouterLink v-else to="/login" class="mobile-cta">Login</RouterLink>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.nav-link.is-current {
  color: var(--color-primary) !important;
}
</style>
