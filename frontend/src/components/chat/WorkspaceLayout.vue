<script setup>
/*
 * Shell for the Refiner and Coach screens: sidebar (drawer on mobile),
 * a slim top bar, and the conversation area.
 */
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useTheme } from '@/composables/useTheme'
import { useAuthStore } from '@/stores/useAuthStore'
import logo from '@/assets/images/logo.svg'

defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
})
const emit = defineEmits(['new-session'])

const { isDarkMode, toggleTheme, initTheme } = useTheme()
const authStore = useAuthStore()
const router = useRouter()
const drawerOpen = ref(false)

const tools = [
  { to: '/refiner', label: 'Refiner', hint: 'Rewrite a prompt' },
  { to: '/coach', label: 'Coach', hint: 'Write one step by step' },
]

const newSession = () => {
  drawerOpen.value = false
  emit('new-session')
}
const signOut = () => {
  authStore.logout()
  router.push('/')
}
const onKey = (e) => {
  if (e.key === 'Escape') drawerOpen.value = false
}

watch(drawerOpen, (open) => {
  document.body.style.overflow = open ? 'hidden' : ''
})
onMounted(() => {
  initTheme()
  window.addEventListener('keydown', onKey)
})
onUnmounted(() => {
  window.removeEventListener('keydown', onKey)
  document.body.style.overflow = ''
})
</script>

<template>
  <div class="workspace">
    <div v-if="drawerOpen" class="scrim" @click="drawerOpen = false"></div>

    <aside id="workspace-nav" class="side" :class="{ open: drawerOpen }" aria-label="Workspace">
      <RouterLink to="/" class="side-brand">
        <img :src="logo" alt="" class="side-logo" />
        <span>Prompt-Engine</span>
      </RouterLink>

      <button type="button" class="btn btn-primary side-new" @click="newSession">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true">
          <path d="M12 5v14M5 12h14" />
        </svg>
        New session
      </button>

      <nav class="side-tools" aria-label="Tools">
        <RouterLink v-for="t in tools" :key="t.to" :to="t.to" class="tool" @click="drawerOpen = false">
          <span class="tool-label">{{ t.label }}</span>
          <span class="tool-hint">{{ t.hint }}</span>
        </RouterLink>
      </nav>

      <div class="side-slot">
        <slot name="sidebar" />
      </div>

      <div class="side-foot">
        <button type="button" class="foot-btn" @click="toggleTheme">
          {{ isDarkMode ? 'Light mode' : 'Dark mode' }}
        </button>
        <RouterLink to="/tutorials" class="foot-btn">Guides</RouterLink>
        <button type="button" class="foot-btn" @click="signOut">Sign out</button>
      </div>
    </aside>

    <div class="main">
      <header class="topbar">
        <button
          type="button"
          class="menu-btn"
          aria-controls="workspace-nav"
          :aria-expanded="drawerOpen"
          aria-label="Open menu"
          @click="drawerOpen = true"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
            <path d="M4 7h16M4 12h16M4 17h10" />
          </svg>
        </button>
        <div class="topbar-text">
          <h1 class="topbar-title">{{ title }}</h1>
          <p v-if="subtitle" class="topbar-sub">{{ subtitle }}</p>
        </div>
        <div class="topbar-actions">
          <slot name="actions" />
        </div>
      </header>

      <div class="content">
        <slot />
      </div>
    </div>
  </div>
</template>

<style scoped>
.workspace {
  display: flex;
  height: 100vh;
  height: 100dvh;
  background: var(--paper);
  overflow: hidden;
}

.side {
  position: fixed;
  inset: 0 auto 0 0;
  z-index: 60;
  width: min(18rem, 86vw);
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  padding: 1rem 0.9rem;
  background: var(--sheet);
  border-right: 1px solid var(--rule);
  transform: translateX(-100%);
  transition: transform 220ms ease;
  overflow-y: auto;
}
.side.open {
  transform: translateX(0);
  box-shadow: var(--lift);
}
.scrim {
  position: fixed;
  inset: 0;
  z-index: 55;
  background: color-mix(in srgb, var(--ink) 35%, transparent);
}
.side-brand {
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  padding: 0.25rem 0.35rem;
  font-weight: 700;
  color: var(--ink);
  text-decoration: none;
}
.side-logo {
  width: 30px;
  height: 30px;
}
.side-brand {
  font-weight: 800;
  letter-spacing: -0.025em;
}
.side-new {
  width: 100%;
}
.side-tools {
  display: grid;
  gap: 0.25rem;
}
.tool {
  display: grid;
  padding: 0.6rem 0.75rem;
  border-radius: var(--radius-control);
  color: var(--ink);
  text-decoration: none;
  border: 1px solid transparent;
}
.tool:hover {
  background: var(--sheet-tint);
}
.tool.router-link-active {
  background: var(--sheet-tint);
  border-color: var(--rule);
  box-shadow: inset 3px 0 0 var(--pencil);
}
.tool-label {
  font-weight: 600;
}
.tool-hint {
  font-size: 0.85rem;
  color: var(--ink-muted);
}
.side-slot {
  flex: 1;
}
.side-foot {
  display: grid;
  gap: 0.15rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--rule);
}
.foot-btn {
  text-align: left;
  padding: 0.5rem 0.75rem;
  font: inherit;
  font-size: 0.925rem;
  color: var(--ink-muted);
  background: transparent;
  border: none;
  border-radius: var(--radius-control);
  text-decoration: none;
  cursor: pointer;
}
.foot-btn:hover {
  color: var(--ink);
  background: var(--sheet-tint);
}

.main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}
.topbar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-height: 4rem;
  padding: 0.6rem 1rem;
  border-bottom: 1px solid var(--rule);
  background: var(--paper);
}
.menu-btn {
  display: inline-grid;
  place-items: center;
  width: 2.5rem;
  height: 2.5rem;
  color: var(--ink);
  background: transparent;
  border: 1px solid var(--rule);
  border-radius: var(--radius-control);
  cursor: pointer;
}
.topbar-title {
  font-size: 1.15rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}
.topbar-sub {
  font-size: 0.875rem;
  color: var(--ink-muted);
}
.topbar-actions {
  margin-left: auto;
  display: flex;
  gap: 0.5rem;
}
.content {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
}

@media (min-width: 1024px) {
  .side {
    position: static;
    transform: none;
    box-shadow: none;
    width: 17rem;
    flex-shrink: 0;
  }
  .scrim,
  .menu-btn {
    display: none;
  }
  .topbar {
    padding: 0.6rem 1.75rem;
  }
}
</style>
