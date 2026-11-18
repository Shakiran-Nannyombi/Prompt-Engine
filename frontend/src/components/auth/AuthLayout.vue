<script setup>
import { RouterLink } from 'vue-router'
import logo from '@/assets/images/logo.svg'

defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
})

const benefits = [
  'Rewrite any prompt in one pass with the Refiner',
  'Learn to write your own with the step-by-step Coach',
  'Use the results in ChatGPT, Claude, Gemini or any AI tool',
]
const year = new Date().getFullYear()
</script>

<template>
  <div class="auth">
    <aside class="auth-brand-panel" aria-label="About Prompt-Engine">
      <RouterLink to="/" class="panel-brand">
        <span class="panel-logo"><img :src="logo" alt="" /></span>
        <span>Prompt-Engine</span>
      </RouterLink>

      <div class="panel-body">
        <h2 class="panel-title">Better prompts, <span class="panel-accent">better answers.</span></h2>
        <p class="panel-lede">Two AI agents that turn rough ideas into clear, structured prompts.</p>

        <ul class="panel-benefits">
          <li v-for="b in benefits" :key="b">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M5 12.5l4.5 4.5L19 7.5" />
            </svg>
            {{ b }}
          </li>
        </ul>

        <figure class="panel-example">
          <div class="example-row">
            <span class="example-label">Before</span>
            <p class="example-text muted">Write a blog post about AI.</p>
          </div>
          <div class="example-row">
            <span class="example-label accent">After</span>
            <p class="example-text">
              Write a 600-word blog post for small-business owners on three practical ways to use AI in customer
              support, with a short checklist at the end.
            </p>
          </div>
        </figure>
      </div>

      <p class="panel-foot">© {{ year }} Prompt-Engine</p>
    </aside>

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

/* Branded panel: dark slate with a soft brand glow */
.auth-brand-panel {
  display: none;
  position: relative;
  overflow: hidden;
  flex-direction: column;
  padding: 2.5rem 3rem;
  color: #f1f5f9;
  background:
    radial-gradient(60% 50% at 85% 10%, rgba(233, 30, 99, 0.35), transparent 70%),
    radial-gradient(55% 45% at 10% 95%, rgba(156, 39, 176, 0.35), transparent 70%),
    #0f172a;
}
.auth-brand-panel::after {
  /* faint grid texture for depth */
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.04) 1px, transparent 1px);
  background-size: 48px 48px;
  mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 0.9), transparent 85%);
  pointer-events: none;
}
.auth-brand-panel > * {
  position: relative;
  z-index: 1;
}
.panel-brand {
  display: inline-flex;
  align-items: center;
  gap: 0.7rem;
  font-weight: 800;
  font-size: 1.1rem;
  letter-spacing: -0.025em;
  color: #ffffff;
  text-decoration: none;
}
.panel-logo {
  display: grid;
  place-items: center;
  width: 2.5rem;
  height: 2.5rem;
  background: #ffffff;
  border-radius: 0.75rem;
}
.panel-logo img {
  width: 1.9rem;
  height: 1.9rem;
}
.panel-body {
  margin: auto 0;
  max-width: 30rem;
  padding: 3rem 0;
}
.panel-title {
  font-size: clamp(2rem, 1.2rem + 2vw, 2.75rem);
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -0.035em;
  color: #ffffff;
}
.panel-accent {
  background: linear-gradient(135deg, #ff4d8d, #c56cf0);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
.panel-lede {
  margin-top: 1rem;
  font-size: 1.05rem;
  line-height: 1.6;
  color: #cbd5e1;
}
.panel-benefits {
  list-style: none;
  margin: 2rem 0 0;
  padding: 0;
  display: grid;
  gap: 0.85rem;
}
.panel-benefits li {
  display: flex;
  align-items: flex-start;
  gap: 0.7rem;
  font-size: 0.975rem;
  color: #e2e8f0;
}
.panel-benefits svg {
  flex-shrink: 0;
  margin-top: 0.1rem;
  padding: 2px;
  color: #ffffff;
  background: linear-gradient(135deg, #e91e63, #9c27b0);
  border-radius: 50%;
}
.panel-example {
  margin: 2.5rem 0 0;
  padding: 1.25rem 1.35rem;
  display: grid;
  gap: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1.25rem;
  backdrop-filter: blur(6px);
}
.example-row {
  display: grid;
  gap: 0.35rem;
}
.example-label {
  font-size: 0.75rem;
  font-weight: 700;
  color: #94a3b8;
}
.example-label.accent {
  color: #ff7aa8;
}
.example-text {
  font-size: 0.95rem;
  line-height: 1.55;
  color: #f1f5f9;
}
.example-text.muted {
  color: #94a3b8;
  text-decoration: line-through;
  text-decoration-color: rgba(255, 122, 168, 0.7);
}
.panel-foot {
  font-size: 0.85rem;
  color: #64748b;
}

/* Form side */
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
  .auth-brand-panel {
    display: flex;
  }
  .auth-brand {
    display: none;
  }
}
</style>
