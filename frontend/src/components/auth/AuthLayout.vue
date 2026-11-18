<script setup>
import { RouterLink } from 'vue-router'
import logo from '@/assets/images/logo.svg'

defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  image: { type: String, default: '/login_bg_branded.png' },
})
</script>

<template>
  <div class="auth">
    <aside class="auth-art" :style="{ backgroundImage: `url(${image})` }" aria-hidden="true"></aside>

    <main class="auth-main">
      <div class="auth-panel card">
        <RouterLink to="/" class="auth-brand" aria-label="Prompt-Engine home">
          <img :src="logo" alt="" class="auth-logo" />
          <span>Prompt-Engine</span>
        </RouterLink>
        <h1 class="auth-title">{{ title }}</h1>
        <p v-if="subtitle" class="auth-subtitle">{{ subtitle }}</p>
        <slot />
      </div>
      <RouterLink to="/" class="auth-back">
        <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        Back to Home
      </RouterLink>
    </main>
  </div>
</template>

<style scoped>
.auth {
  min-height: 100vh;
  display: grid;
  background: var(--color-background);
}
.auth-art {
  display: none;
  background-size: cover;
  background-position: center;
}
.auth-main {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1.25rem;
  padding: 2.5rem 1.25rem;
}
.auth-panel {
  width: 100%;
  max-width: 26rem;
  padding: 2rem 1.75rem;
}
.auth-brand {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 1.75rem;
  font-weight: 800;
  letter-spacing: -0.025em;
  color: var(--color-text);
  text-decoration: none;
}
.auth-logo {
  width: 30px;
  height: 30px;
}
.auth-title {
  font-size: 1.85rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: var(--color-text);
}
.auth-subtitle {
  margin-top: 0.4rem;
  color: var(--color-text-muted);
}
.auth-back {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.2rem;
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--color-text);
  text-decoration: none;
  border: 1px solid var(--color-card-border);
  border-radius: 2rem;
  background: var(--color-card-bg);
}
.auth-back:hover {
  background: var(--color-secondary);
}

@media (min-width: 960px) {
  .auth {
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  }
  .auth-art {
    display: block;
  }
}
</style>
