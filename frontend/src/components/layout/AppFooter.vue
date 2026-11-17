<script setup>
import { RouterLink } from 'vue-router'
import BrandMark from './BrandMark.vue'

const repo = 'https://github.com/Shakiran-Nannyombi/Prompt-Engine'
const year = new Date().getFullYear()
</script>

<template>
  <footer class="app-footer">
    <div class="wrap footer-grid">
      <div class="footer-brand">
        <RouterLink to="/" class="brand" aria-label="Prompt Engine home">
          <BrandMark :size="24" />
          <span>Prompt Engine</span>
        </RouterLink>
        <p class="footer-blurb">
          Two agents for better prompts: one rewrites them, one teaches you why.
        </p>
      </div>

      <nav class="footer-col" aria-label="Product">
        <h2 class="footer-heading">Product</h2>
        <RouterLink to="/refiner">Refiner</RouterLink>
        <RouterLink to="/coach">Coach</RouterLink>
        <RouterLink to="/tutorials">Tutorials</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>

      <nav class="footer-col" aria-label="Project">
        <h2 class="footer-heading">Project</h2>
        <a :href="repo" target="_blank" rel="noopener">Source on GitHub</a>
        <a :href="`${repo}/issues`" target="_blank" rel="noopener">Report an issue</a>
        <a :href="`${repo}/blob/main/LICENSE`" target="_blank" rel="noopener">Licence</a>
      </nav>
    </div>
    <div class="wrap footer-base">
      <p>© {{ year }} Prompt Engine. Built by Shakiran Nannyombi.</p>
    </div>
  </footer>
</template>

<style scoped>
.app-footer {
  border-top: 1px solid var(--rule);
  padding-top: 3.5rem;
  margin-top: 6rem;
}
.footer-grid {
  display: grid;
  gap: 2.5rem;
  grid-template-columns: 1fr 1fr;
}
.footer-brand {
  grid-column: 1 / -1;
}
.brand {
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  font-weight: 700;
  color: var(--ink);
  text-decoration: none;
}
.footer-blurb {
  margin-top: 0.85rem;
  max-width: 32ch;
  color: var(--ink-muted);
}
.footer-col {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}
.footer-heading {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--ink-muted);
  letter-spacing: 0;
  margin-bottom: 0.25rem;
}
.footer-col a {
  color: var(--ink);
  text-decoration: none;
  width: fit-content;
}
.footer-col a:hover {
  color: var(--pencil);
  text-decoration: underline;
  text-underline-offset: 3px;
}
.footer-base {
  margin-top: 3rem;
  padding-bottom: 2rem;
  font-size: 0.875rem;
  color: var(--ink-muted);
}
.footer-base p {
  padding-top: 1.25rem;
  border-top: 1px solid var(--rule);
}
@media (min-width: 768px) {
  .footer-grid {
    grid-template-columns: 2fr 1fr 1fr;
  }
  .footer-brand {
    grid-column: auto;
  }
}
</style>
