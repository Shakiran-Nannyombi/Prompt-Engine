<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { useTheme } from '@/composables/useTheme'
import { useAuthStore } from '@/stores/useAuthStore'
import BrandMark from './BrandMark.vue'

const links = [
  { to: '/refiner', label: 'Refiner' },
  { to: '/coach', label: 'Coach' },
  { to: '/tutorials', label: 'Tutorials' },
  { to: '/about', label: 'About' },
]

const { isDarkMode, toggleTheme, initTheme } = useTheme()
const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()

const menuOpen = ref(false)
const scrolled = ref(false)

const onScroll = () => {
  scrolled.value = window.scrollY > 8
}
const onKey = (e) => {
  if (e.key === 'Escape') menuOpen.value = false
}

const signOut = () => {
  authStore.logout()
  menuOpen.value = false
  router.push('/')
}

watch(() => route.fullPath, () => {
  menuOpen.value = false
})
watch(menuOpen, (open) => {
  document.body.style.overflow = open ? 'hidden' : ''
})

onMounted(() => {
  initTheme()
  onScroll()
  window.addEventListener('scroll', onScroll, { passive: true })
  window.addEventListener('keydown', onKey)
})
onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
  window.removeEventListener('keydown', onKey)
  document.body.style.overflow = ''
})
</script>

<template>
  <header class="app-header" :class="{ 'is-scrolled': scrolled }">
    <div class="wrap header-row">
      <RouterLink to="/" class="brand" aria-label="Prompt Engine home">
        <BrandMark :size="28" />
        <span class="brand-name">Prompt Engine</span>
      </RouterLink>

      <nav class="desktop-nav" aria-label="Main">
        <RouterLink v-for="link in links" :key="link.to" :to="link.to" class="nav-link">
          {{ link.label }}
        </RouterLink>
      </nav>

      <div class="header-actions">
        <button
          type="button"
          class="icon-btn"
          :aria-label="isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'"
          @click="toggleTheme"
        >
          <svg v-if="isDarkMode" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
            <circle cx="12" cy="12" r="4" />
            <path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" />
          </svg>
          <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z" />
          </svg>
        </button>

        <button v-if="authStore.isAuthenticated" type="button" class="btn btn-secondary hide-sm" @click="signOut">
          Sign out
        </button>
        <RouterLink v-else to="/login" class="btn btn-primary hide-sm">Sign in</RouterLink>

        <button
          type="button"
          class="icon-btn menu-btn"
          :aria-expanded="menuOpen"
          aria-controls="mobile-menu"
          :aria-label="menuOpen ? 'Close menu' : 'Open menu'"
          @click="menuOpen = !menuOpen"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
            <path v-if="menuOpen" d="M6 6l12 12M18 6L6 18" />
            <path v-else d="M4 7h16M4 12h16M4 17h10" />
          </svg>
        </button>
      </div>
    </div>

    <Transition name="sheet">
      <div v-if="menuOpen" id="mobile-menu" class="mobile-menu">
        <nav class="wrap mobile-nav" aria-label="Mobile">
          <RouterLink to="/" class="mobile-link">Home</RouterLink>
          <RouterLink v-for="link in links" :key="link.to" :to="link.to" class="mobile-link">
            {{ link.label }}
          </RouterLink>
          <div class="mobile-actions">
            <button v-if="authStore.isAuthenticated" type="button" class="btn btn-secondary" @click="signOut">Sign out</button>
            <RouterLink v-else to="/login" class="btn btn-primary">Sign in</RouterLink>
          </div>
        </nav>
      </div>
    </Transition>
  </header>
</template>

<style scoped>
.app-header {
  position: sticky;
  top: 0;
  z-index: 50;
  background-color: color-mix(in srgb, var(--paper) 88%, transparent);
  backdrop-filter: saturate(1.4) blur(10px);
  border-bottom: 1px solid transparent;
  transition: border-color 200ms;
}
.app-header.is-scrolled {
  border-bottom-color: var(--rule);
}
.header-row {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  height: 4rem;
}
.brand {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  text-decoration: none;
  color: var(--ink);
}
.brand-name {
  font-weight: 700;
  font-size: 1.05rem;
  letter-spacing: -0.02em;
}
.desktop-nav {
  display: none;
  gap: 0.25rem;
  margin-left: 1rem;
}
.nav-link {
  position: relative;
  padding: 0.5rem 0.75rem;
  color: var(--ink-muted);
  font-weight: 500;
  text-decoration: none;
  border-radius: var(--radius-control);
}
.nav-link:hover {
  color: var(--ink);
}
.nav-link.router-link-active {
  color: var(--ink);
}
.nav-link.router-link-active::after {
  content: '';
  position: absolute;
  left: 0.75rem;
  right: 0.75rem;
  bottom: 0.2rem;
  height: 2px;
  background: var(--pencil);
  border-radius: 2px;
}
.header-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-left: auto;
}
.icon-btn {
  display: inline-grid;
  place-items: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: var(--radius-control);
  color: var(--ink);
  background: transparent;
  border: 1px solid transparent;
  cursor: pointer;
}
.icon-btn:hover {
  background-color: var(--sheet-tint);
}
.hide-sm {
  display: none;
}
.mobile-menu {
  position: fixed;
  inset: 4rem 0 0 0;
  background-color: var(--paper);
  border-top: 1px solid var(--rule);
  overflow-y: auto;
}
.mobile-nav {
  display: flex;
  flex-direction: column;
  padding-top: 1rem;
  padding-bottom: 2rem;
}
.mobile-link {
  padding: 0.9rem 0;
  font-size: 1.5rem;
  font-weight: 600;
  letter-spacing: -0.02em;
  color: var(--ink);
  text-decoration: none;
  border-bottom: 1px solid var(--rule);
}
.mobile-link.router-link-exact-active {
  color: var(--pencil);
}
.mobile-actions {
  display: flex;
  margin-top: 1.5rem;
}
.mobile-actions .btn {
  flex: 1;
}
.sheet-enter-active,
.sheet-leave-active {
  transition: opacity 180ms ease, transform 180ms ease;
}
.sheet-enter-from,
.sheet-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

@media (min-width: 768px) {
  .desktop-nav {
    display: flex;
  }
  .hide-sm {
    display: inline-flex;
  }
  .menu-btn,
  .mobile-menu {
    display: none;
  }
}
</style>
