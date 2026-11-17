<script setup>
import { RouterLink } from 'vue-router'
import BrandMark from '@/components/layout/BrandMark.vue'
import Manuscript from '@/components/manuscript/Manuscript.vue'

defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
})

const sample = [
  { type: 'add', text: 'As a recruiter, ', note: 'A role sets the voice.' },
  { type: 'keep', text: 'write a job ad for a ' },
  { type: 'cut', text: 'developer. ' },
  { type: 'add', text: 'junior Vue developer in Kampala, under 150 words, with the salary range first.', note: 'Specifics replace guesswork.' },
]
</script>

<template>
  <div class="auth">
    <aside class="auth-side" aria-hidden="true">
      <RouterLink to="/" class="auth-brand" tabindex="-1">
        <BrandMark :size="28" />
        <span>Prompt Engine</span>
      </RouterLink>
      <div class="auth-side-body">
        <p class="auth-side-line">Every prompt gets a second draft.</p>
        <Manuscript :segments="sample" label="Example" />
      </div>
    </aside>

    <main class="auth-main">
      <div class="auth-panel">
        <RouterLink to="/" class="auth-brand auth-brand-sm" aria-label="Prompt Engine home">
          <BrandMark :size="26" />
          <span>Prompt Engine</span>
        </RouterLink>
        <h1 class="auth-title">{{ title }}</h1>
        <p v-if="subtitle" class="auth-subtitle">{{ subtitle }}</p>
        <slot />
        <RouterLink to="/" class="auth-back">Back to home</RouterLink>
      </div>
    </main>
  </div>
</template>

<style scoped>
.auth {
  min-height: 100vh;
  display: grid;
}
.auth-side {
  display: none;
}
.auth-brand {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  font-weight: 700;
  font-size: 1.05rem;
  color: var(--ink);
  text-decoration: none;
}
.auth-main {
  display: grid;
  place-items: center;
  padding: 2.5rem 1.25rem;
}
.auth-panel {
  width: 100%;
  max-width: 24rem;
}
.auth-brand-sm {
  margin-bottom: 2.5rem;
}
.auth-title {
  font-size: 2.1rem;
  font-weight: 750;
  letter-spacing: -0.04em;
}
.auth-subtitle {
  margin-top: 0.5rem;
  color: var(--ink-muted);
}
.auth-back {
  display: inline-block;
  margin-top: 2rem;
  font-size: 0.925rem;
  color: var(--ink-muted);
  text-decoration: underline;
  text-underline-offset: 3px;
}
.auth-back:hover {
  color: var(--ink);
}

@media (min-width: 960px) {
  .auth {
    grid-template-columns: minmax(0, 1.1fr) minmax(0, 1fr);
  }
  .auth-side {
    display: flex;
    flex-direction: column;
    padding: 2rem 3rem 3rem;
    background: var(--sheet-tint);
    border-right: 1px solid var(--rule);
  }
  .auth-side-body {
    margin: auto 0;
    max-width: 34rem;
  }
  .auth-side-line {
    font-size: clamp(1.9rem, 1rem + 2vw, 2.6rem);
    font-weight: 750;
    letter-spacing: -0.04em;
    line-height: 1.05;
    margin-bottom: 2rem;
    max-width: 14ch;
  }
  .auth-brand-sm {
    display: none;
  }
}
</style>
